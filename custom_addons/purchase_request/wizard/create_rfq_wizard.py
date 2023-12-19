from odoo import _, api, fields, models
from datetime import datetime
from odoo.exceptions import UserError

class CreateRfqWizard(models.TransientModel):
	_name = 'create.rfq.wizard'

	supplier_id = fields.Many2one("res.partner",string="Supplier",required=True,)

	purchase_request_id = fields.Many2one('purchase.request', string="Indend Request")

	create_rfq_line_ids = fields.One2many('create.rfq.wizard.line','create_rfq_line_id',string='Create RFQ Wizard Ref')
	select_all = fields.Boolean('Select All')

	@api.onchange('select_all')
	def onchange_select_all(self):
		if self.select_all == True:
			for line in self.create_rfq_line_ids:
				if line.rfq_created == False :
					line.create_rfq = True
		if self.select_all == False:
			for line in self.create_rfq_line_ids:
				if line.rfq_created == False:
					line.create_rfq = False

	def make_purchase_order_from_indend(self):
		po_line_list = []

		for line in self.create_rfq_line_ids:
			if line.create_rfq == True and line.rfq_created == False:
				po_line_list.append((0, 0, {
						'product_id' : line.product_id.id,
						'name' : line.name,
						'product_qty' : line.product_qty,
						'product_uom' : line.product_uom_id.id,
						# 'price_unit' : 0.0,
						'date_planned' : datetime.now()
					}))
				line.purchase_request_line_id.rfq_created = True
				line.rfq_created = True

		po_vals = {
			'partner_id' : self.supplier_id.id,
			'order_line' : po_line_list,
			'purchase_request_id' : self.purchase_request_id.id
		}
		rfq_id = self.env["purchase.order"].create(po_vals)

class CreateRfqWizardLine(models.TransientModel):
	_name = 'create.rfq.wizard.line'

	create_rfq_line_id = fields.Many2one('create.rfq.wizard', string='Create RFQ Wizard Ref')
	purchase_request_id = fields.Many2one('purchase.request', string="Indend Request")
	purchase_request_line_id = fields.Many2one('purchase.request.line', string='Purchase Request Line ID')
	product_id = fields.Many2one('product.product', string='Product')
	name = fields.Char('Description')
	product_qty = fields.Float('Quantity to Purchase')
	product_uom_id = fields.Many2one('uom.uom', string='Uom')
	create_rfq = fields.Boolean('Create RFQ')
	rfq_created = fields.Boolean('RFQ Created')