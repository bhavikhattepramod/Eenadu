from odoo import api, fields, models


class INSRegion(models.Model):
    _name = 'ins.region'

    name = fields.Char('Name')
