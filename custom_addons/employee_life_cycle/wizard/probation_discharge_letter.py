from odoo import models, fields, api
from datetime import datetime


class ProbationDischarge(models.TransientModel):
    _name = "probation.discharge.letter"

    name_id = fields.Many2one('employee.life.cycle', string='Employee Name')
    current_date=fields.Date(string="Current date", default=fields.Date.today())


    def probation_discharge_print(self):
        data = {

        }
        return self.env.ref('employee_life_cycle.probation_discharge_letter_wizards').report_action(self, data=data)
