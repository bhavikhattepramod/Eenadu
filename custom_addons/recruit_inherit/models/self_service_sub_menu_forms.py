from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class SelfserviceOndutyForm(models.Model):
    _name = 'self.service.application.details'
    _rec_name = 'e_name'

    def current_employee(self):
        return self.env.user.employee_id

    e_name = fields.Many2one('hr.employee','Employee Name' , default=current_employee, readonly=True, size=20)
    e_code = fields.Char(related='e_name.identification_id')
    designation_onduty = fields.Char(related='e_name.job_id.name')
    department_onduty = fields.Char(related='e_name.department_id.name')
    section_onduty_emp = fields.Many2many(related='e_name.section_name_hr')
    place_onduty = fields.Many2many(related='e_name.unit_name_hr',string='Place')
    day_type =fields.Selection([('full day','Full Day'),('1st half','1st Half'),('2nd half','2nd Half')])
    duty_from_date = fields.Date(string='Duty From')
    duty_to_date = fields.Date(string='Duty To')
    duty_days = fields.Integer(string='Duty Days')
    place_of_on_duty = fields.Text(string='Place Of On Duty')
    duty_from_time = fields.Float(string='Duty From Time')
    duty_to_time = fields.Float(string='Duty To Time')
    duty_purpose = fields.Char(string='Purpose')
    duty_hours = fields.Float(string='Hours',compute='_compute_duty_hours', store=True)
    status = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('reject', 'Rejected')], string='Status', default='draft')

    def action_submit(self):
        self.status = 'submitted'

    def action_cancel(self):
        self.status = 'draft'


    @api.depends('duty_from_time', 'duty_to_time')
    def _compute_duty_hours(self):
        for record in self:
            if record.duty_from_time and record.duty_to_time:
                # Calculate the number of hours
                duty_hours = record.duty_to_time - record.duty_from_time
                record.duty_hours = duty_hours


class ShiftChangesForm(models.Model):
    _name = 'shift.changes.form'
    _rec_name = 'e_name_shift'

    def current_employee(self):
        return self.env.user.employee_id

    e_name_shift = fields.Many2one('hr.employee','Employee Name' , default=current_employee, ondelete='cascade',readonly=True, size=20)
    e_code_shift = fields.Char(related='e_name_shift.identification_id')
    designation_shift = fields.Char(related='e_name_shift.job_id.name')
    department_shift = fields.Char(related='e_name_shift.department_id.name')
    section_shift_emp = fields.Many2many(related='e_name_shift.section_name_hr')
    place_shift = fields.Many2many(related='e_name_shift.unit_name_hr',string='Place')
    current_shift = fields.Many2one(related='e_name_shift.emp_time_id', string='Current Shift')
    shift_from_date = fields.Date(string='Shift From Date')
    shift_to_date = fields.Date(string='Shift To Date')
    shift_days = fields.Integer(string='Shift Days', compute='_compute_shift_days', store=True)
    new_shift = fields.Many2one('shift.management', string='New Shift')
    shift_reason = fields.Text(string='Reason')
    shift_note_field = fields.Text(string='Note',
                                   default='You should intimate & take prior approval from your HOD.Otherwise your application cannot be processed',
                                   readonly=True)
    status = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('reject', 'Rejected')], string='Status', default='draft')


    def action_submit_shift(self):
        self.status = 'submitted'


    def action_cancel_shift(self):
        self.status = 'draft'
    #
    @api.depends('shift_from_date', 'shift_to_date')
    def _compute_shift_days(self):
        for record in self:
            if record.shift_from_date and record.shift_to_date:
                # Calculate the number of days
                delta = record.shift_to_date - record.shift_from_date
                record.shift_days = delta.days + 1


