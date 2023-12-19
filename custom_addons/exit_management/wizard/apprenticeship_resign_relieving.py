from odoo import models, fields, api
from datetime import datetime

class ApprenticeshipResignRelieving(models.TransientModel):
    _name = 'apprenticeship.resign.relieving'

    name_id = fields.Many2one('hr.resignation', string='Name', required=True)
    date = fields.Date(string="Date", default=fields.Datetime.now(), date_format="%dd/%mm/%yyyy")

    def action_print_apprentice_resign_relieving(self):
        data = {
            # 'nomination': self.read()[0],
        }
        return self.env.ref('exit_management.apprenticeship_resign_relieving_action').report_action(self, data=data)

