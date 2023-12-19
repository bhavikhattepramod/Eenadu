import calendar

from odoo import api, fields, models, _
from datetime import date, datetime,timedelta
# from num2words import num2words
# from odoo.tools.misc import formatLang
# from dateutil.relativedelta import relativedelta
# from odoo.tools.misc import format_date


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    basic_salary = fields.Float("Basic Salary")
    hra = fields.Float("HRA")
    standard_deduction = fields.Float("Standard Deduction")
    lta = fields.Float("LTA")
    special_allowance = fields.Float("Special Allowance")
    variable_allowance = fields.Float("Variable Allowance")
    pf_amount = fields.Float("PF (Employer's Contribution)")

    #other deductions & allowances
    food_coupon_ded = fields.Float("Food Coupon (Deduction)")
    income_tax = fields.Float("Income Tax")
    surcharge = fields.Float("Surcharge")
    cess = fields.Float("Cess")
    hr_deduction = fields.Float("HR Deductions")
    other_deductions = fields.Float("Other Deductions")
    food_coupon_alw = fields.Float("Food Coupon (Allowance)")
    onsite_allowance = fields.Float("Onsite Allowance")
    shift_allowance = fields.Float("Shift Allowance")
    other_allowance = fields.Float("Other Allowance")
    bonus = fields.Float("Bonus")
    ex_gratia = fields.Float("Ex-Gratia")
    income_tax_total = fields.Float("IT total",compute="compute_income_tax")

    #working & leave days
    total_days = fields.Float("Total Days", compute="get_total_number_of_days")
    paid_days = fields.Float("Paid Days")
    salary_days = fields.Float("Salary Days")
    leave_days = fields.Float("Leave Days", compute="get_total_leave_days")
    unpaid_days = fields.Float('Loss Of Pay (Days)')
    weekend_days = fields.Float("Weekend / Holiday Days", compute='_compute_num_weekdays')
    public_leave_days = fields.Float('Public Holidays')
    present_days = fields.Float("Present Days")
    number_of_days = fields.Integer(string="Number of days present")
    ot_hours = fields.Float(string='OT Hours')
    ot_amount = fields.Float(string='OT Amount')
    lop_arrear_field = fields.Float(string='LoP Arrears')
    lop_arrear_total_amount = fields.Float(string='LoP Arrear Amount')
    hop_days = fields.Float(string="HOP days")
    nsa_days = fields.Float(string="NSA Days")


    # for getting the week off day of the employee
    @api.depends('date_from', 'date_to','employee_id.week_off_day')
    def _compute_num_weekdays(self):
        for payslip in self:
            if payslip.date_from and payslip.date_to and payslip.employee_id.week_off_day:
                # Calculate the number of occurrences of the selected week off day between from_date and to_date
                weekday_num = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
                week_off_day = payslip.employee_id.week_off_day

                if week_off_day in weekday_num:
                    num_selected_weekday = 0
                    current_date = payslip.date_from
                    while current_date <= payslip.date_to:
                        if current_date.weekday() == weekday_num[week_off_day]:
                            num_selected_weekday += 1
                        current_date += timedelta(days=1)
                    payslip.weekend_days = num_selected_weekday
                else:
                    payslip.weekend_days = 0
            else:
                payslip.weekend_days = 0


    # For getting the no of working days of his contract month
    @api.onchange('employee_id')
    def value_days(self):
        for rec in self:
            get_date = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
            for val in get_date:
                print(val.date_join, 'Date Join')
                if val and val.date_join and rec.date_from and rec.date_to:
                    if rec.date_from < get_date.date_join < rec.date_to:
                        date_value_field = (rec.date_to - val.date_join).days + 1
                        rec.number_of_days = date_value_field
                        # print(date_value_field, 'Days')
                        # print('Found')
                    else:
                        print('Not Found')
                else:
                    print('Invalid data')
        # get_date = self.env['hr.employee'].search([('identification_id', '=', self.employee_id.identification_id)])
        # print(get_date.date_join, 'Date Join')
        # if self.date_from < get_date.date_join < self.date_to:
        #     print(self.date_to, 'To date')
        #     date_value_field = (self.date_to - get_date.date_join).days + 1
        #     self.number_of_days = date_value_field
        #     print(date_value_field, 'Days')
        #     print('Found')
        # else:
        #     print('Not Found')

    def compute_income_tax(self):
        for rec in self:
            rec.income_tax_total = rec.income_tax + rec.surcharge + rec.cess

    # @api.onchange('employee_id')
    # @api.depends('employee_id')
    # def calculate_salary_details(self):
    #     # employee = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
    #     if self.struct_id.name == 'Intership Stipend':
    #         basic = self.employee_id.total_ctc
    #         self.write({'basic_salary': round(basic),
    #                     'hra': 0.00,
    #                     'standard_deduction': 0.00,
    #                     'lta': 0.00,
    #                     'special_allowance': 0.00,
    #                     'variable_allowance': 0.00,
    #                     'pf_amount': 0.0
    #                     })
    #     else:
    #         total_ctc = self.employee_id.total_ctc
    #         mbo = self.employee_id.mbo
    #         mbo = mbo / 100
    #         base_salary = round(total_ctc - (total_ctc*mbo))
    #         lta = 0
    #         var_alw = 0
    #         if base_salary <= 400000.00:
    #             basic = 180000.00
    #             lta = 0
    #         elif base_salary > 400000.00 and base_salary <= 700000.00:
    #             basic = base_salary * 0.5
    #             lta = 18000
    #         elif base_salary > 700000 and base_salary <= 1200000:
    #             basic = base_salary * 0.45
    #             lta = 24000
    #         elif base_salary > 1200000:
    #             basic = base_salary * 0.45
    #             lta = 42000
    #         if basic:
    #             if base_salary <= 300000:
    #                 hra = 0
    #             elif base_salary > 300000:
    #                 hra = basic * 0.4
    #         if base_salary > 400000.00:
    #             std_ded = 50000
    #         else:
    #             std_ded = 0
    #         if basic/12 > 15000:
    #             pf = 1800*12        # employee = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
    #
    #         else:
    #             pf = (basic/12 * 0.12)*12
    #         # fca = self.food_coupon_alw
    #         spl_alw = base_salary - (basic + hra + std_ded + lta + pf)   # + fca)
    #         var_alw = total_ctc * mbo
    #         self.write({'basic_salary': round(basic),
    #                     'hra': round(hra),
    #                     'standard_deduction': round(std_ded),
    #                     'lta': round(lta),
    #                     'special_allowance': round(spl_alw),
    #                     'variable_allowance': round(var_alw),
    #                     'pf_amount': round(pf)})

    # def calculating_for_income_tax(self):
    #     for rec in self:
    #         print(len(self.search([('employee_id', '=', rec.employee_id.id)])))


    def compute_sheet(self):
        for rec in self:
            # rec.calculate_salary_details()
            rec.get_total_leave_days()
            rec.value_days()
            # rec.calculating_for_income_tax()
            super(HrPayslip, rec).compute_sheet()
        return

    @api.onchange('employee_id', 'date_from', 'date_to')
    @api.depends('date_from', 'date_to')
    def get_total_leave_days(self):
        date_from = self.date_from
        date_to = self.date_to
        days = lop_days = leave_days = sal_days = new_days = 0
        emp = self.employee_id
        start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
        end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
        days = (end_date - start_date).days + 1
        new_days = days
        if emp.first_contract_date:
            if self.date_to > emp.first_contract_date > self.date_from:
                join_date = str(emp.first_contract_date)
                join_date = datetime.strptime(join_date, "%Y-%m-%d")
                start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
                end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
                days = (end_date - start_date).days + 1
                new_days = (end_date - join_date).days + 1
                sal_days = days - new_days
        if emp.relieving_date:
            if self.date_from <= emp.relieving_date <= self.date_to:
                relieve_date = str(emp.relieving_date)
                relieve_date = datetime.strptime(relieve_date, "%Y-%m-%d")
                start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
                end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
                days = (end_date - start_date).days + 1
                new_days = (relieve_date - start_date).days + 1
                sal_days = days - new_days
            if self.date_from > emp.relieving_date:
                new_days = 0
        self.with_user(2).write({
            'paid_days': new_days,
            'salary_days': sal_days,
        })
        emp_id = self.employee_id.id
        emp_public_state = self.employee_id.state_id_emp
        holiday_obj = self.env['resource.calendar.leaves']
        public_holidays = holiday_obj.search([('resource_id', '=', False)])
        for val in public_holidays:
            # if val.work_entry_type_id.code == 'PUBLIC':
            start_date = val.date_from.date()
            end_date = val.date_to.date()
            if start_date >= date_from and end_date <= date_to and val.state_id.id == emp_public_state.id:
                holiday_obj |= val
        self.with_user(2).write({
            'public_leave_days': len(holiday_obj.ids),
        })
        type_ids = self.env['hr.leave.type'].search([]).ids
        recs = self.env['hr.leave'].search([('employee_id', '=', emp_id), ('state', '=', 'validate'),
                                            ('holiday_status_id', 'in', type_ids),
                                            ('request_date_from', '>=', date_from),
                                            ('request_date_to', '<=', date_to)])
        for rec in recs:
            leave_days += rec.number_of_days
        self.with_user(2).write({
            'leave_days': leave_days,
        })
        type_id = self.env['hr.leave.type'].search([('name', '=', 'Unpaid Leave')])
        # recs = self.env['hr.leave'].search([('employee_id', '=', emp_id), ('state', '=', 'validate'),
        #                                     ('holiday_status_id', '=', type_id.id),
        #                                     ('request_date_from', '>=', date_from),
        #                                     ('request_date_to', '<=', date_to)])
        # for rec in recs:
        #     lop_days += rec.number_of_days
        # self.with_user(2).write({
        #     'unpaid_days': lop_days,
        # })

    @api.onchange('date_from', 'date_to')  # added on 20-april
    @api.depends('date_from', 'date_to')
    def get_total_number_of_days(self):
        date_from = str(self.date_from)
        date_to = str(self.date_to)
        start_date = datetime.strptime(date_from, "%Y-%m-%d")
        end_date = datetime.strptime(date_to, "%Y-%m-%d")
        days = (end_date - start_date).days + 1
        self.with_user(2).write({
            'total_days': days,
        })
        sun = 0
        sat = 0
        dates_btwn = start_date
        while dates_btwn <= end_date:
            if (dates_btwn.strftime("%A") == 'Sunday'):
                sun += 1
            else:
                sun += 0
            if (dates_btwn.strftime("%A") == 'Saturday'):
                sat += 1
            else:
                sat += 0
            dates_btwn = dates_btwn + timedelta(days=1)
        self.with_user(2).write({
            'present_days': self.total_days - (self.weekend_days + self.leave_days + self.public_leave_days + self.unpaid_days),
        })


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar.leaves'

    state_id = fields.Many2one('res.country.state', string='State')



