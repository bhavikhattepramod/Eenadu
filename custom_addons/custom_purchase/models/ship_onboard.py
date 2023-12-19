from odoo import fields, models, api, _

class ShipOnboard(models.Model):
	_name = "ship.onboard"
	_rec_name = "purchase_order_id"

	policy_number_id = fields.Many2one('international.policy', string = 'Policy Number')
	purchase_order_id = fields.Many2one('purchase.order', string = 'Purchase Order')
	vendor_partner_id = fields.Many2one('res.partner', string = 'Vendor')
	agent_partner_id = fields.Many2one('res.partner', string = 'Insurance Agent')
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	total_ship_onboard_value = fields.Monetary(string = 'Total Ship On-board Price', currency_field='currency_id', compute='_compute_total_ship_onboard_value')
	
	ship_oboard_line_ids = fields.One2many('ship.onboard.line','ship_onboard_line_id', string = 'Ship On-Board Details')

	additional_charges_line_ids = fields.One2many('ship.onboard.additional.charges', 'additional_charges_line_id', string = "Additional Charges")

	total_estimated_additional_charges = fields.Monetary('Total Estimated Additional Charges', currency_field="currency_id", compute="_compute_estimated_total_additional_charges")
	total_estimated_tax_charges = fields.Monetary('Total Estimated Tax Charges', currency_field="currency_id", compute="_compute_total_estimated_tax_charges")
	total_actual_additional_charges = fields.Monetary('Total Actual Additional Charges', currency_field="currency_id", compute="_compute_actual_total_additional_charges")
	total_actual_tax_charges = fields.Monetary('Total Actual Tax Charges', currency_field="currency_id", compute="_compute_total_actual_tax_charges")

	@api.depends('additional_charges_line_ids')
	def _compute_estimated_total_additional_charges(self):
		for rec in self:
			if rec.additional_charges_line_ids:
				total_estimated_additional_charges = 0.0
				for line in rec.additional_charges_line_ids:
					total_estimated_additional_charges += line.price_unit
				rec.total_estimated_additional_charges = total_estimated_additional_charges
			else:
				rec.total_estimated_additional_charges = 0.0

	@api.depends('additional_charges_line_ids')
	def _compute_total_estimated_tax_charges(self):
		for rec in self:
			if rec.additional_charges_line_ids:
				total_estimated_tax_charges = 0.0
				for line in rec.additional_charges_line_ids:
					total_estimated_tax_charges += line.price_tax_estimate
				rec.total_estimated_tax_charges = total_estimated_tax_charges
			else:
				rec.total_estimated_tax_charges = 0.0

	@api.depends('additional_charges_line_ids')
	def _compute_actual_total_additional_charges(self):
		for rec in self:
			if rec.additional_charges_line_ids:
				total_actual_additional_charges = 0.0
				for line in rec.additional_charges_line_ids:
					total_actual_additional_charges += line.actual_amount
				rec.total_actual_additional_charges = total_actual_additional_charges
			else:
				rec.total_actual_additional_charges = 0.0

	@api.depends('additional_charges_line_ids')
	def _compute_total_actual_tax_charges(self):
		for rec in self:
			if rec.additional_charges_line_ids:
				total_actual_tax_charges = 0.0
				for line in rec.additional_charges_line_ids:
					total_actual_tax_charges += line.price_tax_actual
				rec.total_actual_tax_charges = total_actual_tax_charges
			else:
				rec.total_actual_tax_charges = 0.0


	@api.depends('ship_oboard_line_ids')
	def _compute_total_ship_onboard_value(self):
		for rec in self:
			if rec.ship_oboard_line_ids:
				total_ship_onboard_value = 0.0
				for line in rec.ship_oboard_line_ids:
					total_ship_onboard_value += line.ship_onboard_value
				rec.total_ship_onboard_value = total_ship_onboard_value
			else:
				rec.total_ship_onboard_value = 0.0

	@api.onchange('policy_number_id')
	def onchange_agent_partner_id(self):
		if self.policy_number_id:
			self.agent_partner_id = self.policy_number_id.policy_provider_id.id

	@api.model
	def create(self, vals):
		if vals.get('purchase_order_id'):
			international_policy_obj = self.env['international.policy'].search([('state', '=', 'running')])
			if international_policy_obj:
				po_count = 0
				for line in international_policy_obj.policy_line_ids:
					if line.purchase_order_id.id == vals.get('purchase_order_id'):
						po_count += 1
					else:
						po_count = po_count
				if po_count == 0:
					policy_line_list = []
					policy_line_list.append([0, 0, {
						'purchase_order_id': int(vals.get('purchase_order_id')),
						'policy_line_id': international_policy_obj,
						}])
					international_policy_obj.policy_line_ids = policy_line_list

		res = super(ShipOnboard, self).create(vals)

		return res

