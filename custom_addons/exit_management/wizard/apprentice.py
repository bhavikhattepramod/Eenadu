from odoo import fields, models


class Apprenticeship(models.TransientModel):
    _name = 'apprenticeship.relieving'

    name = fields.Many2one('hr.resignation', string="Name")
    current_date = fields.Date(string="Current Date", default=fields.Date.today())

    def invoice_print(self):
        data = {
        }
        return self.env.ref('exit_management.report_forms_wizards').report_action(self, data=data)