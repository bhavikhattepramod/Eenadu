from odoo import fields, models, api, _

class ClaimDomesticInsurance(models.Model):
	_name = 'claim.domestic.insurance'
	_rec_name = 'delivery_challan_no_id'

	policy_number_id = fields.Many2one('domestic.policy', string = 'Policy Number')
	delivery_challan_no_id = fields.Many2one('distribute.shipments', string = 'Delivery Challan No')
	vendor_partner_id = fields.Many2one('res.partner', string = 'Vendor')
	agent_partner_id = fields.Many2one('res.partner', string = 'Insurance Agent')
	state = fields.Selection([
		('new','New'),
		('waiting_for_claim','Waiting for Claim'),
		('claimed','Claimed'),], default = 'new', string = 'Status')

	claim_insurance_line_ids = fields.One2many('claim.domestic.insurance.line', 'claim_insurance_id', string = 'Claim Insurance Line')

	@api.onchange('policy_number_id')
	def onchange_agent_partner_id(self):
		if self.policy_number_id:
			self.agent_partner_id = self.policy_number_id.policy_provider_id.id

	def send_for_claim(self):
		self.state = 'waiting_for_claim'

	def approve_claim(self):
		self.state = 'claimed'

	@api.model
	def create(self, vals):
		if vals.get('delivery_challan_no_id'):
			domestic_policy_obj = self.env['domestic.policy'].search([('state', '=', 'running')])
			if domestic_policy_obj:
				dc_count = 0
				for line in domestic_policy_obj.domestic_policy_line_ids:
					if line.delivery_challan_no_id.id == vals.get('delivery_challan_no_id'):
						dc_count += 1
					else:
						dc_count = dc_count
				if dc_count == 0:
					policy_line_list = []
					policy_line_list.append([0, 0, {
						'delivery_challan_no_id': int(vals.get('delivery_challan_no_id')),
						'domestic_policy_line_id': domestic_policy_obj,
						}])
					domestic_policy_obj.domestic_policy_line_ids = policy_line_list

		res = super(ClaimDomesticInsurance, self).create(vals)

		return res

class ClaimDomesticInsurenceLine(models.Model):
	_name = 'claim.domestic.insurance.line'

	product_id = fields.Many2one('product.product', string = 'Product')
	product_qty = fields.Float('Quantity')
	product_uom_id = fields.Many2one('uom.uom')
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	unit_price = fields.Monetary(string = 'Unit Price', currency_field='currency_id')
	price_subtotal = fields.Monetary(string = 'Product Total', currency_field='currency_id', compute="_compute_price_subtotal")
	claim_amount = fields.Monetary(string = 'Claim Amount', currency_field='currency_id')
	claim_insurance_id = fields.Many2one('claim.domestic.insurance', string = 'Claim Insurance Ref')

	@api.onchange('product_id')
	def onchange_product_id(self):
		if self.product_id:
			self.product_uom_id = self.product_id.uom_id.id

	@api.depends('product_qty','unit_price')
	def _compute_price_subtotal(self):
		for rec in self:
			rec.price_subtotal = rec.product_qty * rec.unit_price