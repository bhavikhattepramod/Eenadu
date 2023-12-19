from odoo import models, fields, api, _


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    is_taxable = fields.Boolean("Is Taxable")
    rule_type = fields.Selection([('fixed', 'Fixed'), ('variable', 'Variable')], string="Rule Type", default="variable")
    rule_ded_priority = fields.Integer(string="Deduction priority")


class HrPayslipItax(models.Model):
    _inherit = 'hr.payslip.line'

    tax_bool = fields.Boolean(string='Tax Check')
    payslip_ded_priority = fields.Integer(string="Deduction priority")

