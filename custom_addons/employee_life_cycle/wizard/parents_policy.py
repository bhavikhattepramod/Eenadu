from odoo import models, fields, api


class ParentsPolicy(models.TransientModel):
    _name = 'parents.policy'

    name = fields.Many2one('hr.employee', string="Name")
    date = fields.Date(string="Date", default=fields.Date.today())

    def action_print_report(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('employee_life_cycle.report_parents_policy_wizards').report_action(self, data=data)

