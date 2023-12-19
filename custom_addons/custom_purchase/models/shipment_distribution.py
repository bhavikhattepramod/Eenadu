from odoo import fields, models, api, _

class DistributeShipments(models.Model):
	_name = "distribute.shipments"
	_rec_name = "picking_id"

	def _compute_shipment_distribution_count(self):
		shipment_distribution_obj = self.env['stock.picking'].search([('origin', '=', self.picking_id.name),('is_distibution_picking', '=', True)])

		self.shipment_distribution_count = len(shipment_distribution_obj)

	def _compute_domestic_insurance_claim_count(self):
		claim_insurance_obj = self.env['claim.domestic.insurance'].search([('delivery_challan_no_id', '=', self.id)])

		self.domestic_insurance_claim_count = len(claim_insurance_obj)

	delivery_challan_no = fields.Char("Delivery Challan No")
	unit_partner_id = fields.Many2one('res.partner', string = "Unit Name")
	delivery_challan_date = fields.Date("Delivery Challan Date")
	issue_unit_date = fields.Date("Issue Date")
	lorry_no = fields.Char("Lorry Number")
	lorry_recipt_no = fields.Char("Lorry Recipt No")
	source_warehouse_id = fields.Many2one('stock.warehouse', string = "Source Warehouse")
	source_dest_id = fields.Many2one('stock.location', string = "Sources Location", domain="[('usage','=','internal')]")
	warehouse_dest_id = fields.Many2one('stock.warehouse', string = "Destination Warehouse")
	location_dest_id = fields.Many2one('stock.location', string = "Destination Location", domain="[('usage','=','internal')]")

	picking_id = fields.Many2one('stock.picking', string = "Shipment(GRN)")

	distribute_shipments_line_ids = fields.One2many('distribute.shipments.line','distribute_shipments_line_id', string = "Distribution Lines")

	shipment_distribution_count = fields.Integer(string = 'Shipment', compute='_compute_shipment_distribution_count')

	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	total_shipment_value = fields.Monetary(string = 'Total Ship On-board Price', currency_field='currency_id', compute='_compute_total_shipment_value')

	domestic_insurance_claim_count = fields.Integer(string = 'Claim Count', compute='_compute_domestic_insurance_claim_count')

	purchase_order_id = fields.Many2one('purchase.order', string = "Purchase Order")
	policy_number_id = fields.Many2one('domestic.policy', string = "Policy Number")
	invoice_id = fields.Many2one('account.move', string = "Invoice No")
	invoice_number = fields.Char('Invoice No')
	clearing_agent_id = fields.Many2one('res.partner', string = "Clearing Agent Name", domain="[('is_clearing_agent', '=', True)]")
	no_of_containers = fields.Integer('No. of Containers')
	bl_number = fields.Char("Bl.No")
	sum_insured = fields.Monetary("Sum Insured", currency_field="currency_id")
	qty_as_per_po = fields.Float("Quantity", compute="_compute_po_qty")
	po_qty_uom = fields.Many2one('uom.uom', string = "UoM")

	@api.depends('purchase_order_id')
	def _compute_po_qty(self):
		for rec in self:
			if rec.purchase_order_id:
				qty_as_per_po = 0.0
				po_qty_uom = None
				for line in rec.purchase_order_id.order_line:
					qty_as_per_po += line.qty_received
					po_qty_uom = line.product_uom.id
				rec.qty_as_per_po = qty_as_per_po
				rec.po_qty_uom = po_qty_uom
			else:
				rec.qty_as_per_po = 0.0
				rec.po_qty_uom = None

	@api.depends('distribute_shipments_line_ids')
	def _compute_total_shipment_value(self):
		for rec in self:
			if rec.distribute_shipments_line_ids:
				total_shipment_value = 0.00
				for line in rec.distribute_shipments_line_ids:
					total_shipment_value += line.price_subtotal
				rec.total_shipment_value = total_shipment_value
			else:
				rec.total_shipment_value = 0.00

	@api.onchange('picking_id')
	def onchange_picking_id(self):
		if self.picking_id:
			purchase_order_obj = self.env['purchase.order'].search([('name', '=', self.picking_id.origin)])
			self.purchase_order_id = purchase_order_obj.id

	@api.onchange('purchase_order_id')
	def onchange_purchase_order_id(self):
		if self.purchase_order_id:
			for line in self.purchase_order_id.order_line:
				for inv_line in line.invoice_lines:
					self.invoice_id = inv_line.move_id.id

	def create_transfer(self):
		location_list = []

		if self.distribute_shipments_line_ids:
			for line in self.distribute_shipments_line_ids:
				if line.destination_location.id not in location_list:
					location_list.append(line.destination_location.id)


		for location in location_list:
			location_obj = self.env['stock.location'].browse(int(location))
			distribution_line_obj = self.env['distribute.shipments.line'].search([
				('destination_location', '=', int(location)),
				('distribute_shipments_line_id', '=', self.id),
				('picking_id', '=', self.picking_id.id)
				])
			distribution_lines = []
			if distribution_line_obj:
				source_location = 0
				for distribution_line in distribution_line_obj:
					source_location = distribution_line.source_location.id
					distribution_lines.append((0, 0, {
						'product_id':distribution_line.product_id.id,
						'name':distribution_line.product_id.name,
						'location_id':distribution_line.source_location.id,
						'location_dest_id':distribution_line.destination_location.id,
						'product_uom_qty':distribution_line.transfer_qty,
						'product_uom':distribution_line.product_id.uom_id.id
						}))
				warehouse_obj = self.env['stock.warehouse'].search([
					('view_location_id', '=', location_obj.location_id.id)
					])
				picking_type_obj = self.env['stock.picking.type'].search([('warehouse_id', '=', warehouse_obj.id),('sequence_code', '=', 'DC')])

				vals = {
						'partner_id': self.unit_partner_id.id,
						'picking_type_id': picking_type_obj.id,
						'location_id': source_location,
						'location_dest_id': location_obj.id,
						'move_ids_without_package': distribution_lines,
						'is_distibution_picking':True,
						'origin':self.picking_id.name
					}

				picking_id = self.env["stock.picking"].create(vals)

				picking_id.action_confirm()

				# operation_lines = []
				for operation_line in picking_id.move_ids_without_package:
					stock_move_id = operation_line
					if stock_move_id.move_line_ids:
						stock_move_id.move_line_ids.unlink()

				# 	line_distribution_obj = self.env['distribute.shipments.line'].search([
				# 		('destination_location', '=', int(location)),
				# 		('distribute_shipments_line_id', '=', self.id),
				# 		('picking_id', '=', self.picking_id.id),
				# 		('product_id', '=', operation_line.product_id.id)
				# 		])

				# 	for line_distribution in line_distribution_obj:
				# 		operation_lines.append((0, 0, {
				# 			'lot_id': [],
				# 			'qty_done': line_distribution.gross_qty,
				# 			'product_uom_id': line_distribution.product_uom.id,
				# 			'location_id': line_distribution.source_location.id,
				# 			'location_dest_id': line_distribution.destination_location.id,
				# 			'product_id': line_distribution.product_id.id,
				# 			'picking_id': picking_id.id,
				# 			'move_id' : stock_move_id.id,
				# 			}))

				# stock_move_id.move_line_ids = operation_lines


	def action_view_distribution(self):

		return {
            'name': _('Shipment Distribution'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('origin', '=', self.picking_id.name),('is_distibution_picking', '=', True)],
            'views_id': False,
            'views': [(self.env.ref('stock.vpicktree').id or False, 'tree'),
                      (self.env.ref('stock.view_picking_form').id or False, 'form')],
        }

	def action_create_domestic_insurance_claim(self):
		ctx = dict()

		ctx = ({
			'default_delivery_challan_no_id': self.id,
			'default_vendor_partner_id': self.unit_partner_id.id,
		})

		form_id = self.env.ref('custom_purchase.claim_domestic_insurance_form_view').id

		return {
			'name': _('Claim Domestic Insurance'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'claim.domestic.insurance',
			'views_id': False,
			'views': [(form_id or False, 'form')],
			'target': 'new',
			'context': ctx,
		}

	def action_view_domestic_insurance_claim(self):

		return {
			'name': _('Domestic Insurance Claim'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'claim.domestic.insurance',
			'domain': [('delivery_challan_no_id', '=', self[0].id)],
			'views_id': False,
			'views': [(self.env.ref('custom_purchase.claim_domestic_insurance_tree_view').id or False, 'tree'),
			(self.env.ref('custom_purchase.claim_domestic_insurance_form_view').id or False, 'form')],
		}

class DistributeShipmentsLine(models.Model):
	_name = "distribute.shipments.line"

	reels_lot_id = fields.Many2one('stock.lot', string = "Reel No")
	product_code = fields.Char("Item Code")
	hsn_code = fields.Char("HSN Code")
	gross_qty = fields.Float("Gross QTY")
	damage_qty = fields.Float("Damage QTY")
	net_qty = fields.Float("Net QTY", compute="_compute_net_qty")
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	unit_rate = fields.Monetary(string = 'Unit Rate', currency_field='currency_id')
	price_subtotal = fields.Monetary(string = "Amount", currency_field='currency_id', compute="_compute_price_subtotal")

	distribute_shipments_line_id = fields.Many2one('distribute.shipments', string = "Distribute Shipments Ref")

	picking_id = fields.Many2one('stock.picking', string = "Picking Ref", related="distribute_shipments_line_id.picking_id")
	product_id = fields.Many2one('product.product', string = "Product Name")
	product_uom = fields.Many2one('uom.uom', string = "UoM")
	no_of_reels = fields.Integer('No. of Reels')
	transfer_qty = fields.Float("Transfer QTY")
	source_location = fields.Many2one('stock.location', string = "Source Location", related='distribute_shipments_line_id.picking_id.location_dest_id', domain="[('usage','=','internal')]")
	destination_location = fields.Many2one('stock.location', string = "Destination Location", domain="[('usage','=','internal')]")
	transport_partner_id = fields.Many2one('res.partner', string = "Transporter")
	lorry_reg_no = fields.Char("Lorry Reg #")
	transporter_contact_no = fields.Char('Transporter Phone')

	@api.onchange('picking_id')
	def onchange_picking_id(self):
		if self.picking_id:
			product_list = []
			for line in self.picking_id.move_ids_without_package:
				product_list.append(line.product_id.id)

			res_domain = {'domain': {
				'product_id': "[('id', '=', False)]"
				}}

			res_domain['domain']['product_id'] = "[('id', 'in', %s)]" % product_list

			return res_domain

	@api.onchange('product_id')
	def onchange_product_id(self):
		if self.product_id:
			self.product_uom = self.product_id.uom_id
	
	@api.depends('gross_qty','damage_qty')
	def _compute_net_qty(self):
		for rec in self:
			rec.net_qty = rec.gross_qty - rec.damage_qty

	@api.depends('net_qty','unit_rate')
	def _compute_price_subtotal(self):
		for rec in self:
			rec.price_subtotal = rec.net_qty * rec.unit_rate

	@api.onchange('reels_lot_id')
	def onchange_reels_lot_id(self):
		if self.reels_lot_id:
			self.product_code = self.reels_lot_id.product_id.default_code
			self.hsn_code = self.reels_lot_id.product_id.l10n_in_hsn_code
			self.product_id = self.reels_lot_id.product_id.id
			self.product_uom = self.reels_lot_id.product_id.uom_id
			self.gross_qty = self.reels_lot_id.product_qty
			self.damage_qty = self.reels_lot_id.damage_qty
			self.unit_rate = self.reels_lot_id.reel_price_unit