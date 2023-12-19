from odoo import fields, models


class Apprenticeship(models.TransientModel):
    _name = 'letter.apprenticeship'

    name = fields.Many2one('hr.employee', string="Name")
    service_id = fields.Many2one('hr.employee', string="Name")
    current_date = fields.Date(string="Current Date", default=fields.Date.today())

    def invoice_print(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('employee_life_cycle.report_letter_wizards').report_action(self, data=data)