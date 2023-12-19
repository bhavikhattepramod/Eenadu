from odoo import fields, api, models


class MultiDiscount(models.Model):
    _name = 'multi.discount'

    name = fields.Char('Name')
    discount = fields.Float('Discount')
    is_multi_region = fields.Boolean('Is Multi Region')
    is_multi_edition = fields.Boolean('Is Multi Edition')
    is_multi_zone = fields.Boolean('Is Multi Zone')
    second_hightest_discount = fields.Float('2nd Highest')
    third_hightest_discount = fields.Float('3nd Highest')
    sale_type = fields.Selection([
        ('main', 'Main'),
        ('mini', 'Mini'),
        # ('pellipandiri', 'Pellipandiri')
    ], string='Sale Type')

    @api.onchange('is_multi_region', 'is_multi_edition', 'is_multi_zone')
    def displaying_name(self):
        for rec in self:
            if rec.is_multi_region == True:
                rec.name = 'Multi Region'
            elif rec.is_multi_edition:
                rec.name = 'Multi Edition'
            elif rec.is_multi_zone == True:
                rec.name = 'Multi Zone'
