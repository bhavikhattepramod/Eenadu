from odoo import api, fields, models


class CategoryDiscount(models.Model):
    _name = 'category.discount'

    name = fields.Char('Name')
    category_type = fields.Selection([('repetitive', 'Repetitive'),
                                      ('non_repetitive', 'Non-Repetitive')])
    max_discount = fields.Integer('Maximum Discount')
