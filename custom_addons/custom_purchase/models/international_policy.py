from odoo import fields, models, api, _

class InternationalPolicy(models.Model):
	_name = "international.policy"

	name = fields.Char('Policy Number')
	policy_provider_id = fields.Many2one('res.partner', string = 'Policy Provider')
	policy_start_date = fields.Date('Policy Start Date')
	policy_end_date = fields.Date('Policy End Date')
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	policy_amount = fields.Monetary(string = 'Policy Amount', currency_field='currency_id')
	total_ship_onboard_value = fields.Monetary(string = 'Ship On-Board Value', currency_field='currency_id', compute='_compute_total_ship_onboard_value')
	total_estimated_additional_charges_with_tax = fields.Monetary(string = 'Total Estimated Additional Charges With Tax', currency_field='currency_id', compute='_compute_total_estimated_additional_charges_with_tax')
	total_actual_additional_charges_with_tax = fields.Monetary(string = 'Total Actual Additional Charges With Tax', currency_field='currency_id', compute='_compute_total_actual_additional_charges_with_tax')
	balance_amount = fields.Monetary(string = 'Balance', currency_field='currency_id', compute='_compute_balance_amount')
	state = fields.Selection([
		('running','Running'),
		('expired','Expired')
		], string = 'Status', default='running')

	policy_line_ids = fields.One2many('international.policy.line','policy_line_id',string = "Policy Lines")

	@api.depends('policy_line_ids')
	def _compute_total_ship_onboard_value(self):
		for rec in self:
			if rec.policy_line_ids:
				total_ship_onboard_value = 0.00
				for line in rec.policy_line_ids:
					total_ship_onboard_value += line.ship_onboard_value
				rec.total_ship_onboard_value = total_ship_onboard_value
			else:
				rec.total_ship_onboard_value = 0.00

	@api.depends('policy_line_ids')
	def _compute_total_estimated_additional_charges_with_tax(self):
		for rec in self:
			if rec.policy_line_ids:
				total_estimated_additional_charges_with_tax = 0.00
				for line in rec.policy_line_ids:
					total_estimated_additional_charges_with_tax += estimated_additional_charges_with_tax
				rec.total_estimated_additional_charges_with_tax = total_estimated_additional_charges_with_tax
			else:
				rec.total_estimated_additional_charges_with_tax = 0.00

	@api.depends('policy_line_ids')
	def _compute_total_actual_additional_charges_with_tax(self):
		for rec in self:
			if rec.policy_line_ids:
				total_actual_additional_charges_with_tax = 0.00
				for line in rec.policy_line_ids:
					total_actual_additional_charges_with_tax += actual_additional_charges_with_tax
				rec.total_actual_additional_charges_with_tax = total_actual_additional_charges_with_tax
			else:
				rec.total_actual_additional_charges_with_tax = 0.00

	@api.depends('policy_amount','total_ship_onboard_value')
	def _compute_balance_amount(self):
		for rec in self:
			additional_charges = 0
			for policy_line in rec.policy_line_ids:
				ship_onboard_obj = self.env['ship.onboard'].search([('purchase_order_id', '=', policy_line.purchase_order_id.id)])
				if ship_onboard_obj:
					for ship_onboard_line in ship_onboard_obj.additional_charges_line_ids:
						if ship_onboard_line.actual_amount != 0.00:
							additional_charges += ship_onboard_line.actual_amount + ship_onboard_line.price_tax_actual
						else:
							additional_charges += ship_onboard_line.price_unit + ship_onboard_line.price_tax_estimate
				else:
					additional_charges = additional_charges

			rec.balance_amount = rec.policy_amount - (rec.total_ship_onboard_value + additional_charges)

class InternationalPolicyLine(models.Model):
	_name = "international.policy.line"

	purchase_order_id = fields.Many2one('purchase.order', string = "Purchase Order")
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	ship_onboard_value = fields.Monetary(string = 'Ship On-Board Value', currency_field='currency_id', compute='_compute_ship_onboard_value')
	
	estimated_additional_charges_with_tax = fields.Monetary(string = "Estimated Additional Charges", currency_field="currency_id", compute='_compute_estimated_additional_charges_with_tax')
	actual_additional_charges_with_tax = fields.Monetary(string = "Actual Additional Charges", currency_field="currency_id", compute='_compute_actual_additional_charges_with_tax')

	policy_line_id = fields.Many2one('international.policy', string = 'International Policy Ref')

	@api.depends('purchase_order_id')
	def _compute_ship_onboard_value(self):
		for rec in self:
			ship_onboard_obj = self.env['ship.onboard'].search([('purchase_order_id', '=', rec.purchase_order_id.id)])
			if ship_onboard_obj:
				rec.ship_onboard_value = ship_onboard_obj.total_ship_onboard_value
			else:
				rec.ship_onboard_value = 0.0


	@api.depends('purchase_order_id')
	def _compute_estimated_additional_charges_with_tax(self):
		for rec in self:
			ship_onboard_obj = self.env['ship.onboard'].search([('purchase_order_id', '=', rec.purchase_order_id.id)])
			estimated_additional_charges_with_tax = 0.0
			if ship_onboard_obj:
				rec.estimated_additional_charges_with_tax = ship_onboard_obj.total_estimated_additional_charges + ship_onboard_obj.total_estimated_tax_charges


	@api.depends('purchase_order_id')
	def _compute_actual_additional_charges_with_tax(self):
		for rec in self:
			ship_onboard_obj = self.env['ship.onboard'].search([('purchase_order_id', '=', rec.purchase_order_id.id)])
			actual_additional_charges_with_tax = 0.0
			if ship_onboard_obj:
				rec.actual_additional_charges_with_tax = ship_onboard_obj.total_actual_additional_charges + ship_onboard_obj.total_actual_tax_charges