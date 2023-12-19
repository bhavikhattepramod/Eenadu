from odoo import models, fields, api


class EmployeeLetter(models.TransientModel):
    _name = 'letter.of.employment.probationary'

    name_id = fields.Many2one('hr.employee', string="Name")
    date = fields.Date(string="Date", default=fields.Date.today())

    def action_print_report(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('employee_life_cycle.letter_of_employment_vi').report_action(self, data=data)
