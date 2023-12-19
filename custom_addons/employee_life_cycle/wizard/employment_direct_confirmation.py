from odoo import models, fields, api


class PhysicalReport(models.TransientModel):
    _name = 'employment.confirmation'

    name = fields.Many2one('hr.employee', string="Name")
    current_date=fields.Date(string="Current Date",default=fields.Date.today())

    def invoice_print(self):

        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('employee_life_cycle.report_letter_confirmation_wizards').report_action(self, data=data)
