from odoo import fields, models, api


class LoanManagement(models.Model):
    _name = 'employee.loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'loan_name_id'

    employee_code = fields.Many2one('hr.employee', string='Employee Code', required=True)
    employee_name = fields.Char(related='employee_code.identification_id', string='Employee Code')
    loan_name_id = fields.Many2one('hr.salary.rule', string='Loan Name', tracking=True, domain=[('is_loan', '=', True)], required=True)
    loan_amount = fields.Float(string="Loan Amount", tracking=True, required=True)
    loan_applied_date = fields.Date(string='Loan Applied Date', tracking=True, required=True)
    loan_approved_date = fields.Date(string='Loan Approved Date', tracking=True, required=True)
    loan_disbursed_date = fields.Date(string='Loan Disbursed Date', tracking=True, required=True)
    loan_recovery_start_date = fields.Date(string='Loan Recovery Start Date', tracking=True, required=True)
    interest_applicable = fields.Selection((
        [('yes', 'Yes'), ('no', 'No')]), string='Interest Applicable', default='no', tracking=True)
    interest_percent = fields.Float(string='Interest Percentage', tracking=True)
    loan_recovery_frequency = fields.Selection((
        [('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('half-year', 'Half Year'), ('year', 'Yearly')]),
        string='Loan Recovery Frequency', tracking=True, default='monthly')
    loan_recovery = fields.Float(string='Loan recovery (Installment amount)', tracking=True, required=True)
    no_of_instalments = fields.Integer(string='No. of Instalments', compute='_compute_no_of_installments',
                                       inverse='_inverse_no_of_installments', tracking=True, required=True)
    principle_amount = fields.Float(string='Principle Amount (recovery)', tracking=True)
    interest_amount = fields.Float(string='Interest Amount (recovery)', tracking=True)
    interest_method = fields.Selection((
        [('emi', 'Emi'), ('reducing_balance', 'Reducing Balance method')]), string='Interest Method', tracking=True)
    loan_closed = fields.Boolean(string='Loan Closed', default=False, tracking=True)
    loan_closed_date = fields.Date(string='Loan Closure Date', tracking=True)
    active = fields.Boolean(string='Active', default=True)
    # result_field = fields.Boolean(string='Result')

    # Getting the loan recovery amount from master and updating into the contract
    @api.constrains('loan_closed')
    @api.onchange('loan_recovery')
    def send_loan_amount(self):
        l_amount = self.env['hr.contract'].search([('employee_id', '=', self.employee_code.id)])
        print(l_amount, 'amount')
        for val in l_amount:
            # print(self.loan_name_id.name, 'loan name')
            # print(self.loan_amount, 'amount')
            # print(self.loan_closed,'closed')
            if self.loan_closed == False:
                existing_rules = val.salary_rule_master.filtered(
                    lambda rule: rule.salary_line_component.id == self.loan_name_id.id)
                if existing_rules:
                    existing_rules.write({
                        'salary_amount': self.loan_recovery,
                        'salary_contract': l_amount.id
                    })
                else:
                    val.salary_rule_master.create({
                        'salary_line_component': self.loan_name_id.id,
                        'salary_amount': self.loan_recovery,
                        'salary_contract': l_amount.id
                    })
            elif self.loan_closed == True:
                existing_rules = val.salary_rule_master.filtered(
                    lambda rule: rule.salary_line_component.id == self.loan_name_id.id)
                if existing_rules:
                    existing_rules.write({
                        'salary_amount': 0.00,
                        'salary_contract': l_amount.id
                    })

    @api.onchange('loan_recovery')
    def _compute_no_of_installments(self):
        for rec in self:
            if rec.loan_amount > 0.00 and rec.loan_recovery > 0.00:
                rec.no_of_instalments = rec.loan_amount / rec.loan_recovery
            else:
                rec.loan_recovery = 0.00

    @api.onchange('no_of_instalments')
    def _inverse_no_of_installments(self):
        for val in self:
            if val.loan_amount > 0.00 :
                val.loan_recovery = val.loan_amount / val.no_of_instalments

    @api.onchange('loan_applied_date')
    def onchange_loan_applied_date(self):
        if self.loan_applied_date:
            if self.loan_applied_date > fields.Date.today():
                raise models.UserError('Date should be less than today')

    @api.onchange('loan_approved_date')
    def onchange_loan_approved_date(self):
        if self.loan_approved_date:
            if self.loan_approved_date < self.loan_applied_date:
                raise models.UserError('Date should be less than applied date')

    @api.onchange('loan_disbursed_date')
    def onchange_loan_disbursed_date(self):
        if self.loan_disbursed_date:
            if self.loan_disbursed_date < self.loan_approved_date:
                raise models.UserError('Date should be equal or greater than approved date')

    @api.onchange('loan_recovery_start_date')
    def onchange_loan_disbursed_date(self):
        if self.loan_recovery_start_date:
            if self.loan_recovery_start_date < self.loan_disbursed_date:
                raise models.UserError('Date should be equal or greater than disbursed date')


class EmployeeLoanField(models.Model):
    _inherit = 'hr.salary.rule'

    is_loan = fields.Boolean(string='Loan Component')


class HrPayslipCheck(models.Model):
    _inherit = 'hr.payslip'

    loan_boolean = fields.Boolean(string='Check Box')

    # Comparing the payslip date to to loan master recovery start date
    @api.onchange('date_to')
    def onchange_loan_recovery_date_to(self):
        for record in self:
            payslip_recovery = self.env['employee.loan'].search([('employee_code', '=', record.employee_id.id)])
            for recovery in payslip_recovery:
                if record.date_to and recovery.loan_recovery_start_date:
                    date1 = fields.Date.from_string(record.date_to)
                    date2 = fields.Date.from_string(recovery.loan_recovery_start_date)
                    print('--------------------------')
                    if date2 <= date1:  # Checking if date_to is equal or greater
                        print('+++++++++++++++++++++++++++')
                        record.loan_boolean = True
                    else:
                        print('pppppppppppppppppppppppppp')
                        record.loan_boolean = False
                else:
                    print('zzzzzzzzzzzzzzzzzzzzzzzzzz')
                    record.loan_boolean = False
