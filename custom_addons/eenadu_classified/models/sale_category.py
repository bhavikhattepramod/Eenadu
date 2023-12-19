from odoo import api, fields, models


class SaleCategory(models.Model):
    _name = 'sale.category'

    name = fields.Char('Name')
    parent_category = fields.Many2one('sale.category', 'Parent category')
