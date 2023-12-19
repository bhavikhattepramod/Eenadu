from odoo import fields, models
from datetime import datetime



class Service(models.TransientModel):
    _name = 'service.extensions'

    service_id = fields.Many2one('employee.life.cycle', string="Name")
    current_date = fields.Date(string="Date", default=fields.Datetime.now(), date_format="%dd/%mm/%yyyy")

    def invoice_print(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('employee_life_cycle.action_service_extension_wizards').report_action(self, data=data)
