from datetime import timedelta

from odoo import fields, models, _, api, exceptions


class Hrsetting(models.Model):
    _inherit = 'hr.employee'

    gen_sub_cat = fields.Many2one('general.sub.category', string="General Sub Category")
    probation_date = fields.Date(string='Probation Date')
    emp_category = fields.Selection(selection_add=[('machine', 'Machine-Elec'),('resigned','Resigned'),('staff','Staff Reporters'),('photographer','Photographers'),
                                                   ('trainee','Trainee'),('apprentice','Apprentice'),('regular','Regular')])



class Generalcategory(models.Model):
    _name = 'general.category'

    name = fields.Char(string="Category Name")


class Generalcategory(models.Model):
    _name = 'general.sub.category'

    name = fields.Char(string='Work Category Name')


class HrLeaveAllocationLeave(models.Model):
    _inherit = 'hr.leave.allocation'

    # holiday_type = fields.Selection(selection_add=[('category_leave', 'By Employee Category')], ondelete={ 'category_leave': 'cascade'})
    general_category_leave = fields.Many2one('general.category', string='General Category')
    work_category_leave = fields.Selection([('confirmed', 'Confirmed'),('in_provisional_period', 'Probation'),
                                            ('trainee','Trainee')], string='Work Category')

    # @api.onchange('general_category_leave','work_category_leave')
    # def onchange_mode(self):
    #     employees = self.env['hr.employee'].search([])
    #     for rec in self:
    #         for emp in employees:
    #             if rec.general_category_leave.id and rec.work_category_leave:
    #                 if rec.general_category_leave.id == emp.emp_cat.id and rec.work_category_leave == 'trainee':
    #                     print(emp.emp_cat.id, 'success',rec.general_category_leave.id )
    #                 elif rec.general_category_leave.id == emp.emp_cat.id and rec.work_category_leave == 'in_provisional_period':
    #                     print(emp.emp_cat.id, 'success',rec.general_category_leave.id )
    #                 elif rec.general_category_leave.id == emp.emp_cat.id and rec.work_category_leave == 'confirmed':
    #                     print(emp.emp_cat.id, 'success', rec.general_category_leave.id)
    #             else:
    #                 print('failed')

    @api.onchange('general_category_leave','work_category_leave')
    @api.depends('holiday_type')
    def _compute_from_holiday_type(self):
        # l = ['Earned Leave', 'Sick Leave']
        default_employee_ids = self.env['hr.employee'].browse(self.env.context.get('default_employee_id')) or self.env.user.employee_id
        print(default_employee_ids, 'default_employee_ids')
        print(self.env.user.employee_id,'self.env.user.employee_id')
        for allocation in self:
            employees = self.env['hr.employee'].search([('emp_cat', '=',allocation.general_category_leave.id ),('emp_category','=', allocation.work_category_leave)])
            print(employees, 'employees1')
            emp_only_cl_time = self.env['hr.employee'].search([('emp_category','=', 'trainee')])
            emp_only_all_time = self.env['hr.employee'].search([('emp_category','!=', 'trainee')])
            print(emp_only_cl_time,'emp_only_cl_time1')
            print(emp_only_all_time,'emp_only_all_time1')
            for emp in employees:
                print(emp.emp_cat.name,'categories', emp.emp_category)
                if allocation.holiday_type == 'employee':
                        # if allocation.holiday_status_id.name in l:
                    if not allocation.employee_ids or allocation.employee_ids:
                        allocation.employee_ids = employees
                        allocation.mode_company_id = False
                        allocation.category_id = False
                elif allocation.holiday_type == 'company':
                    allocation.employee_ids = False
                    if not allocation.mode_company_id:
                        allocation.mode_company_id = self.env.company
                    allocation.category_id = False
                elif allocation.holiday_type == 'department':
                    allocation.employee_ids = False
                    allocation.mode_company_id = False
                    allocation.category_id = False
                elif allocation.holiday_type == 'category':
                    allocation.employee_ids = False
                    allocation.mode_company_id = False
                else:
                    allocation.employee_ids = default_employee_ids

    @api.onchange('work_category_leave')
    def onchange_work(self):
        for rec in self:
            if rec.work_category_leave == 'trainee':
                id = self.env['hr.leave.type'].search([('code', '=', 'CL')])
                print(id.ids)
                # return rec.holiday_status_id
                return {'domain': {'holiday_status_id': [('id', 'in', id.ids)]}}