class OnTourForm(models.Model):
    _name = 'on.tour.form'
    _rec_name = 'e_name_on_tour'

    def current_employee(self):
        return self.env.user.employee_id

    e_name_on_tour = fields.Many2one('hr.employee','Employee Name' , default=current_employee, ondelete='cascade',readonly=True, size=20)
    e_code_on_tour = fields.Char(related='e_name_on_tour.identification_id')
    designation_on_tour = fields.Char(related='e_name_on_tour.job_id.name')
    department_on_tour = fields.Char(related='e_name_on_tour.department_id.name')
    section_on_tour_emp = fields.Many2many(related='e_name_on_tour.section_name_hr')
    place_on_tour = fields.Many2many(related='e_name_on_tour.unit_name_hr',string='Place')
    instructed_by = fields.Char(string='Instructed By')
    tour_place = fields.Char(string='Tour Place')
    tour_starts_from = fields.Selection([('1st half','1st Half'),('2nd half','2nd Half')])
    tour_ends_on = fields.Selection([('1st half','1st Half'),('2nd half','2nd Half')])
    on_tour_from_time = fields.Float(string='Time From')
    on_tour_from_date = fields.Date(string='Tour From Date')
    on_tour_to_date = fields.Date(string='Tour To Date')
    on_tour_days = fields.Integer(string='Tour Days', compute='_compute_tour_days', store=True)
    purpose = fields.Text(string='Purpose')
    advance_amount = fields.Float(string='Advance Amount')
    amount_in_words = fields.Char(string='Amount In Words')
    on_tour_note_field = fields.Text(string='Note',
                                   default='You should intimate & take prior approval from your HOD.Otherwise your application cannot be processed',
                                   readonly=True)
    status = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('reject', 'Rejected')], string='Status', default='draft')

    def action_submit_tour(self):
        self.status = 'submitted'

    def action_cancel_tour(self):
        self.status = 'draft'

    @api.depends('on_tour_from_date', 'on_tour_to_date')
    def _compute_tour_days(self):
        for record in self:
            if record.on_tour_from_date and record.on_tour_to_date:
                # Calculate the number of days
                delta = record.on_tour_to_date - record.on_tour_from_date
                record.on_tour_days = delta.days + 1


class AuthorisationForm(models.Model):
    _name = 'authorisation.form'
    _rec_name = 'e_name_auth'

    def current_employee(self):
        return self.env.user.employee_id

    e_name_auth = fields.Many2one('hr.employee', 'Employee Name', default=current_employee, ondelete='cascade',
                                     readonly=True, size=20)
    e_code_auth = fields.Char(related='e_name_auth.identification_id')
    designation_auth = fields.Char(related='e_name_auth.job_id.name')
    department_auth = fields.Char(related='e_name_auth.department_id.name')
    section_auth_emp = fields.Many2many(related='e_name_auth.section_name_hr')
    place_auth = fields.Many2many(related='e_name_auth.unit_name_hr', string='Place')
    auth_note_field = fields.Text(string='Note',
                                     default='You should intimate & take prior approval from your HOD.Otherwise your application cannot be processed',
                                     readonly=True)
    status = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('reject', 'Rejected')], string='Status', default='draft')
    type_of_leave = fields.Selection([('weekly off','Weekly Off'),('extra hours','Extra Hours'),('public holidays','Public Holidays')])
    availed_type = fields.Selection([('comp off','COMP OFF')])
    auth_from_date = fields.Date(string='From Date')
    auth_to_date = fields.Date(string='To Date')
    auth_duty_days = fields.Integer(string='Duty Days')
    auth_shift = fields.Many2one('shift.management', string='Shift')
    hours_from = fields.Float(string='Hours From')
    hours_to = fields.Float(string='Hours To')
    hours = fields.Float(string='Hours',compute='_compute_auth_hours',store=True)
    auth_purpose  = fields.Text(string='Purpose')

    @api.depends('hours_from', 'hours_to')
    def _compute_auth_hours(self, _logger=None):
        for record in self:
            if record.hours_from and record.hours_to:
                auth_hours = record.hours_to - record.hours_from
                record.hours = auth_hours
                # _logger.info(f"Computed hours for record {record.id}: {auth_hours}")

    def action_submit_auth(self):
        self.status = 'submitted'

    def action_cancel_auth(self):
        self.status = 'draft'


class RectificationForm(models.Model):
    _name = 'rectification.form'
    _rec_name = 'e_name_rect'

    def current_employee(self):
        return self.env.user.employee_id

    e_name_rect = fields.Many2one('hr.employee', 'Employee Name', default=current_employee, ondelete='cascade',
                                     readonly=True, size=20)
    e_code_rect = fields.Char(related='e_name_rect.identification_id')
    designation_rect = fields.Char(related='e_name_rect.job_id.name')
    department_rect = fields.Char(related='e_name_rect.department_id.name')
    section_rect_emp = fields.Many2many(related='e_name_rect.section_name_hr')
    place_rect = fields.Many2many(related='e_name_rect.unit_name_hr', string='Place')
    rect_note_field = fields.Text(string='Note',
                                     default='You should intimate & take prior approval from your HOD.Otherwise your application cannot be processed',
                                     readonly=True)
    status = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('reject', 'Rejected')], string='Status', default='draft')
    day_type = fields.Selection([('full day','Full Day'),('1st half','1st Half'),('2nd half','2nd Half')])
    rect_reasons = fields.Selection([('forgot to punch','FORGOT TO PUNCH'),('company vehicle break down','COMPANY VEHICLE BREAK DOWN')],string='Reason')
    date = fields.Date(string='Date')
    rect_remarks = fields.Text(string='Remarks')

    def action_submit_rect(self):
        self.status = 'submitted'

    def action_cancel_rect(self):
        self.status = 'draft'


