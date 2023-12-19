from odoo import fields, models, api, _

class SaleDocumentType(models.Model):
    _name = 'sale.document.type'

    name = fields.Char('Name')