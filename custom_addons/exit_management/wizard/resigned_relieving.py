from odoo import models, fields, api
from datetime import datetime, timedelta


class ResignedRelieving(models.TransientModel):
    _name = 'resigned.relieving'

    # name = fields.Many2one('hr.employee', string="Name")
    date = fields.Date(string="Date", default=fields.Date.today())
    name_id = fields.Many2one('hr.resignation', string="Name")


    # duration = fields.Integer(string='Duration (days)')
    #
    # @api.onchange('admin_date', 'end_date', 'duration')
    # def calculate_date(self)
    #     if self.admin_date and self.end_date:
    #         d1 = datetime.strptime(str(self.admin_date), '%Y-%m-%d')
    #         d2 = datetime.strptime(str(self.end_date), '%Y-%m-%d')
    #         d3 = d2 - d1
    #         self.duration = str(d3.days + 1)

    def action_print_report(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('exit_management.report_resigned_relieving').report_action(self, data=data)
