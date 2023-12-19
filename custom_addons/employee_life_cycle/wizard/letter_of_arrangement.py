from odoo import models, fields, api
from datetime import datetime


class LetterOfArragement(models.TransientModel):
    _name = "letter.arrangement"

    name_id = fields.Many2one('hr.employee', string='Employee Name')
    name = fields.Char(string="Name")
    current_date=fields.Date(string="Current date", default=fields.Date.today())


    def invoice_print(self):
        data = {

        }
        return self.env.ref('employee_life_cycle.report_letter_arrangement_wizards').report_action(self, data=data)
