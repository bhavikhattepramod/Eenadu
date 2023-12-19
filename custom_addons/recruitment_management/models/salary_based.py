from odoo import fields ,models ,api


class Applicant(models.Model):
    _inherit = 'hr.applicant'

    cur_date = fields.Date(string='Date', default=fields.Date.today())