class HrLeaveCond(models.Model):
    _inherit = 'hr.leave'

    contact_mobile_leave = fields.Char(string='Contact Phone')
    contact_leave_address = fields.Char(string='Contract Address')
    # state = fields.Selection(selection_add=[('cancel','Cancel')])

    @api.onchange('date_to')
    def compute_leave_phone(self):
        self.contact_mobile_leave = self.env.user.employee_id.work_phone

    @api.onchange('holiday_status_id')
    def not_sl_for_esi(self):
        if self.env.user.employee_id.esi_applicable_check_box:
            if self.holiday_status_id.code == 'SL':
                raise models.UserError('Sick Leave is Not Applicable')

    # @api.depends('number_of_days')
    # def _compute_number_of_days_display(self):
    #     leave_sandwich = self.env['hr.leave.type'].search([])
    #     leave_holiday = self.env['resource.calendar.leaves'].search([])
    #     res = super(HrLeaveCond, self)._compute_number_of_da
    #     ys_display()
    #     if self.env.user.employee_id.emp_cat.name == 'Journalists':
    #         for rec in self:
    #             for pub_hol in leave_holiday:
    #                 for rule in leave_sandwich:
    #                     if rule.sandwich_rule == True and rec.holiday_status_id.name == 'Casual Leave':
    #                         if rec.request_date_from < pub_hol.date_from.date() and rec.request_date_to > pub_hol.date_to.date():
    #                             print('ppppppppp')
    #                             rec.number_of_days_display = (rec.request_date_to - rec.request_date_from).days + 1
    #     return res

    @api.onchange('date_to')
    def onchange_leave_sl(self):
        if self.holiday_status_id.code == 'SL':
            if self.number_of_days < self.holiday_status_id.min_days:
                raise models.ValidationError('Minimum Half day should take.')

    @api.onchange('date_to')
    def onchange_leave_cl(self):
        if self.holiday_status_id.code == 'CL':
            if self.number_of_days < self.holiday_status_id.min_days:
                raise models.ValidationError('Minimum Half day should take.')

    @api.onchange('date_to')
    def onchange_leave_el(self):
        if self.holiday_status_id.code == 'EL':
            if self.number_of_days < self.holiday_status_id.min_days:
                raise models.ValidationError('Minimum Half day should take.')


    @api.depends('date_from', 'date_to', 'employee_id')
    def _compute_number_of_days(self):
        # leave_sandwich = self.env['hr.leave.type'].search([])
        if self.env.user.employee_id.emp_cat.name == 'Journalists':
            for holiday in self:
                if holiday.holiday_status_id.sandwich_rule == True and holiday.holiday_status_id.code == 'CL':
                    if holiday.date_from and holiday.date_to:
                        number_of_days_data = holiday._get_number_of_days(holiday.date_from, holiday.date_to,holiday.employee_id.id)
                        public_holidays = holiday.env['resource.calendar.leaves'].search([('date_from', '>=', holiday.date_from),('date_to', '<=', holiday.date_to)])
                        for public_holiday in public_holidays:
                            if public_holiday.date_from != holiday.date_from and public_holiday.date_to != holiday.date_to:
                                number_of_days_data['days'] += 1
                        holiday.number_of_days = number_of_days_data['days']
                    else:
                        holiday.number_of_days = 0
                elif holiday.holiday_status_id.sandwich_rule == False:
                    return super(HrLeaveCond,self)._compute_number_of_days()

    @api.onchange('date_from', 'date_to', 'holiday_status_id')
    def _check_leave_sequence(self):
        for leave in self:
            if leave.holiday_status_id.code in ['SL', 'EL']:
                yesterday = leave.date_from - timedelta(days=1)
                previous_leave = self.search([('employee_id', '=', leave.employee_id.id),('date_from', '=', yesterday),('holiday_status_id.code', '=', 'CL')])
                if previous_leave:
                    raise exceptions.ValidationError("You cannot apply earned leave immediately after casual leave.")


class HrLeaveTypeIn(models.Model):
    _inherit = 'hr.leave.type'

    # work_emp_leave = fields.Selection([('casual', 'Casual Leave'), ('earned', 'Earned Leave'),('compensatory', 'Compensatory Off Days'),
    #                                         ('sick', 'Sick Leave')], string='Work Category')
    sandwich_rule = fields.Boolean(string='Sandwich Rule Applicable')
    min_days = fields.Float(string='Minimum Days')
    max_days = fields.Float(string='Maximum Days')

    # @api.onchange('work_emp_leave')
    # def selected_leave(self):
    #     for record in self:
    #         if record.work_emp_leave:
    #             record.name = dict(self._fields['work_emp_leave'].selection).get(record.work_emp_leave)
    #         else:
    #             record.selected_leave = False



