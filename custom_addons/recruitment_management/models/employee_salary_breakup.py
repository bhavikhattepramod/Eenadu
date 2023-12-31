from odoo import api, fields, models, _


class EmployeeSalaryBreakup(models.Model):
    _name = 'employee.salary.breakup'

    name = fields.Many2one("hr.applicant", string="Applicant's Name")
    # name = fields.Char("Name")
    # email = fields.Char("Email")
    basic_salary = fields.Float("Basic Salary(per Year)")
    hra = fields.Float("HRA")
    standard_deduction = fields.Float("Standard Deduction(per Year)")
    leave_travel_allowance = fields.Float("Leave Travel Allowance(per Year)")
    special_allowance = fields.Float("Special Allowances(per Year)")
    food_coupon = fields.Float("Food Coupon")
    pf_employer_contribution = fields.Float("PF Employer Contribution(per Year)")
    variable_allowance = fields.Float("Variable Allowance")
    # deduction = fields.Float("Deduction")
    pf_employee_contribution = fields.Float("PF Employee Contribution")
    professional_tax = fields.Float(string="Professional Tax")
    income_tax_tds = fields.Float(string="Income Tax (TDS)")
    proposed_salary = fields.Float(related='name.salary_proposed', string="Proposed Salary")
    salary_structure = fields.Many2one("hr.payroll.structure", string="Salary")
    mbo1 = fields.Float()


class EmployeeApplicant(models.Model):
    _inherit = 'hr.applicant'
    _rec_name = 'partner_name'

