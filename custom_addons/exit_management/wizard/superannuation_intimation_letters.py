from odoo import models, fields, api
from datetime import datetime


class SuperannuationIntimationLetter(models.TransientModel):
    _name = "superannuation.intimation.letter"

    name_id = fields.Many2one('hr.employee', string='Employee Name')
    resignation_id=fields.Many2one('hr.resignation', string="Name")
    company_id=fields.Many2one('res.company', default='USHODAYA ENTERPRISES PRIVATE LIMITED')
    current_date=fields.Date(string="Current date", default=fields.Date.today())


    def superannuation_intimation_letter_print(self):

        data = {

        }
        return self.env.ref('exit_management.report_superannuation_letter_wizards').report_action(self, data=data)
