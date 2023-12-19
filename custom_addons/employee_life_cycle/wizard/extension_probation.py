from odoo import models, fields, api


class ExtensionReport(models.TransientModel):
    _name = 'extension.probation'

    current_date=fields.Date(string="Current Date",default=fields.Date.today())
    no_of_months = fields.Many2one('employee.life.cycle', string='Employee Code')

    def report_print(self):

        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('employee_life_cycle.report_probation_wizards').report_action(self, data=data)
