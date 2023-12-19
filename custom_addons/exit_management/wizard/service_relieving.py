from odoo import models, fields, api


class ServiceRelieving(models.TransientModel):
    _name = 'service.relieving'

    # name = fields.Many2one('hr.employee', string="Name")
    date = fields.Date(string="Date", default=fields.Date.today())
    name_id = fields.Many2one('hr.resignation', string="Name")

    def action_print_report(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('exit_management.report_service_relieving').report_action(self, data=data)
