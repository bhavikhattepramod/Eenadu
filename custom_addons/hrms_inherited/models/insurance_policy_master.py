from odoo import fields, models, api
from odoo.exceptions import ValidationError


class InsurancePolicyMatserDetailsChanges(models.Model):
    _name = "insurance.policy"
    _rec_name = 'employee_name'

    employee_name = fields.Char(related='employee_code.identification_id' ,string="Employee Code")
    employee_code = fields.Many2one('hr.employee',string="Employee Name")
    total_sum_values = fields.Float(string='Total', compute='_compute_total_sum_values')
    insurance_policy_master = fields.One2many('insurance.policy.line','service', string='Insurance policy')
    # payslip_ids = fields.One2many('hr.payslip', 'insurance', string='Payslips')


    @api.depends('insurance_policy_master.premium_amt', 'insurance_policy_master.insurance_applicable')
    def _compute_total_sum_values(self):
        for policy in self:
            if policy.insurance_policy_master and any(
                    line.insurance_applicable for line in policy.insurance_policy_master):
                total_premium_amt = sum(
                    line.premium_amt for line in policy.insurance_policy_master if line.insurance_applicable)
                policy.total_sum_values = total_premium_amt
            else:
                policy.total_sum_values = 0.0


class InsurancePolicyMatser(models.Model):
    _name = "insurance.policy.line"


    # service_provider = fields.Char(string='Service Provider')
    service_company = fields.Many2one('service.provider',string='Service Provider')
    policy_no = fields.Char(string='Policy No.')
    policy_amt = fields.Float(string='Policy Amount')
    premium_amt = fields.Float(string='Premium Amount')
    service =  fields.Many2one('insurance.policy')
    insurance_applicable = fields.Boolean(string='Active')

class HrPayslipInsurance(models.Model):
    _inherit = "hr.payslip"

    insurance_field = fields.Float(string='Insurance')
    notice_period_amount = fields.Float(string='Notice Period amount')


    # @api.constrains('employee_id')


    # def compute_sheet(self):
    #     self.onchange_employee_insurance()

class ServiceProvider(models.Model):
    _name = 'service.provider'
    _rec_name = 'service_provider_name'

    service_provider_name = fields.Char(string='Insurance Company Name')
    contact_person = fields.Char(string='Contact Person')
    contact_no = fields.Integer(string='Contact No.')
    branch_name = fields.Char(string='Branch Name')
    branch_address = fields.Char(string='Branch Address')
