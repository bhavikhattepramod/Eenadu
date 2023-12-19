from odoo import fields, models


class HRushodaya(models.TransientModel):
    _name = 'ushodaya.hr'

    names_id = fields.Many2one('hr.resignation', string="Name")
    current_date = fields.Date(string="Current Date", default=fields.Date.today())

    def invoice_print(self):
        data = {

        }
        return self.env.ref('exit_management.report_ushodaya_wizards').report_action(self, data=data)