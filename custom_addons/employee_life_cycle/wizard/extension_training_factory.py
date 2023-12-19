from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime,timedelta

class EmployeeLetter(models.TransientModel):
    _name = 'extension.of.training.factory'

    name_id = fields.Many2one('hr.employee', string="Name")
    names_id = fields.Many2one('employee.life.cycle', string="Name")
    date = fields.Date(string="Date", default=fields.Date.today())
    date_from_join = fields.Date(string='Date from Join', compute='_compute_date_from_join', store=True)
    six_months_from_given = fields.Date('Six Months from Given Date', compute='_compute_six_months_from_given', store=True)

    def action_print_report(self):
        data = {
        }
        return self.env.ref('employee_life_cycle.extension_training_factory_form').report_action(self, data=data)


    @api.depends('name_id')
    def _compute_date_from_join(self):
        for record in self:
            if record.name_id:
                record.date_from_join = record.name_id.date_join
            else:
                record.date_from_join = False

    @api.depends('date_from_join')
    def _compute_six_months_from_given(self):
        for record in self:
            if record.date_from_join:
                six_months = record.date_from_join + relativedelta(months=6)
                record.six_months_from_given = six_months
            else:
                record.six_months_from_given = False