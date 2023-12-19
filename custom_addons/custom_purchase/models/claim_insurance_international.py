from odoo import fields, models, api, _

class ClaimInternationalInsurance(models.Model):
	_name = 'claim.international.insurance'
	_rec_name = 'purchase_order_id'

	policy_number_id = fields.Many2one('international.policy', string = 'Policy Number')
	purchase_order_id = fields.Many2one('purchase.order', string = 'Purchase Order')
	vendor_partner_id = fields.Many2one('res.partner', string = 'Vendor')
	agent_partner_id = fields.Many2one('res.partner', string = 'Insurance Agent')
	state = fields.Selection([
		('new','New'),
		('waiting_for_claim','Waiting for Claim'),
		('claimed','Claimed'),], default = 'new', string = 'Status')

	claim_insurance_line_ids = fields.One2many('claim.international.insurance.line', 'claim_insurance_id', string = 'Claim Insurance Line')

	@api.onchange('policy_number_id')
	def onchange_agent_partner_id(self):
		if self.policy_number_id:
			self.agent_partner_id = self.policy_number_id.policy_provider_id.id

	def send_for_claim(self):
		self.state = 'waiting_for_claim'

	def approve_claim(self):
		self.state = 'claimed'

class ClaimInternationalInsurenceLine(models.Model):
	_name = 'claim.international.insurance.line'

	product_id = fields.Many2one('product.product', string = 'Product')
	product_qty = fields.Float('Quantity')
	product_uom_id = fields.Many2one('uom.uom')
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	unit_price = fields.Monetary(string = 'Unit Price', currency_field='currency_id')
	price_subtotal = fields.Monetary(string = 'Product Total', currency_field='currency_id', compute="_compute_price_subtotal")
	claim_amount = fields.Monetary(string = 'Claim Amount', currency_field='currency_id')
	claim_insurance_id = fields.Many2one('claim.international.insurance', string = 'Claim Insurance Ref')

	order_id = fields.Many2one('purchase.order', string = "Purchase order ref", related='claim_insurance_id.purchase_order_id')

	@api.onchange('product_id')
	def onchange_product_id(self):
		if self.product_id:
			self.product_uom_id = self.product_id.uom_id.id

	@api.depends('product_qty','unit_price')
	def _compute_price_subtotal(self):
		for rec in self:
			rec.price_subtotal = rec.product_qty * rec.unit_price

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