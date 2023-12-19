from odoo import fields, models, api


class EmployeeSalaryDetailsChanges(models.Model):
    _inherit = "hr.contract"

    salary_rule_master = fields.One2many('hr.contract.line', 'salary_contract', string='Salary Rules')
    vpf_field = fields.Boolean(string="VPF")
    da_exit_applicable = fields.Boolean(string='DA Applicable in Exit')
    nsa_amount = fields.Float(string="NSA Amount")
    lop_days_exit = fields.Float()
    present_days_exit = fields.Float()
    amount_da = fields.Float()


    @api.onchange('vpf_field')
    def _onchange_vpf_field(self):
        for line in self.salary_rule_master:
            if line.salary_code == 'VPF':
                line.vpf_field = self.vpf_field

class CreateHRcontractLine(models.Model):
    _name = "hr.contract.line"

    salary_line_component = fields.Many2one("hr.salary.rule", string="Salary Name")
    salary_code = fields.Char(related="salary_line_component.code", string='Code')
    salary_amount = fields.Float(string="Amount")
    salary_contract = fields.Many2one('hr.contract')
    salary_amount_percentage = fields.Float(string="Percentage")
    vpf_field = fields.Boolean(string="VPF")
    prorate_field = fields.Boolean(string="Applicable for Prorata")
    lop_applicable = fields.Boolean(string="Applicable for LoP")
    # lop_arrear_applicable = fields.Boolean(string="Applicable for LoP Arrear")


class CreateAmountField(models.Model):
    _inherit = "hr.salary.rule"

    sal_amount = fields.Float(string="Amount")
