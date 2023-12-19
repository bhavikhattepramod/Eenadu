from odoo import models, fields
from datetime import datetime


class EmployeeLifeCycle(models.TransientModel):
    _name = "life.cycle"

    names_id= fields.Many2one('employee.life.cycle', string='Employee Name')
    date = fields.Date(string='Date', default=fields.Date.today())

    def action_print_report(self):
        data = {
            # 'nomination': self.read()[0],
        }
        return self.env.ref('employee_life_cycle.life_cycle_report_action').report_action(self, data=data)


class ApplicationReport(models.TransientModel):
    _name = 'hrms.application'

    name = fields.Many2one('hr.employee', string="Name")
    current_date=fields.Date(string="Current Date",default=fields.Date.today())

    def report_print(self):

        data = {

        }
        return self.env.ref('employee_life_cycle.report_application_wizards').report_action(self, data=data)
