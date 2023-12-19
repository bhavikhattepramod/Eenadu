from odoo import fields,models

class Companysettings(models.Model):
    _inherit = "res.company"

    retire_age = fields.Integer(string="Retirement Age")