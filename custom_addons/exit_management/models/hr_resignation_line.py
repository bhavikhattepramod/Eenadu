from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrResignationLine(models.Model):
    _name = 'hr.resignation.line'
    _description = 'Hr Resignation Line'
    _order = 'sequence, code'

    name = fields.Char(required=True)
    note = fields.Text(string='Description')
    sequence = fields.Integer(required=True, index=True, default=5,
                              help='Use to arrange calculation sequence')
    code = fields.Char(required=True,
                       help="The code of salary rules can be used as reference in computation of other rules. "
                       "In that case, it is case sensitive.")
    slip_id = fields.Many2one('hr.resignation', string='Pay Slip', required=True, ondelete='cascade')
    salary_rule_id = fields.Many2one('hr.salary.rule', string='Rule', required=True)
    salary_master_exit = fields.Float(string="Salary Master", store=True, readonly=True)
    # contract_id = fields.Many2one('hr.contract', string='Contract', required=True, index=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    rate = fields.Float(string='Rate (%)', digits='Payroll Rate', default=100.0)
    amount = fields.Monetary()
    salary_master_res = fields.Monetary()
    quantity = fields.Float(digits='Payroll', default=1.0)
    total = fields.Monetary(compute='_compute_total', string='Total', store=True)
    amount_select = fields.Selection(related='salary_rule_id.amount_select', readonly=True)
    amount_fix = fields.Float(related='salary_rule_id.amount_fix', readonly=True)
    amount_percentage = fields.Float(related='salary_rule_id.amount_percentage', readonly=True)
    appears_on_payslip = fields.Boolean(related='salary_rule_id.appears_on_payslip', readonly=True)
    category_id = fields.Many2one(related='salary_rule_id.category_id', readonly=True, store=True)
    # partner_id = fields.Many2one(related='salary_rule_id.partner_id', readonly=True, store=True)

    date_from = fields.Date(string='From', related="slip_id.date_from", store=True)
    date_to = fields.Date(string='To', related="slip_id.date_to", store=True)
    company_id = fields.Many2one(related='slip_id.company_id')
    currency_id = fields.Many2one('res.currency', related='slip_id.currency_id')
    structure_id_exit = fields.Many2one('hr.payroll.structure', string='Structure')


    company_notice_period_check = fields.Boolean(string='Company Notice Period Applicable')
    employee_notice_period_check = fields.Boolean(string='Employee Notice Period Applicable')
    gratuity_rule_check_exit = fields.Boolean(string='Gratuity Applicable')
    leave_encashment_rule_check_exit = fields.Boolean(string='Leave Encashment Applicable')
    pf_cal_exit = fields.Boolean(string='PF Calculation')
    esi_cal_exit = fields.Boolean(string='ESI Calculation')

    @api.depends('quantity', 'amount', 'rate')
    def _compute_total(self):
        for line in self:
            line.total = float(line.quantity) * line.amount * line.rate / 100




    # @api.depends('quantity', 'amount', 'rate')
    # def _compute_total(self):
    #     for line in self:
    #         res = self.env['hr.resignation'].search([('employee_id', '=', line.employee_id.id)])
    #         company_gra = self.env['res.company'].search([])
    #         # gratuity_emp = self.env['hr.employee'].search([])
    #         # for line in self:
    #
    #
    #     # def pass_value(self):
    #         for value in res:
    #             for lines in res.line_ids:
    #                 for comp in company_gra:
    #                     # for emp in gratuity_emp:
    #                     line.total = float(line.quantity) * line.amount * line.rate / 100
    #                     if lines.code == 'COMPNOTICE':
    #                         print('sss')
    #                         lines.total = value.notice_tot
    #                         print(lines.total, 'total')
    #                     if lines.code == 'EMPNOTICE':
    #                         print('employe')
    #                         lines.total = value.notice_tot_rec
    #                     print(lines.total,'tot')
    #                     if comp.calculate_gratuity == True and value.employee_id.gratuity_employee_level == True and lines.code == 'GRAT':
    #                         lines.total = value.total_gratuity
    #                     if lines.code == 'LEAVENC':
    #                         print('employe')
    #                         lines.total = value.leave_sum
    #                     if lines.code == 'EPFEMP':
    #                         lines.total = value.pf_emp_value_exit
    #                     if lines.code == 'EPFEMPLR':
    #                         lines.total = value.pf_empr_value_exit
    #                     if lines.code == 'EPSEMPLR':
    #                         lines.total = value.eps_emp_value_exit
    #                     if lines.code == 'ESIEMP':
    #                         lines.total = value.esi_emp_value_exit
    #                     if lines.code == 'ESIEMPLR':
    #                         lines.total = value.esi_empr_value_exit
            # return lines.total

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if 'employee_id' not in values or 'contract_id' not in values:
                payslip = self.env['hr.resignation'].browse(values.get('slip_id'))
                values['employee_id'] = values.get('employee_id') or payslip.employee_id.id
                # values['contract_id'] = values.get('contract_id') or payslip.contract_id and payslip.contract_id.id
                # if not values['contract_id']:
                #     raise UserError(_('You must set a contract to create a payslip line.'))
        return super(HrResignationLine, self).create(vals_list)