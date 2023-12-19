from odoo import fields, models


class TourExpenses(models.Model):
    _name = 'tour.expenses.bill'
    _inherit = ['mail.thread','mail.activity.mixin']

    def current_employee(self):
        return self.env.user.employee_id

    e_name_tour = fields.Many2one('hr.employee', string='Employee Name', default=current_employee, ondelete='cascade',
                                     readonly=True, size=20)
    e_code_tour = fields.Char(related='e_name_tour.identification_id', string='Employee Code')
    designation_tour = fields.Char(related='e_name_tour.job_id.name', string='Designation')
    department_tour = fields.Char(related='e_name_tour.department_id.name')
    place_of_tour = fields.Char(string='Place of Tour')
    purpose_of_tour = fields.Char(string='Purpose of Tour')
    started_on = fields.Date(string='Started On')
    started_time = fields.Float(string='Time')
    returned_on = fields.Date('Returned On')
    returned_time = fields.Float(string='Time')
    tour_line_ids = fields.One2many('tour.expenses.bill.line', 'tour_detail_id')


class AddingDetails(models.Model):
    _name = 'tour.expenses.bill.line'

    tour_detail_id = fields.Many2one('tour.expenses.bill')
    date_tour = fields.Date(string='Date')
    dep_time = fields.Float(string='Dep. Time')
    place_from = fields.Char(string='Place From')
    place_to = fields.Char(string='Place To')
    arrival_time = fields.Float(string='Arrival Time')
    mode_of_travel = fields.Char(string='Mode Of Travel')
    fare_tour = fields.Float(string='Fare Rs.')
    local_tour = fields.Float(string='Local Conv. Rs.')
    living_tour = fields.Float(string='Living Expenses Rs.')


