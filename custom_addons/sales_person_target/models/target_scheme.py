from odoo import fields, models, api, _

class TargetScheme(models.Model):
	_name = 'target.scheme'

	name = fields.Char('Scheme Name')
	is_reta_scheme = fields.Boolean('Is Reta Scheme?')
	is_classifieds_scheme = fields.Boolean('Is Classifieds Scheme?')

	scheme_product_line_ids = fields.One2many('target.scheme.line','scheme_product_line_id', string="Product Lines")


class TargetSchemeLine(models.Model):
	_name = 'target.scheme.line'

	scheme_product_line_id = fields.Many2one('target.scheme', string='Target Scheme Ref')
	product_id = fields.Many2one('product.product', string="Product")
	product_uom_id = fields.Many2one('uom.uom', string="UoM")

	@api.onchange('product_id')
	def onchange_product_id(self):
		if self.product_id:
			self.product_uom_id = self.product_id.uom_id.id