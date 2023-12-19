from odoo import models, fields
from datetime import datetime


class TraineeDischarge(models.TransientModel):
    _name = "trainee.discharge"

    name_id= fields.Many2one('hr.resignation', string='Employee Name')
    cur_date=fields.Date(string="Current date",default=fields.date.today())

    def action_print_report(self):
        data = {
            # 'nomination': self.read()[0],
        }
        return self.env.ref('exit_management.trainee_discharge_report_action').report_action(self, data=data)
