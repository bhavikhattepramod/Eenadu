from odoo import fields, models


class HRdept(models.TransientModel):
    _name = 'hr.dept'

    # name_id = fields.Many2one('hr.employee', string="Name")
    names_id = fields.Many2one('hr.resignation', string="Name")
    current_date = fields.Date(string="Current Date", default=fields.Date.today())

    def invoice_print(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('exit_management.report_hrdept_wizards').report_action(self, data=data)