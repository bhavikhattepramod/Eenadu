from odoo import api, fields, models


class Areas(models.Model):
    _name = 'area.area'

    name = fields.Char('Name')
    parent_name = fields.Many2one('area.area')
