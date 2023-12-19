from odoo import models, fields, api


class SuperannuationRelieving(models.TransientModel):
    _name = "superannuation.relieving"

    # name_id = fields.Many2one('hr.employee', string='Name')
    date_cur = fields.Date(string='Date', default=fields.Date.today())
    joining_date_id = fields.Many2one('hr.resignation', string='Name')

    def action_print_relieving(self):
        data = {
            # 'nomination': self.read()[0],
        }
        return self.env.ref('exit_management.superannuation_report_action').report_action(self, data=data)
