from odoo import models, fields, api
from datetime import datetime

class ApprenticeshipResignRelieving(models.TransientModel):
    _name = 'apprenticeship.resign.relieving'

    name_id = fields.Many2one('', string='Name', required=True)
    date = fields.Date(string="Date", default=fields.Datetime.now(), date_format="%dd/%mm/%yyyy")

    def action_print_report(self):
        data = {
            # 'nomination': self.read()[0],
        }
        return self.env.ref('employee_life_cycle.confirmation_order_report_action').report_action(self,data=data)