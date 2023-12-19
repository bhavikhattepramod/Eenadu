from odoo import api, fields, models


class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    price_type = fields.Selection([
        ('fixed', 'Fixed'), 
        ('variable', 'Variable')],string="Price Type",default="variable")
    size = fields.Char(string="Size")
