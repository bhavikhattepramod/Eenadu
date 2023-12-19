# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from odoo import api, Command, fields, models, _
from odoo.tools import float_round, date_utils, convert_file, html2plaintext
from odoo.tools.float_utils import float_compare
# from om_hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips, ResultRules
from dateutil import relativedelta as rdelta
from odoo.tools.misc import formatLang
from num2words import num2words
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_date



class HrResignation(models.Model):
    _name = 'hr.resignation'
    _inherit = 'mail.thread'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help='Name of the employee for whom the request is creating')
    date_of_resignation = fields.Date(string="Resignation Date",
                                      help='Date on which the request is confirmed by the employee.',
                                      track_visibility="always")
    resignation_type = fields.Many2one('hr.departure.reason', string="Resign For"
                                       )
    is_resigned = fields.Boolean(default=False)
    is_terminated = fields.Boolean(default=False)
    is_retired = fields.Boolean(default=False)
    is_absconded = fields.Boolean(default=False)
    is_others = fields.Boolean(default=False)
    reason = fields.Text(string="Reason", help='Specify reason for leaving the company')
    notice_period = fields.Integer(string="Notice Period (in Days)")
    notice_shortfall = fields.Integer(string="Notice Shortfall (Days)")
    company_notice_days = fields.Integer(string="Company Notice (Days)")
    state = fields.Selection(
        [('discussion', 'Manager Discussion'),
         ('rejected', 'Rejected'), ('accepted', 'Accepted'),
         ('processing', 'Processing'), ('done', 'Done')],
        string='Status', default='discussion', track_visibility="always")

    manager_feedback = fields.Text(string="Manager Feedback", help='Specify reason for leaving the company')
    exit_interview_feedback = fields.Text(string="Exit Interview Feedback",
                                          help='Specify reason for leaving the company')
    # exit_interview_feedback = fields.Many2one('survey.survey',string="Exit Interview Feedback", help='Specify reason for leaving the company')
    date_of_acceptance = fields.Date(string="Resignation Accepted On",
                                     help='Date on which the request is confirmed by the employee.',
                                     )
    date_of_relieving = fields.Date(string="Actual Relieving Date",
                                    help='Date of Relieving according to the company.',
                                    )
    emp_relieving_date = fields.Date(string="Last Working Day",
                                     help='Date on which the request is confirmed by the employee.',
                                     )
    date_of_settlement = fields.Date(string="Settlement Date",
                                     help='Date on which the request is confirmed by the employee.',
                                     )
    date_of_joining = fields.Date(string="Joining Date",
                                  help='Date on which the employee has joined the company.',
                                  )
    waive_off = fields.Boolean('Waive Off Notice Period')
    # structure = fields.Many2one('hr.payroll.structure')

    # other deductions & allowances
    food_coupon_ded = fields.Float("Food Coupon (Deduction)")
    income_tax = fields.Float("Income Tax")
    hr_deduction = fields.Float("HR Deductions")
    other_deductions = fields.Float("Other Deductions")
    food_coupon_alw = fields.Float("Food Coupon (Allowance)")
    onsite_allowance = fields.Float("Onsite Allowance")
    shift_allowance = fields.Float("Shift Allowance")
    other_allowance = fields.Float("Other Allowance")

    # working & leave days
    present_days = fields.Float("Present Days")
    leave_days = fields.Float("Leave Days", compute="get_total_leave_days")
    total_days = fields.Float("Total Days", compute="get_total_number_of_days")
    salary_days = fields.Float("Salary Days")
    paid_days = fields.Float("Paid Days")

    # master salry details
    basic_salary = fields.Float("Basic Salary")
    hra = fields.Float("HRA")
    standard_deduction = fields.Float("Standard Deduction")
    lta = fields.Float("LTA")
    special_allowance = fields.Float("Special Allowance")
    variable_allowance = fields.Float("Variable Allowance")
    pf_amount = fields.Float("PF (Employer's Contribution)")

    unpaid_days = fields.Float('Loss Of Pay (Days)')
    weekend_days = fields.Float("Weekend / Holiday Days")
    public_leave_days = fields.Float('Public Holidays')

    termination_date = fields.Date(string="Date Of Termination")
    retirement_date = fields.Date(string="Date Of Retirement")
    date_of_death = fields.Date(string="Date Of Death")
    date_of_absconding = fields.Date(string="Date Of Absconding")
    month_1 = fields.Float('Month 1 Amount')
    month_2 = fields.Float('Month 2 Amount')
    month_3 = fields.Float('Month 3 Amount')
    month_name_1 = fields.Char()
    month_name_2 = fields.Char()
    month_name_3 = fields.Char()
    compute_date = fields.Date('Computed On')
    pending_salary_days = fields.Float("Pending Salary Days")
    number = fields.Char(
        string='Reference', readonly=True, copy=False,
        states={'draft': [('readonly', False)], 'verify': [('readonly', False)]})
    date_from = fields.Date(
        string='From',
        default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
        # states={'draft': [('readonly', False)], 'verify': [('readonly', False)]}
    )
    date_to = fields.Date(
        string='To',
        default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()),
        # states={'draft': [('readonly', False)], 'verify': [('readonly', False)]}
    )
    company_id = fields.Many2one(
        'res.company', string='Company', copy=False, required=True,
        compute='_compute_company_id', store=True, readonly=False,
        default=lambda self: self.env.company,
        states={'draft': [('readonly', False)], 'verify': [('readonly', False)]})
    contract_id = fields.Many2one(
        'hr.contract', string='Contract', domain="[('company_id', '=', company_id)]",
        compute='_compute_contract_id', store=True, readonly=False,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)], 'paid': [('readonly', True)]})
    currency_id = fields.Many2one(related='contract_id.currency_id')
    line_ids = fields.One2many(
        'hr.resignation.line', 'slip_id', string='Hr Resignation Lines',
        compute='_compute_line_ids', store=True, readonly=True, copy=True,
        states={'discussion': [('readonly', False)], 'accepted': [('readonly', False)]})
    struct_id = fields.Many2one(
        'hr.payroll.structure', string='Structure',
        compute='_compute_struct_id', store=True, readonly=False,
        states={'accepted': [('readonly', False)], 'cancel': [('readonly', True)], 'paid': [('readonly', True)]},
        help='Defines the rules that have to be applied to this payslip, according '
             'to the contract chosen. If the contract is empty, this field isn\'t '
             'mandatory anymore and all the valid rules of the structures '
             'of the employee\'s contracts will be applied.')
    # struct_type_id = fields.Many2one('hr.payroll.structure.type', related='struct_id.type_id')
    # input_line_ids = fields.One2many(
    #     'hr.settlement.input', 'settlement_id', string='Settlement Inputs',
    #     compute='_compute_input_line_ids', store=True,
    #     readonly=False,
    #     states={'done': [('readonly', True)], 'cancel': [('readonly', True)], 'paid': [('readonly', True)]})
    leave_balance = fields.Float('Leave Balance')
    service_years = fields.Char('Years Of Service')
    years = fields.Float('Completed Years')
    calculate_gratuity = fields.Boolean('Calculate Gratuity')
    check = fields.Boolean(compute='_get_value')
    relieving_reference = fields.Char(string="Relieving Letter - Reference")
    experience_reference = fields.Char(string="Experience Letter - Reference")
    pending_total_days = fields.Integer(string="Pending Total Days")
    notice_tot = fields.Float(string='Notice Total',store=True)
    notice_tot_rec = fields.Float(string='Notice Total Recovery',store=True)
    total_gratuity = fields.Float(string='Total Gratuity',store=True)
    leave_sum = fields.Float(string='Total Leave Encashment',store=True)
    days_present = fields.Float(string='Number of days present',store=True)
    pf_emp_value_exit = fields.Float(store=True)
    pf_empr_value_exit = fields.Float(store=True)
    eps_emp_value_exit = fields.Float(store=True)

    esi_emp_value_exit = fields.Float(store=True)
    esi_empr_value_exit = fields.Float(store=True)
    pt_value_exit = fields.Float(store=True)
    lic_value_exit = fields.Float(store=True)
    # amount_da_exit = fields.Float(store=True)



    @api.depends('employee_id')
    def _get_value(self):
        if self.company_id.calculate_gratuity:
            self.check = True
            self.calculate_gratuity = True
        else:
            self.check = False
            self.calculate_gratuity = False
        # rec = self.env['survey.survey'].search([('title','='"Exit Interview Form - Exzatech")])

    @api.constrains('employee_id')
    def _check_emp_name(self):
        recs = self.search([('employee_id', '=', self.employee_id.id), ('id', '!=', self.id)])
        if recs:
            raise ValidationError("Employee already exists")

    # @api.depends('input_line_ids')
    def _compute_line_ids(self):
        if not self.env.context.get("payslip_no_recompute"):
            return
        for payslip in self.filtered(lambda p: p.line_ids and p.state in ['discussion', 'accepted']):
            payslip.line_ids = [(5, 0, 0)] + [(0, 0, line_vals) for line_vals in payslip._get_payslip_lines()]

    @api.depends('contract_id')
    def _compute_struct_id(self):
        for slip in self.filtered(lambda p: not p.struct_id):
            # slip.struct_id = slip.contract_id.structure_type_id.default_struct_id
            slip.struct_id = False

    @api.depends('employee_id')
    def _compute_company_id(self):
        for slip in self.filtered(lambda p: p.employee_id):
            slip.company_id = slip.employee_id.company_id

    @api.depends('employee_id', 'date_from', 'date_to')
    def _compute_contract_id(self):
        for slip in self:
            if not slip.employee_id or not slip.date_from or not slip.date_to:
                slip.contract_id = False
                continue
            # Add a default contract if not already defined or invalid
            if slip.contract_id and slip.employee_id == slip.contract_id.employee_id:
                continue
            contracts = slip.employee_id._get_contracts(slip.date_from, slip.date_to)
            slip.contract_id = contracts[0] if contracts else False

    def action_accept(self):
        if not self.emp_relieving_date:
            raise ValidationError("Please enter the Last Working Date")
        self.date_of_acceptance = date.today()
        self.state = 'accepted'

    def action_reject(self):
        self.state = 'rejected'

    def action_approval(self):
        self.date_of_settlement = date.today()
        self.state = 'done'

    def action_slip_processing(self):
        return self.write({'state': 'processing'})

    @api.onchange('employee_id')
    def get_pay_structure(self):
        emp_id = self.employee_id
        rec = self.env['hr.payroll.structure'].search([('name', '=', 'Journalists')])
        self.write({'struct_id': rec.id})
        if emp_id.first_contract_date:
            self.write({'date_of_joining': emp_id.first_contract_date})

    @api.onchange('resignation_type')
    @api.depends('resignation_type')
    def res_type(self):
        if self.resignation_type.name == 'Termination':
            self.write({'is_terminated': True,
                        'is_retired': False,
                        'is_resigned': False,
                        'is_others': False,
                        'is_absconded': False})
        elif self.resignation_type.name == 'Retirement':
            self.write({'is_terminated': False,
                        'is_retired': True,
                        'is_resigned': False,
                        'is_others': False,
                        'is_absconded': False})
        elif self.resignation_type.name == 'Resignation':
            self.write({'is_terminated': False,
                        'is_retired': False,
                        'is_resigned': True,
                        'is_others': False,
                        'is_absconded': False})
        elif self.resignation_type.name == 'Absconding':
            self.write({'is_absconded': True,
                        'is_terminated': False,
                        'is_retired': False,
                        'is_resigned': False,
                        'is_others': False})
        elif self.resignation_type.name == 'Death':
            self.write({'is_absconded': False,
                        'is_terminated': False,
                        'is_retired': False,
                        'is_resigned': False,
                        'is_others': True})

    @api.model
    def get_notice_days(self):
        return self.notice_shortfall

    @api.model
    def get_leave_balance(self):
        return self.leave_balance

    @api.onchange('employee_id', 'date_of_resignation', 'emp_relieving_date', 'termination_date', 'date_of_absconding',
                  'retirement_date', 'date_of_death')
    @api.depends('employee_id', 'date_of_resignation', 'emp_relieving_date', 'termination_date', 'date_of_absconding',
                 'retirement_date', 'date_of_death')
    def notice_days(self):
        notice_obj = self.env['notice.period.days']
        emp_id = self.employee_id
        days = 0
        if self.resignation_type.name == 'Absconding':
            if self.date_of_absconding:
                self.emp_relieving_date = self.date_of_absconding
        elif self.resignation_type.name == 'Retired':
            if self.retirement_date:
                self.emp_relieving_date = self.retirement_date
        elif self.resignation_type.name == 'Death':
            if self.date_of_death:
                self.emp_relieving_date = self.date_of_death
        if emp_id:
            recs = notice_obj.search([('employee_category', '=', self.employee_id.emp_category)])
            for rec in recs:
                if rec.employee_notice_days:
                    self.notice_period = rec.employee_notice_days
                    self.company_notice_days = rec.company_notice_days
                if self.resignation_type.name == 'Resignation':
                    if self.date_of_resignation:
                        self.date_of_relieving = ((self.date_of_resignation) + timedelta(days=self.notice_period))
                    if self.emp_relieving_date:
                        if self.emp_relieving_date < self.date_of_relieving:
                            diff = self.date_of_relieving - self.emp_relieving_date
                            self.notice_shortfall = diff.days
                        elif self.emp_relieving_date == self.date_of_relieving:
                            self.notice_shortfall = 0
                elif self.resignation_type.name == 'Termination':
                    if self.termination_date:
                        self.emp_relieving_date = self.termination_date

    def _get_payslip_lines(self, contract_ids=False, payslip_id=False):
        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            localdict['categories'].dict[category.code] = category.code in localdict['categories'].dict and \
                                                          localdict['categories'].dict[category.code] + amount or amount

            return localdict

        class BrowsableObject(object):
            def __init__(self, employee_id, dict, env):
                self.employee_id = employee_id
                self.dict = dict
                self.env = env

            def __getattr__(self, attr):
                return attr in self.dict and self.dict.__getitem__(attr) or 0.0

        class InputLine(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""
                    SELECT sum(amount) as sum
                    FROM hr_payslip as hp, hr_payslip_input as pi
                    WHERE hp.employee_id = %s AND hp.state = 'done'
                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                return self.env.cr.fetchone()[0] or 0.0

        class WorkedDays(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def _sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""
                    SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours
                    FROM hr_payslip as hp, hr_payslip_worked_days as pi
                    WHERE hp.employee_id = %s AND hp.state = 'done'
                    AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                return self.env.cr.fetchone()

            def sum(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[0] or 0.0

            def sum_hours(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[1] or 0.0

        class Payslips(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = fields.Date.today()
                self.env.cr.execute("""SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)
                            FROM hr_payslip as hp, hr_payslip_line as pl
                            WHERE hp.employee_id = %s AND hp.state = 'done'
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s""",
                                    (self.employee_id, from_date, to_date, code))
                res = self.env.cr.fetchone()
                return res and res[0] or 0.0

        # we keep a dict with the result because a value can be overwritten by another rule with the same code
        result_dict = {}
        rules_dict = {}
        worked_days_dict = {}
        inputs_dict = {}
        blacklist = []
        # payslip = self.env['hr.payslip'].browse(payslip_id)
        payslip = self.env['hr.resignation'].browse(payslip_id)

        # for worked_days_line in payslip.worked_days_line_ids:
        #     worked_days_dict[worked_days_line.code] = worked_days_line
        # for input_line in payslip.input_line_ids:
        #     inputs_dict[input_line.code] = input_line

        categories = BrowsableObject(payslip.employee_id.id, {}, self.env)
        inputs = InputLine(payslip.employee_id.id, inputs_dict, self.env)
        worked_days = WorkedDays(payslip.employee_id.id, worked_days_dict, self.env)
        payslips = Payslips(payslip.employee_id.id, payslip, self.env)
        rules = BrowsableObject(payslip.employee_id.id, rules_dict, self.env)

        baselocaldict = {'categories': categories, 'rules': rules, 'payslip': payslips, 'worked_days': worked_days,
                         'inputs': inputs}
        # get the ids of the structures on the contracts and their parent id as well
        contracts = self.env['hr.contract'].browse(contract_ids)
        if len(contracts) == 1 and payslip.struct_id:
            # structure_ids = list(set(payslip.struct_id._get_parent_structure().ids))
            structure_ids = self.struct_id.id
        else:
            structure_ids = contracts.get_all_structures()
        # get the rules of the structure and thier children
        rule_ids = self.env['hr.payroll.structure'].browse(structure_ids).get_all_rules()
        # run the rules by sequence
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x: x[1])]
        sorted_rules = self.env['hr.salary.rule'].browse(sorted_rule_ids)
        for contract in contracts:
            employee = contract.employee_id
            localdict = dict(baselocaldict, employee=employee, contract=contract)
            for rule in sorted_rules:
                # print(rule,payslip.salary_days,"Rule---------------------------------------")
                key = rule.code + '-' + str(contract.id)
                localdict['result'] = None
                localdict['result_qty'] = 1.0
                localdict['result_rate'] = 100
                # check if the rule can be applied
                if rule._satisfy_condition(localdict) and rule.id not in blacklist:
                    # compute the amount of the rule
                    amount, qty, rate = rule._compute_rule(localdict)
                    # check if there is already a rule computed with that code
                    previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                    # set/overwrite the amount computed for this rule in the localdict
                    tot_rule = contract.company_id.currency_id.round(amount * qty * rate / 100.0)
                    # print(tot_rule,amount,qty,rate,"RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
                    localdict[rule.code] = tot_rule
                    rules_dict[rule.code] = rule
                    # sum the amount for its salary category
                    localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                    # create/overwrite the rule in the temporary results
                    result_dict[key] = {
                        'salary_rule_id': rule.id,
                        # 'contract_id': contract.id,
                        'name': rule.name,
                        'code': rule.code,
                        'category_id': rule.category_id.id,
                        'sequence': rule.sequence,
                        'appears_on_payslip': rule.appears_on_payslip,
                        # 'condition_select': rule.condition_select,
                        # 'condition_python': rule.condition_python,
                        # 'condition_range': rule.condition_range,
                        # 'condition_range_min': rule.condition_range_min,
                        # 'condition_range_max': rule.condition_range_max,
                        'amount_select': rule.amount_select,
                        'amount_fix': rule.amount_fix,
                        # 'amount_python_compute': rule.amount_python_compute,
                        'amount_percentage': rule.amount_percentage,
                        # 'amount_percentage_base': rule.amount_percentage_base,
                        # 'register_id': rule.register_id.id,
                        'amount': amount,
                        'employee_id': contract.employee_id.id,
                        'quantity': qty,
                        'rate': rate,
                    }
                    print(result_dict,'result_dict')
                else:
                    # blacklist this rule and its children
                    blacklist += [id for id, seq in rule._recursive_search_of_rules()]

        return list(result_dict.values())
    #lic value

    def onchange_employee_insurance_exit(self):
        for rec in self:
            amount = self.env['insurance.policy'].search([('employee_code', '=', rec.employee_id.id)])
            rec.lic_value_exit = amount.total_sum_values




    ####calculating salary master in exit#####

    def prep_salary_master_exit(self):
        # Create a dictionary to store the salary_master values for each line
        salary_master_dict = {}
        vpay = 0.0
        for payslip in self:
            if not payslip.contract_id:
                continue

            contract = payslip.contract_id
            component_lines = contract.salary_rule_master

            for payslip_line in payslip.line_ids:
                code = payslip_line.code
                component = component_lines.filtered(lambda line: line.salary_code == code)

                if component:
                    # Store the salary_master value for each line in the dictionary
                    salary_master_dict[payslip_line.id] = component.salary_amount

        # After processing, set the salary_master values for each line from the dictionary
        for payslip_line in self.line_ids:
            if payslip_line.id in salary_master_dict:
                payslip_line.salary_master_exit = salary_master_dict[payslip_line.id]
            for payslip in self:
                contract = self.env['hr.contract'].search([('employee_id', '=', payslip.employee_id.id),
                                                           ('name', '=', payslip.contract_id.name)])
                cpi = self.env['cpi.points'].search([])
                # amount_da_field = self.env['hr.payslip'].search([('employee_id', '=', payslip.employee_id.id)])
                for da in contract:
                    for cpi_val in cpi:
                        for cpi_val_line in cpi_val.cpi_point_lines:

                            for line in payslip.line_ids:
                                for val in contract.salary_rule_master:
                                    if val.salary_code == 'BASIC':
                                        value = val.salary_amount
                                        if line.code == 'VPAY':
                                            vpay = line.salary_master_exit = round(value * 35 / 100)
                                        if line.code == 'DA' and not cpi_val_line.effective_date_to:
                                            da.amount_da = round((value / 189) * cpi_val_line.cpi_points_payroll)
                                            line.salary_master_exit = round(da.amount_da)
                                        if line.code == 'HRA':
                                            line.salary_master_exit = round((value + vpay) * 10 / 100)
                                        if line.code == 'TA':
                                            line.salary_master_exit = round((value + vpay) * 10 / 100)

    #calculate notice period

    @api.model
    def get_sum_notice_period(self):
        sum_notice_period = 0
        sum_cal_notice = 0
        total_val = self.env['hr.payslip'].search([])
        notice_per = self.env['hr.salary.rule'].search([])
        struct_notice_pr = self.env['hr.payroll.structure'].search([])
        for struct_sal in struct_notice_pr:
            for record in notice_per:
                var = self.env['hr.resignation.line'].search([('name', '=', record.name)])
                for val in var:
                    if self.struct_id.id == struct_sal.id:
                        if record.name == val.name:
                            val.company_notice_period_check = record.company_notice_period
                            print('notice')
        # for sum in total_val:
        for line in self.line_ids:
            if line.company_notice_period_check == True:
                print(f"Adding salary_master notice {line.salary_master_exit} for line: {line.name}")
                sum_notice_period += line.salary_master_exit
                sum_cal_notice = round(sum_notice_period / self.struct_id.structure_days) * self.company_notice_days
                # total_val.notice_period_amount = sum_cal_notice
                self.notice_tot = sum_cal_notice
                print(sum_notice_period,'sum notice period')
                print(sum_cal_notice,'sum cal notice')

        return self.notice_tot


  #get employee notice period recovery
    def notice_period_recover(self):
        sum_notice_period_recover = 0
        sum_cal_notice_recover = 0
        total_value_rec = self.env['hr.payslip'].search([])
        notice_per_rec = self.env['hr.salary.rule'].search([])
        struct_notice_pr_rec = self.env['hr.payroll.structure'].search([])
        for struct_sal in struct_notice_pr_rec:
            for record in notice_per_rec:
                var_rec = self.env['hr.resignation.line'].search([('name', '=', record.name)])
                for val in var_rec:
                    if self.struct_id.id == struct_sal.id:
                        if record.name == val.name:
                            val.employee_notice_period_check = record.employee_notice_period
                            print('notice rec')
        # for sum in total_val:
        for line in self.line_ids:
            if line.employee_notice_period_check == True:
                print(f"Adding salary_master recover {line.salary_master_exit} for line: {line.name}")
                sum_notice_period_recover += line.salary_master_exit
                sum_cal_notice_recover = round(sum_notice_period_recover / self.struct_id.structure_days) * self.notice_shortfall
                # total_val.notice_period_amount = sum_cal_notice
                self.notice_tot_rec = sum_cal_notice_recover
                print(sum_notice_period_recover, 'sum notice period recovery')
                print(sum_cal_notice_recover, 'sum cal notice recovery')
        return self.notice_tot_rec

#gratuity calculation
    def gratuity_calculation(self):
        sum_gratuity = 0
        sum_cal_gratuity = 0
        total_value_rec = self.env['hr.payslip'].search([])
        gratuity = self.env['hr.salary.rule'].search([])
        struct_gartuity = self.env['hr.payroll.structure'].search([])
        for struct_sal in struct_gartuity:
            for record in gratuity:
                var_rec = self.env['hr.resignation.line'].search([('name', '=', record.name)])
                for val in var_rec:
                    if self.struct_id.id == struct_sal.id:
                        if record.name == val.name:
                            val.gratuity_rule_check_exit = record.gratuity_rule_check
                            print('gratuity')
        # for sum in total_val:
        for line in self.line_ids:
            print(line.name,line.code,line.salary_master_exit,line.total, 'lineeeeeeeeeeeeeeeeeeeeeeee')
            if line.gratuity_rule_check_exit == True:
                if self.years >= 5:
                    print(f"Adding salary_master gratuity {line.salary_master_exit} for line: {line.name}")
                    sum_gratuity += line.salary_master_exit
                    sum_cal_gratuity = round((sum_gratuity) *  (15 / self.struct_id.structure_days) * self.years)
                    # total_val.notice_period_amount = sum_cal_notice
                    self.total_gratuity = sum_cal_gratuity
                    print(sum_gratuity, 'sum sum_gratuity period')
                    print(sum_cal_gratuity, 'sum cal gratuity')

        return self.total_gratuity

#leave encashment calculation

    def leave_encashment_calculation(self):
        sum_leave = 0
        sum_cal_gratuity = 0
        total_value_rec = self.env['hr.payslip'].search([])
        leave_encash = self.env['hr.salary.rule'].search([])
        struct_leave_en = self.env['hr.payroll.structure'].search([])
        for struct_sal in struct_leave_en:
            for record in leave_encash:
                var_rec = self.env['hr.resignation.line'].search([('name', '=', record.name)])
                for val in var_rec:
                    if self.struct_id.id == struct_sal.id:
                        if record.name == val.name:
                            val.leave_encashment_rule_check_exit = record.leave_encashment_rule_check
                            print('leave')
        # for sum in total_val:
        for line in self.line_ids:
            if line.leave_encashment_rule_check_exit == True:
                print(f"Adding salary_master leave {line.salary_master_exit} for line: {line.name}")
                sum_leave += line.salary_master_exit
                cal_leave_sum = round((sum_leave / self.struct_id.structure_days) * self.leave_balance)
                # total_val.notice_period_amount = sum_cal_notice
                self.leave_sum = cal_leave_sum
                print(sum_leave, 'sum leave')
                print(cal_leave_sum, 'sum cal leave sum')
        return self.leave_sum



# passing value of company notice and employee notice recovery

    def _compute_total(self):
        for line in self:
            res = self.env['hr.resignation.line'].search([])
            company_grauity = self.env['res.company'].search([])
            # gratuity_employee = self.env['hr.employee'].search([('name', '=', line.employee_id.id)])
            for value in res:
                for lines in line.line_ids:
                    for comp in company_grauity:
                        # for emp in gratuity_employee:
                        lines.total = float(lines.quantity) * lines.amount * lines.rate / 100
                        if lines.code == 'COMPNOTICE':
                            print('sss')
                            lines.total = line.notice_tot
                            print(lines.total, 'total')
                        if lines.code == 'EMPNOTICE':
                            print('employe')
                            lines.total = line.notice_tot_rec
                        print(lines.total, 'tot rec')
                        if comp.calculate_gratuity == True and line.employee_id.gratuity_employee_level == True and lines.code == 'GRAT':
                            lines.total = line.total_gratuity
                        if lines.code == 'LEAVENC':
                            print('employe')
                            lines.total = line.leave_sum
                        if lines.code == 'EPFEMP':
                            lines.total = line.pf_emp_value_exit
                        if lines.code == 'EPFEMPLR':
                            lines.total = line.pf_empr_value_exit
                        if lines.code == 'EPSEMPLR':
                            lines.total = line.eps_emp_value_exit
                        if lines.code == 'ESIEMP':
                            lines.total = line.esi_emp_value_exit
                        if lines.code == 'ESIEMPLR':
                            lines.total = line.esi_empr_value_exit
                        if lines.code == 'PT':
                            lines.total = line.pt_value_exit
                        if lines.code == 'LIC':
                            lines.total = line.lic_value_exit


    #pf calcultion
    def pf_calculation_exit(self):
        pf_exit = self.env['pf.esi.settings'].search([], limit=1)
        # esi_inherit = self.env['hr.payslip.line'].search([])
        pf_emp_contribution_exit = self.env['hr.salary.rule'].search([('name', '=', 'EPF Employee Contribution')])
        pf_empr_contribution_exit = self.env['hr.salary.rule'].search([('name', '=', 'EPF Employer Contribution')])
        eps_empr_contribution_exit = self.env['hr.salary.rule'].search([('name', '=', 'EPS Employer Contribution')])
        line_payroll_exit = self.env['hr.payroll.structure'].search([('name', '=', 'Journalists')])
        line_payroll_struct_exit = self.env['hr.payroll.structure'].search([])
        check_box_pf_exit = self.env['hr.employee'].search([])
        # print(pf_emp_contribution, line_payroll)

        record = self
        pf_not_value = 0.0
        for rec in record:
           for pf_struct in line_payroll_struct_exit:
                for rule in rec.struct_id.rule_ids:
                    for line in rec.line_ids:
                        line.structure_id_exit = rec.struct_id
                        if rule.name == line.name:
                            if rule.pf_applicable == True:
                                line.pf_cal_exit = True
                            # if rule.pf_compute == True:
                            #     line.pf_com = True

                    line_list = []
                    total = 0.0
                    for line_val in rec.line_ids:
                        if line_val.pf_cal_exit and line_val.code not in ['EPFEMP', 'EPFEMPLR', 'EPSEMPLR']:
                            line_list.append(line_val.total)

                    if len(line_list) != 0:
                        # esi_total = 0
                        for i in line_list:
                            print("DDDDDDDDDDDd", i)
                            total = total + i
                            print(total, 'hhhhhhhhhhh')
                            a = total * pf_exit.employee_contribution / 100
                            pf_emp_total = round(a)
                            b = total * pf_exit.employer_contribution / 100
                            pf_empr_total = round(b)
                            c = total * pf_exit.employee_pension_scheme / 100
                            eps_total = round(c)
                            # print(eps_total, 'wwwwwwwwwwwwwwwwww')

                        for vals in check_box_pf_exit:
                            pf_sal_limit = 0.0

                            if rec.employee_id.name == vals.name:
                                if vals.pf_applicable_check_box == True:
                                    if rec.struct_id.id == pf_struct.id:
                                        if pf_emp_contribution_exit and line_payroll_exit and eps_empr_contribution_exit and pf_empr_contribution_exit and pf_emp_contribution_exit.amount_select == 'code':
                                            if total > pf_exit.pf_salary_limit:
                                                epf_1 = (pf_exit.pf_salary_limit * pf_exit.employee_contribution) / 100
                                                emprpf_1 = (pf_exit.pf_salary_limit * pf_exit.employer_contribution) / 100
                                                eps_1 = (pf_exit.pf_salary_limit * pf_exit.employee_pension_scheme) / 100
                                                print(epf_1,emprpf_1,eps_1,'epfepseprmpf')
                                                x1 = round(epf_1)
                                                y1= round(emprpf_1)
                                                z1 = round(eps_1)
                                                print('x1y1z1')
                                                self.pf_emp_value_exit = x1
                                                self.pf_empr_value_exit = y1
                                                self.eps_emp_value_exit = z1
                                            elif total < pf_exit.pf_salary_limit:
                                                epf_2 = (total * pf_exit.employee_contribution) /100
                                                empr_2 = (total * pf_exit.employer_contribution) /100
                                                eps_2 = (total * pf_exit.employee_pension_scheme) /100
                                                if eps_2 < pf_exit.eps_limit:
                                                    x2 = round(epf_2)
                                                    y2 = round(empr_2)
                                                    z2 = round(eps_2)
                                                    print(x2,y2,z2,'x2y2z2')
                                                    self.pf_emp_value_exit = x2
                                                    self.pf_empr_value_exit = y2
                                                    self.eps_emp_value_exit = z2
                                            # elif total < 9999999:
                                                elif eps_2 >= pf_exit.eps_limit:
                                                    d = total * pf_exit.employee_pension_scheme / 100
                                                    pf_sal_limit = round(d)
                                                    e = (pf_sal_limit - pf_exit.eps_limit) + pf_empr_total
                                                    print(pf_sal_limit, pf_exit.eps_limit, pf_empr_total, 'calculationeps')
                                                    print(e, 'calculation eeeeeeee')
                                                    empr_total = round(e)
                                                    self.pf_emp_value_exit = pf_emp_total
                                                    self.pf_empr_value_exit = empr_total
                                                    self.eps_emp_value_exit = pf_exit.eps_limit

                                                    # print(pf_sal_limit,'ddlllllllloooopppplllllllllllllllllllllllllllllllllllllllllllllllllllllllllll')


                                else:
                                    self.pf_emp_value_exit = pf_not_value
                                    self.pf_empr_value_exit = pf_not_value
                                    self.eps_emp_value_exit = pf_not_value
                                    # pf_emp_contribution_exit.amount_python_compute = 'result = ' + str(pf_not_value)
                                    # pf_empr_contribution_exit.amount_python_compute = 'result = ' + str(pf_not_value)
                                    # eps_empr_contribution_exit.amount_python_compute = 'result = ' + str(pf_not_value)

        return self.pf_emp_value_exit,self.pf_empr_value_exit,self.eps_emp_value_exit


    #esi calculation exit management

    def esi_calculation_exit(self):
        esi_exit = self.env['pf.esi.settings'].search([], limit=1)
        # esi_inherit = self.env['hr.payslip.line'].search([])
        emp_contribution_exit = self.env['hr.salary.rule'].search([('name', '=', 'ESI Employee Contribution')])
        empr_contribution_exit = self.env['hr.salary.rule'].search([('name', '=', 'ESI Employer Contribution')])
        exe_payroll_exit = self.env['hr.payroll.structure'].search([('name', '=', 'Journalists')])
        esi_check_box = self.env['hr.employee'].search([])
        exe_payroll_struct = self.env['hr.payroll.structure'].search([])
        # print(emp_contribution, exe_payroll)

        record = self
        esi_not_value = 0.0
        esi_emp_total = 0.0
        esi_empr_total = 0.0
        for rec in record:
            for esi_struct in exe_payroll_struct:
                for rule in rec.struct_id.rule_ids:
                    for line in rec.line_ids:
                        line.structure_id_exit = rec.struct_id
                        # print(line.structure_id.name, "ggggggggggggggggg")
                        if rule.name == line.name:
                            if rule.esi_applicable == True:
                                line.esi_cal_exit = True
                                # print(line.esi_applicable, 'rrrrrrrr')
                            # if rule.esi_compute == True:
                            #     line.esi_com = True


                    line_list = []
                    total = 0.0
                    for line_val in rec.line_ids:
                        if line_val.esi_cal_exit and line_val.code not in ['ESIEMP', 'ESIEMPLR']:
                            line_list.append(line_val.total)
                            print(line_val,'linelist')

                    if len(line_list) != 0:
                        # esi_total = 0
                        for i in line_list:
                            print("DDDDDDDDDDDdesi", i)
                            total = total + i
                            print(total, 'hhhhhhhhhhhesi')
                            a = total * esi_exit.esi_employee_contribution / 100
                            esi_emp_total = round(a)
                            b = total * esi_exit.esi_employer_contribution / 100
                            esi_empr_total = round(b)
                        # print(total, "111111111111111111111111111")
                        # print(esi_emp_total, a, "88888888888888888888888888")
                        # print(esi_empr_total, b, "ooooooooooooooooooo")

                        for vals in esi_check_box:
                            if rec.employee_id.name == vals.name:
                                if vals.esi_applicable_check_box == True:
                                    if rec.struct_id.id == esi_struct.id:
                                        if emp_contribution_exit and exe_payroll_exit and empr_contribution_exit and emp_contribution_exit.amount_select == 'code':
                                            self.esi_emp_value_exit = esi_emp_total
                                            self.esi_empr_value_exit = esi_empr_total
                                            # print(emp_contribution.amount_python_compute, "llllllllllljjjjkkkk")
                                            # print(empr_contribution.amount_python_compute, "ddddddddddllllllllllljjjjkkkk")

                                else:
                                    self.esi_emp_value_exit = esi_not_value
                                    self.esi_empr_value_exit = esi_not_value
                                    # print(emp_contribution.amount_python_compute, "llllpooooooppppppppppppppp")
                                    # print(empr_contribution.amount_python_compute, "daaaaaaaaaaaaaaaaaaaadkkkk")

        return self.esi_emp_value_exit,self.esi_empr_value_exit

    # Getting the gross from the pre-processing payslip and  compare the gross state wise from that PT amount


    def get_gross_exit(self):
        for rec in self:
            state_val = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
            structure_emp = self.env['hr.payroll.structure'].search([])
            from_state = self.env['professional.tax'].search([('name', '=', state_val.state_id_emp.id)])
            # emp_pt = self.env['hr.salary.rule'].search([('code', '=', 'PT')])
            for struct in structure_emp:
                for amt in from_state.gross_line_ids:
                    if state_val.state_id_emp.id == from_state.name.id:
                        for val in rec.line_ids:
                            if val.name == 'Gross':
                                if amt.gross_min < val.total < amt.gross_max:
                                    # rec.pt_amount = amt.gross_value
                                    if rec.struct_id.id == struct.id:
                                        rec.pt_value_exit = amt.gross_value

            return rec.pt_value_exit

    def compute_sheet(self):
        self.new_compute_sheet()
        self.new_compute_sheet()
        self.new_compute_sheet()

    def new_compute_sheet(self):
        self.get_total_leave_days()
        self.get_total_number_of_days()
        self.check_pending_month_salary()
        self.check_pending_salary_days()
        self.calculate_no_years()
        self._compute_total()
        resignation_slip = self.filtered(lambda slip: slip.state in ['discussion', 'accepted', 'processing', 'done'])
        # Delete old payslip lines
        resignation_slip.line_ids.unlink()
        payslip = self.env['hr.payslip'].search([('employee_id', '=', self.employee_id.id)], order="id desc", limit=1)
        for slip in resignation_slip:
            number = slip.number or self.env['ir.sequence'].next_by_code('settlement.slip')
            if len(payslip) < 0:  # Reverse the condition
                lines = [(0, 0, line) for line in
                         slip._get_payslip_lines(contract_ids=slip.employee_id.contract_id.id,
                                                 payslip_id=slip.id)]
                print('compute after')  # Change the message to 'compute after'
            else:
                lines = [(0, 0, line) for line in
                         slip._get_payslip_lines(contract_ids=self.contract_id.id,
                                                 payslip_id=slip.id)]
                print(payslip.date_from, 'datefrom')  # Move this line here
                print('compute before')  # Change the message to 'compute before'
            slip.write({'line_ids': lines, 'number': number, 'state': 'accepted', 'compute_date': fields.Date.today()})
            self.state = 'processing'

        self.onchange_total_days_resignation()
        self.onchange_present_days_resignation()
        # self.onchange_lop_days_resignation()
        self.value_days_present_days()
        self.prep_salary_master_exit()
        self.pf_calculation_exit()
        self.esi_calculation_exit()
        self.get_sum_notice_period()
        self.notice_period_recover()
        self.gratuity_calculation()
        self.leave_encashment_calculation()
        self.get_gross_exit()
        self.onchange_employee_insurance_exit()
        self._compute_total()
        return True

    def onchange_total_days_resignation(self):
        structure = self.env['hr.payroll.structure'].search([('name','=','Journalists')])
        for rec in self:
            structure.structure_days = rec.total_days

    def onchange_present_days_resignation(self):
        record = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)])
        for rec in self:
            record.present_days_exit = rec.days_present

    #getting lop days in contract for DA calculation
    # def onchange_lop_days_resignation(self):
    #     rec = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id)])
    #     for days in self:
    #         rec.lop_days_exit = days.unpaid_days


    # @api.onchange('employee_id')
    # @api.depends('employee_id')
    # def calculate_salary_details(self):
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
    #         base_salary = round(total_ctc - (total_ctc * mbo))
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
    #         if basic / 12 > 15000:
    #             pf = 1800 * 12
    #         else:
    #             pf = (basic / 12 * 0.12) * 12
    #         fca = self.food_coupon_alw
    #         spl_alw = base_salary - (basic + hra + std_ded + lta + pf + fca)
    #         var_alw = total_ctc * mbo
    #         self.write({'basic_salary': round(basic),
    #                     'hra': round(hra),
    #                     'standard_deduction': round(std_ded),
    #                     'lta': round(lta),
    #                     'special_allowance': round(spl_alw),
    #                     'variable_allowance': round(var_alw),
    #                     'pf_amount': round(pf)})

    @api.depends('employee_id', 'date_from', 'date_to')
    def check_pending_month_salary(self):
        payslips = self.env['hr.payslip'].search(
            [('employee_id', '=', self.employee_id.id), ('state', 'not in', ('paid', 'cancel'))], order="id")
        data = {}
        i = 0
        name = {}
        x = 0
        for slip in payslips:
            # if slip.struct_id.name == 'Exzatech Payroll':
            if self.date_of_resignation:
                if (slip.date_from >= self.date_of_resignation) and (slip.date_from <= self.emp_relieving_date):
                    for line in slip.line_ids:
                        if line.code == 'NET':
                            i += 1
                            x += 1
                            total = line.total
                            data[i] = total
                            name[x] = format_date(self.env, slip.date_from, date_format="MMMM")
        self.month_1 = data.get(1)
        self.month_2 = data.get(2)
        self.month_3 = data.get(3)
        self.month_name_1 = name.get(1)
        self.month_name_2 = name.get(2)
        self.month_name_3 = name.get(3)

    @api.depends('employee_id', 'date_from', 'date_to')
    def check_pending_salary_days(self):
        payslips = self.env['hr.payslip'].search(
            [('employee_id', '=', self.employee_id.id)])
        if payslips:
            for slip in payslips:
                # if slip.struct_id.name == 'Exzatech Payroll':
                # if slip.struct_id.name == 'Executive Payroll':
                # if 'Exzatech' in slip.struct_id.name:
                if self.emp_relieving_date:
                    if (slip.date_to >= self.emp_relieving_date >= slip.date_from):
                        self.pending_salary_days = 0
                        self.pending_total_days = 0
                    else:
                        date_1 = fields.Date.to_string(date.today().replace(day=1))
                        date_from = (self.emp_relieving_date.replace(day=1))

                        month = self.emp_relieving_date.month
                        year = self.emp_relieving_date.year
                        days = monthrange(year, month)
                        pending_total_days = days[1]

                        diff = (self.emp_relieving_date - date_from).days + 1
                        self.pending_salary_days = diff
                        self.pending_total_days = pending_total_days
        else:
            date_1 = fields.Date.to_string(date.today().replace(day=1))
            date_from = (self.emp_relieving_date.replace(day=1))
            diff = (self.emp_relieving_date - date_from).days + 1
            self.pending_salary_days = diff

            month = self.emp_relieving_date.month
            year = self.emp_relieving_date.year
            days = monthrange(year, month)
            pending_total_days = days[1]
            self.pending_total_days = pending_total_days

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
        if self.emp_relieving_date:
            if self.date_from <= self.emp_relieving_date <= self.date_to:
                relieve_date = str(self.emp_relieving_date)
                relieve_date = datetime.strptime(relieve_date, "%Y-%m-%d")
                start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
                end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
                days = (end_date - start_date).days + 1
                new_days = (relieve_date - start_date).days + 1
                sal_days = days - new_days
            if self.date_from > self.emp_relieving_date:
                new_days = 0
        elif self.retirement_date:
            if self.date_from <= self.retirement_date <= self.date_to:
                retire_date = str(self.retirement_date)
                retire_date = datetime.strptime(retire_date, "%Y-%m-%d")
                start_date = datetime.strptime(str(date_from), "%Y-%m-%d")
                end_date = datetime.strptime(str(date_to), "%Y-%m-%d")
                days = (end_date - start_date).days + 1
                new_days = (retire_date - start_date).days + 1
                sal_days = days - new_days
            if self.date_from > self.retirement_date:
                new_days = 0
        self.with_user(2).write({
            'paid_days': new_days,
            'salary_days': sal_days,
        })
        emp_id = self.employee_id.id
        holiday_obj = self.env['resource.calendar.leaves']
        public_holidays = holiday_obj.search([])
        for val in public_holidays:
            if val.work_entry_type_id.code == 'PUBLIC':
                start_date = val.date_from.date()
                end_date = val.date_to.date()
                if start_date >= date_from and end_date <= date_to:
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
        type_id = self.env['hr.leave.type'].search([('name', '=', 'Unpaid')])
        recs = self.env['hr.leave'].search([('employee_id', '=', emp_id), ('state', '=', 'validate'),
                                            ('holiday_status_id', '=', type_id.id),
                                            ('request_date_from', '>=', date_from),
                                            ('request_date_to', '<=', date_to)])
        for rec in recs:
            lop_days += rec.number_of_days
        self.with_user(2).write({
            'unpaid_days': lop_days,
        })
        leave_enc_days = 0
        allocation = self.env['hr.leave.allocation'].search(
            [('employee_id', '=', emp.id), ('holiday_status_id.is_encashable', '=', True)])
        alloc_days = 0
        taken_days = 0
        for alloc in allocation:
            # if alloc.holiday_status_id.name == "Paid Time Off":
            alloc_days = alloc.number_of_days
            recs = self.env['hr.leave'].search([('employee_id', '=', emp.id), ('state', '=', 'validate'),
                                                ('holiday_status_id', '=', alloc.holiday_status_id.id)])
            for rec in recs:
                taken_days += rec.number_of_days
        leave_enc_days = alloc_days - taken_days
        self.leave_balance = leave_enc_days

    @api.model
    def calculate_no_years(self):
        years = 0
        if self.emp_relieving_date:
            rd = rdelta.relativedelta(self.emp_relieving_date, self.employee_id.first_contract_date)
            self.service_years = "{0.years} years and {0.months} month(s)".format(rd)
            self.years = rd.years
            if rd.years >= 5:
                years += rd.years
        elif self.retirement_date:
            rd = rdelta.relativedelta(self.retirement_date, self.employee_id.first_contract_date)
            self.service_years = "{0.years} years and {0.months} month(s)".format(rd)
            self.years = rd.years
            if rd.years >= 5:
                years += rd.years
        return years

    def get_years(self):
        return self.years

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
            'weekend_days': sun + sat,
            'present_days': self.total_days - (self.weekend_days + self.leave_days + self.public_leave_days),
        })

    def order_formatLang(self, value, currency_obj=False):
        res = value
        if currency_obj and value:
            res = formatLang(self.env, value, currency_obj=False)
        return res

    def net_amount_to_text(self):
        words = " "
        for val in self.line_ids:
            if val.code == "NET":
                net_amount = round(val.total)
                words = 'Rupees ' + num2words(net_amount, lang='en_IN').title() + ' only'
        return words


    #number of days present

    # @api.onchange('employee_id')
    def value_days_present_days(self):
        for rec in self:
            # get_date = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
            if rec.emp_relieving_date and rec.date_from and rec.date_to:
                if rec.date_from < rec.emp_relieving_date < rec.date_to:
                    date_value_field = (rec.emp_relieving_date - rec.date_from ).days
                    rec.days_present = date_value_field
                    print(date_value_field, 'Days')
                    print('Found')
                else:
                    print('Not Found')
            else:
                print('Invalid data')











class Employee(models.Model):
    _inherit = "hr.employee"

    # to be written in hr.resignation(payslip)
    @api.model
    def calculate_total_days(self):
        res = self.env['hr.resignation']
        rec = res.search([('employee_id', '=', self.id)])
        if rec.emp_relieving_date:
            month = rec.emp_relieving_date.month
            year = rec.emp_relieving_date.year
            days = monthrange(year, month)
            days = days[1]
        elif rec.retirement_date:
            month = rec.retirement_date.month
            year = rec.retirement_date.year
            days = monthrange(year, month)
            days = days[1]
        return days

    @api.model
    def get_notice_shortfall_days(self):
        res = self.env['hr.resignation'].search([('employee_id', '=', self.id)])
        days = res.get_notice_days()
        return days

    @api.model
    def get_leave_balance(self):
        res = self.env['hr.resignation'].search([('employee_id', '=', self.id)])
        days = res.get_leave_balance()
        return days

    @api.model
    def get_no_years(self):
        # calculate_no_years
        res = self.env['hr.resignation'].search([('employee_id', '=', self.id)])
        yrs = res.get_years()
        return yrs
