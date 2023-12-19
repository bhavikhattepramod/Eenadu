from odoo import fields, models, api, _

class DomesticPolicy(models.Model):
	_name = "domestic.policy"

	name = fields.Char('Policy Number')
	policy_provider_id = fields.Many2one('res.partner', string = 'Policy Provider')
	policy_start_date = fields.Date('Policy Start Date')
	policy_end_date = fields.Date('Policy End Date')
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	policy_amount = fields.Monetary(string = 'Policy Amount', currency_field='currency_id')
	total_shipment_value = fields.Monetary(string = 'Shipment Value', currency_field='currency_id', compute='_compute_total_shipment_value')
	balance_amount = fields.Monetary(string = 'Balance', currency_field='currency_id', compute='_compute_domestic_policy_balance_amount')
	state = fields.Selection([
		('running','Running'),
		('expired','Expired')
		], string = 'Status', default='running')

	domestic_policy_line_ids = fields.One2many('domestic.policy.line','domestic_policy_line_id',string = "Policy Lines")

	@api.depends('domestic_policy_line_ids')
	def _compute_total_shipment_value(self):
		for rec in self:
			if rec.domestic_policy_line_ids:
				total_shipment_value = 0.00
				for line in rec.domestic_policy_line_ids:
					total_shipment_value += line.shipment_value
				rec.total_shipment_value = total_shipment_value
			else:
				rec.total_shipment_value = 0.00

	@api.depends('policy_amount','total_shipment_value')
	def _compute_domestic_policy_balance_amount(self):
		for rec in self:
			rec.balance_amount = rec.policy_amount - rec.total_shipment_value

class DomesticPolicyLine(models.Model):
	_name = "domestic.policy.line"

	delivery_challan_no_id = fields.Many2one('distribute.shipments', string = "Delivery Challan No")
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	shipment_value = fields.Monetary(string = 'Shipment Value', currency_field='currency_id', compute='_compute_shipment_value')
	domestic_policy_line_id = fields.Many2one('domestic.policy', string = 'Domestic Policy Ref')

	@api.depends('delivery_challan_no_id')
	def _compute_shipment_value(self):
		for rec in self:
			shipment_obj = self.env['distribute.shipments'].search([('id', '=', rec.delivery_challan_no_id.id)])
			if shipment_obj:
				rec.shipment_value = shipment_obj.total_shipment_value
			else:
				rec.shipment_value = 0.0