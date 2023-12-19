from odoo import fields, models, api, _


class AdvertisementPosition(models.Model):
    _name = 'advertisement.position'

    name = fields.Char('Position Name')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    base_price = fields.Monetary('Amount', currency_field='currency_id')