class ShipOnboardLine(models.Model):
	_name = "ship.onboard.line"

	name = fields.Char('Ship On-Board Number')
	product_id = fields.Many2one('product.product', string = 'Product')
	product_qty = fields.Float('Quantity')
	product_uom_id = fields.Many2one('uom.uom', string = 'UOM')
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	unit_price = fields.Monetary('Unit Price', currency_field='currency_id')
	ship_onboard_value = fields.Monetary('Ship On-Board Value', currency_field='currency_id', compute='_compute_ship_onboard_value')

	ship_onboard_line_id = fields.Many2one('ship.onboard', string = 'Ship On-Board Ref')

	order_id = fields.Many2one('purchase.order', string = "Purchase order ref", related='ship_onboard_line_id.purchase_order_id')


	@api.depends('product_qty','unit_price')
	def _compute_ship_onboard_value(self):
		for rec in self:
			rec.ship_onboard_value = rec.product_qty * rec.unit_price

	@api.onchange('product_id')
	def onchange_product_id(self):
		if self.product_id:
			self.product_uom_id = self.product_id.uom_id.id

	@api.onchange('order_id')
	def onchange_order_id(self):
		if self.order_id:
			product_list = []
			for line in self.order_id.order_line:
				product_list.append(line.product_id.id)
			
			res_domain = {'domain': {
				'product_id': "[('id', '=', False)]"
				}}

			res_domain['domain']['product_id'] = "[('id', 'in', %s)]" % product_list

			return res_domain


class ShipOnboardAdditionalCharges(models.Model):
	_name = "ship.onboard.additional.charges"

	product_id = fields.Many2one('product.product', string = "Tax Desc", domain="[('detailed_type', '=', 'service')]")
	product_desc = fields.Char("Tax Type")
	product_qty = fields.Float("Qty", default=1)
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	price_unit = fields.Monetary('Estimated Tax Amount', currency_field = 'currency_id')
	taxes_id = fields.Many2many('account.tax', string='Taxes', domain=['|', ('active', '=', False), ('active', '=', True)])

	actual_amount = fields.Monetary('Actual Tax Amount', currency_field = 'currency_id')

	additional_charges_line_id = fields.Many2one('ship.onboard', string = "Ship On-Board Ref")


	price_tax_estimate = fields.Float(compute='_compute_estimate_tax_amount', string='Tax Estimated', store=True)
	price_tax_actual = fields.Float(compute='_compute_actual_tax_amount', string='Tax Actual', store=True)

	@api.depends('product_qty', 'price_unit', 'taxes_id')
	def _compute_estimate_tax_amount(self):
		for line in self:
			tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_estimate_base_line_dict()])
			totals = list(tax_results['totals'].values())[0]
			amount_tax = totals['amount_tax']

			line.update({
				'price_tax_estimate': amount_tax,
			})


	def _convert_to_tax_estimate_base_line_dict(self):
		""" Convert the current record to a dictionary in order to use the generic taxes computation method
		defined on account.tax.

		:return: A python dictionary.
		"""
		self.ensure_one()
		return self.env['account.tax']._convert_to_tax_base_line_dict(
			self,
			currency=self.currency_id,
			product=self.product_id,
			taxes=self.taxes_id,
			price_unit=self.price_unit,
			quantity=self.product_qty,
		)

	@api.depends('product_qty', 'actual_amount', 'taxes_id')
	def _compute_actual_tax_amount(self):
		for line in self:
			tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_actual_base_line_dict()])
			totals = list(tax_results['totals'].values())[0]
			amount_tax = totals['amount_tax']

			line.update({
				'price_tax_actual': amount_tax,
			})


	def _convert_to_tax_actual_base_line_dict(self):
		""" Convert the current record to a dictionary in order to use the generic taxes computation method
		defined on account.tax.

		:return: A python dictionary.
		"""
		self.ensure_one()
		return self.env['account.tax']._convert_to_tax_base_line_dict(
			self,
			currency=self.currency_id,
			product=self.product_id,
			taxes=self.taxes_id,
			price_unit=self.actual_amount,
			quantity=self.product_qty,
		)