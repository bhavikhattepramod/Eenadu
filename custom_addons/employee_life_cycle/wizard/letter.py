from odoo import models, fields, api


class EmployeeLetter(models.TransientModel):
    _name = 'employee.letter'

    name = fields.Many2one('employee.life.cycle', string="Name")
    date = fields.Date(string="Date", default=fields.Date.today())

    def action_print_report(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('employee_life_cycle.report_employment_wizards').report_action(self, data=data)
