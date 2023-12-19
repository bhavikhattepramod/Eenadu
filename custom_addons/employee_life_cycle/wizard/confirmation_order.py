from odoo import models, fields, api
from datetime import datetime

class ConfirmationOrderWizard(models.TransientModel):
    _name = 'confirmation.order.note.wizard'

    # employee_id = fields.Many2one('employee.life.cycle', string='Name', required=True)
    name_id = fields.Many2one('hr.employee', string='Name', required=True)
    date = fields.Date(string="Date", default=fields.Datetime.now(), date_format="%dd/%mm/%yyyy")

    # date_current = fields.Date(string="Date", default=date.today())

    def action_print_report(self):
        data = {
            # 'nomination': self.read()[0],
        }
        return self.env.ref('employee_life_cycle.confirmation_order_report_action').report_action(self,data=data)