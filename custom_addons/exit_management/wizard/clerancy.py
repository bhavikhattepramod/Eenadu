from odoo import models, fields, api


class EmployeeLetter(models.TransientModel):
    _name = 'clearance_certificates.exit'


    date = fields.Date(string="Date", default=fields.Date.today())
    name_id=fields.Many2one('hr.resignation',string="Name", required=True)

    def action_print_report(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('exit_management.clerancy_cerficate_exit_hr').report_action(self, data=data)