class LTAForm(models.Model):
    _name = 'lta.form'
    _rec_name = 'e_name_lta'

    def current_employee(self):
        return self.env.user.employee_id

    e_name_lta = fields.Many2one('hr.employee', 'Employee Name', default=current_employee, ondelete='cascade',
                                  readonly=True, size=20)
    e_code_lta = fields.Char(related='e_name_lta.identification_id')
    designation_lta = fields.Char(related='e_name_lta.job_id.name')
    department_lta = fields.Char(related='e_name_lta.department_id.name')
    section_lta_emp = fields.Many2many(related='e_name_lta.section_name_hr')
    place_lta = fields.Many2many(related='e_name_lta.unit_name_hr', string='Place')
    lta_note_field = fields.Text(string='Note',
                                  default='You should intimate & take prior approval from your HOD.Otherwise your application cannot be processed',
                                  readonly=True)
    status = fields.Selection([('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('reject', 'Rejected')], string='Status', default='draft')
    lta_place = fields.Char(string='LTA Place(s)')
    lta_tour_from = fields.Date(string='Tour From')
    lta_tour_to = fields.Date(string='Tour To')
    lta_tour_days = fields.Integer(string='Tour Days',compute='_compute_lta_tour_days',store=True)
    leave_ids = fields.One2many('employee.leave.record', 'employee_leave_id', string="Leave Records")
    lta_amount = fields.Float(string='LTA Amount')
    lta_amount_words =fields.Char(string='Amount In Words')
    lta_el_balance = fields.Float(string='EL Balance')
    lta_family_details = fields.One2many('employee.leave.record','employee_leave_id',string='Family Details')
    spouse_elgiblity = fields.Selection([('my spouse is not working','My Spouse is not working'),('my spouse is working and is not elgible for lta','My Spouse is working and is not elgible for LTA')])
    ack_lta = fields.Boolean()
    ack_default = fields.Text(string='def', default='I will submit the proof of journey,accommodation and hotel bills along with LTA expenses statement within 7 days after return from my tour',readonly=True )

    @api.model
    def create(self, vals):
        if 'ack_default' not in vals:
            vals[
                'ack_default'] = 'I will submit the proof of journey, accommodation, and hotel bills along with LTA expenses statement within 7 days after return from my tour'
        return super(LTAForm, self).create(vals)

    @api.depends('lta_tour_from', 'lta_tour_to')
    def _compute_lta_tour_days(self):
        for record in self:
            if record.lta_tour_from and record.lta_tour_to:
                # Calculate the number of days
                delta = record.lta_tour_to - record.lta_tour_from
                record.lta_tour_days = delta.days + 1

    @api.depends('employee_id')
    def _compute_ltc_el_field(self):
        for record in self:
            # Fetch the data from hr.leave.allocation where holiday_status_id is "Earned Leaves"
            leave_allocation = self.env['hr.leave.allocation'].search([
                ('holiday_status_id', '=', 'Earned Leaves'),
                ('employee_id', '=', record.employee_id.id)  # Filter by the current employee
            ])

            total_days = sum(leave.number_of_days_display for leave in leave_allocation)
            record.lta_el_balance_el = total_days



    @api.onchange('lta_amount')
    def el_balance(self):
        el = self.env['hr.leave'].search([('employee_id','=',self.env.user.employee_id.id)])
        for rec in el:
            print(rec.holiday_status_id,'holiday')
            print(rec.holiday_status_id.name,'holiday name')
            if rec.holiday_status_id.code == self.leave_ids.leave_type == 'EL':
                self.lta_el_balance = rec.holiday_status_id.remaining_leaves
                print(self.lta_el_balance,'lta balance')

    def action_submit_lta(self):
        self.status = 'submitted'

    def action_cancel_lta(self):
        self.status = 'draft'

    @api.constrains('ack_lta')
    def _check_ack_lta(self):
        # for record in self:
        if not self.ack_lta:
            raise ValidationError("please acknowledging LTA condition form.")


class EmployeeLeaveRecord(models.Model):
    _name = "employee.leave.record"
    _description = "Employee Leave Record"

    date = fields.Date(string="Date")
    leave_type = fields.Selection([
        ('vacation', 'Vacation'),
        ('SL', 'Sick Leave'),
        ('unpaid', 'Unpaid Leave'),
        ('EL','Earned Leaves')

        # Add other leave types here
    ], string="Leave Type")
    # lta_opt = fields.Char()
    lta_relation = fields.Char(string='Relation')
    lta_name = fields.Char(string='Name')
    lta_age = fields.Integer(string='Age')
    employee_leave_id = fields.Many2one('lta.form', string="Employee Leave")


