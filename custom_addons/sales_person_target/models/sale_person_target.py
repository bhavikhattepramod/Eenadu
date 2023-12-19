from odoo import fields, models, api, _

class SalesPersonTarget(models.Model):
	_name = 'sales.person.target'
	_rec_name = 'partner_id'

	partner_id = fields.Many2one('res.partner',string="Agent")
	target_scheme_id = fields.Many2one('target.scheme', string='Scheme')

	is_reta_target = fields.Boolean('Is Reta Target?')
	is_classifieds_target = fields.Boolean('Is Classifieds Target?')

	target_type = fields.Selection([
		('sales','Release Order'),
		('product','Products')
		], default='sales', string='Target Type')

	date_from = fields.Date('From Date')
	date_to = fields.Date('To Date')

	product_target_line_ids = fields.One2many('product.target.line', 'product_target_line_id', string="Product Target Line")
	so_targer_line_ids = fields.One2many('so.target.line', 'so_targer_line_id', string="Sale Order Target Line Ref")

	@api.onchange('target_scheme_id')
	def onchange_target_scheme_id(self):
		product_lines = []
		for line in self.target_scheme_id.scheme_product_line_ids:
			product_lines.append((0,0, {
					'product_id' : line.product_id.id,
					'target_amount' : 0.00
				}))
		self.product_target_line_ids.unlink()
		self.product_target_line_ids = product_lines

class ProductTargetLine(models.Model):
	_name = 'product.target.line'

	product_target_line_id = fields.Many2one('sales.person.target', string="Sales Person Target Ref")
	product_id = fields.Many2one('product.product', string="Product")
	target_amount = fields.Float('Target Amount')
	achieved_amount = fields.Float('Achieved Amount', compute='compute_achieved_amount')
	to_be_achieved = fields.Char('Target to be Achieved', compute='compute_to_be_achieved')
	parent_partner_id = fields.Many2one('res.partner', string="Agent Ref")
	parent_is_reta_target = fields.Boolean('Is Reta Target ref?')
	parent_is_classifieds_target = fields.Boolean('Is Classifieds Target ref?')

	@api.depends('target_amount','achieved_amount')
	def compute_to_be_achieved(self):
		for rec in self:
			if rec.target_amount > rec.achieved_amount:
				rec.to_be_achieved = rec.target_amount - rec.achieved_amount
			else:
				rec.to_be_achieved = 'Target Acheived'

	@api.depends('product_id')
	def compute_achieved_amount(self):
		for rec in self:
			sale_orders_obj = self.env['sale.order'].search([
				('agent_name', '=', rec.product_target_line_id.partner_id.id),
				('state', 'in', ('sale','print','done')),
				# ('date_order', '<=', rec.product_target_line_id.date_from),
				# ('date_order', '>=', rec.product_target_line_id.date_to)
				])
			if sale_orders_obj:
				so_product_value = 0.00
				for order in sale_orders_obj:
					if rec.product_target_line_id.is_reta_target:
						for reta_line in order.reta_order_line:
							if rec.product_id.id == reta_line.product_id.id:
								so_product_value += reta_line.price_subtotal
							else:
								so_product_value = so_product_value
					elif rec.product_target_line_id.is_classifieds_target:
						for classifieds_line in order.classified_order_line:
							if rec.product_id.id == classifieds_line.product_id.id:
								so_product_value += classifieds_line.price_subtotal
							else:
								so_product_value = so_product_value
					else:
						so_product_value = so_product_value
				rec.achieved_amount = so_product_value
			else:
				rec.achieved_amount = 0.00

class SaleOrderTargetLine(models.Model):
	_name = 'so.target.line'

	parent_target_type = fields.Selection([
		('sales','Release Order'),
		('product','Products')
		],string='Parent Target Type')
	target_amount = fields.Float('Target Amount')
	so_total_amount = fields.Float('Ro Total Amount', compute='_compute_so_total_amount')
	achieved_amount = fields.Float('Achieved Amount', compute='_compute_acheived_amount')
	to_be_achieved = fields.Char('Target to be Achieved', compute='compute_to_be_achieved')
	so_targer_line_id = fields.Many2one('sales.person.target', string='Sale Person Target ref')


	@api.depends('target_amount','achieved_amount')
	def compute_to_be_achieved(self):
		for rec in self:
			if rec.target_amount > rec.achieved_amount:
				rec.to_be_achieved = rec.target_amount - rec.achieved_amount
			else:
				rec.to_be_achieved = 'Target Acheived'

	@api.depends('target_amount')
	def _compute_so_total_amount(self):
		for rec in self:
			sale_orders_obj = self.env['sale.order'].search([
				('agent_name', '=', rec.so_targer_line_id.partner_id.id),
				('state', 'in', ('sale','print','done')),
				('date_order', '<=', rec.so_targer_line_id.date_from),
				('date_order', '>=', rec.so_targer_line_id.date_to)
				])
			if sale_orders_obj:
				so_total_amount = 0.00
				for order in sale_orders_obj:
					so_total_amount += order.amount_total
				rec.so_total_amount = so_total_amount
			else:
				rec.so_total_amount = 0.00

	@api.depends('target_amount')
	def _compute_acheived_amount(self):
		for rec in self:
			sale_orders_obj = self.env['sale.order'].search([
				('agent_name', '=', rec.so_targer_line_id.partner_id.id),
				('state', 'in', ('sale','print','done')),
				('date_order', '<=', rec.so_targer_line_id.date_from),
				('date_order', '>=', rec.so_targer_line_id.date_to)
				])
			if sale_orders_obj:
				achieved_amount = 0.00
				for order in sale_orders_obj:
					achieved_amount += order.cio_paid_amount
				rec.achieved_amount = achieved_amount
			else:
				rec.achieved_amount = 0.00
