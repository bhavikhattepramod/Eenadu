from odoo import fields ,models ,api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    authorized_by = fields.Char(String="Authorize")

