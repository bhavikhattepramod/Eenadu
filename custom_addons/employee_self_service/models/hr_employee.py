from odoo import models, fields, _, api
from odoo.tools import email_normalize
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    tds_count = fields.Integer("TDS", compute="compute_tds_count")
    allocation_used_display = fields.Float('Allocation used Display')
    native_place = fields.Many2one('employ.place',string="Native Place", tracking=True)
    native_district = fields.Many2one('employ.district',string="Native District", tracking=True)
    emp_nationality = fields.Char(string="Nationality",default='INDIAN', tracking=True)
    handi_caps = fields.Selection([('yes', 'YES'), ('no', 'NO')], string='Handicap', default='no', tracking=True)
    mother_tongue = fields.Many2one('native.language',string="Mother Tongue", tracking=True)
    height = fields.Float(string='Height (Cms)', tracking=True)
    weight = fields.Float(string='Weight (Kgs)', tracking=True)
    left_eye = fields.Char(string='Left Eye (Sight)', tracking=True)
    right_eye = fields.Char(string="Right Eye (Sight)", tracking=True)
    identification_mark1 = fields.Text(string="Identification Marks 1", tracking=True)
    identification_mark2 = fields.Text(string="Identification Marks 2", tracking=True)
    place_id = fields.Many2one("employ.place",string="Place of Birth", tracking=True)
    retired_age = fields.Date(string="Retirement Date" ,compute='_compute_retired_age', store=True, tracking=True)
    probation_date = fields.Date(string='Probation Date')
    emp_cat = fields.Many2one('general.category', string="General Category", tracking=True)
    gen_sub_cat = fields.Many2one('general.sub.category', string="General Sub Category")
    doc_emp = fields.One2many('document.attachment', 'doc_attach_emp')
    pf_number = fields.Char(string="PF Number", tracking=True)
    esi_number = fields.Char(string = "ESI Number")
    pf_applicable_check_box = fields.Boolean(string="PF Applicable")
    esi_applicable_check_box = fields.Boolean(string="ESI Applicable")
    incentive_type = fields.Selection([('fixed_amt','Fixed Amount'),('percentage','Percentage')])
    incentive_amt = fields.Monetary('Incentive Amount', currency_field='currency_id')
    incentive_percent = fields.Integer('Incentive')
    family_relation = fields.One2many('employee.relation','organization_relation',string='Organisation')
    # career_history_field = fields.One2many('employee.life.cycle', 'emp_code', domain=[('state', '=', 'post')])
    # unit_name_hr = fields.Many2many('unit.master',string='Unit Name', tracking=True)
    # section_name_hr = fields.Many2many('section.master',string='Section Name', tracking=True)




    # date_joining = fields.Date(string="Date Of Joining (Company)", tracking=True, compute='_compute_date_joining')


    # @api.depends('contract_ids.state', 'contract_ids.date_of_join_company')
    # def _compute_date_joining(self):
    #     for employee in self:
    #         contracts = employee._get_first_contracts()
    #         if contracts:
    #             employee.date_joining = min(contracts.mapped('date_of_join_company'))
    #         else:
    #             employee.date_joining = False

    @api.depends('birthday')
    def _compute_retired_age(self):
        for rec in self:
            if rec.birthday:
                r_age = self.env['res.company'].search([])
                retirement_age = r_age.retire_age
                birth_date = datetime.strptime(str(rec.birthday), "%Y-%m-%d").date()
                retired_aged = birth_date + relativedelta(years=+retirement_age)
                retired_age = retired_aged + relativedelta(day=31)
                rec.retired_age = retired_age.strftime("%Y-%m-%d")
            else:
                rec.retired_age = False

    def compute_tds_count(self):
        for rec in self:
            if rec.id:
                rec.tds_count = self.env['employee.tds'].search_count([('employee_id', '=', rec.id)])
            else:
                rec.tds_count = 0

    def action_tds_self_service(self):
        return {
            'name': _('TDS Details'),
            'type': 'ir.actions.act_window',
            'res_model': 'employee.tds',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'employee_id': self.id,
            },
        }

    def action_tax_self_service(self):
        return {
            'name': _('Tax Details'),
            'type': 'ir.actions.act_window',
            'res_model': 'it.returns',
            'view_mode': 'list',
            'views':
                [[self.env.ref('Itax_calculation_master.it_returns_tree_new').id, 'list'],
                 [self.env.ref('Itax_calculation_master.it_returns_form_new').id, 'form']],
            # 'view_id': 'Itax_calculation_master.action_it_returns_new',
            # 'view_id': self.env.ref('Itax_calculation_master.it_returns_tree_new').id,
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'employee_id': self.id,
            },
        }
        # return {
        #     'name': _('Tax Details'),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'hr.employee.tax',
        #     'view_mode': 'tree,form',
        #     'domain': [('employee_id', '=', self.id)],
        #     'context': {
        #         'employee_id': self.id,
        #     },
        # }

    def action_time_off_dashboard_self_service(self):
        return {
            'name': _('Time Off Dashboard'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave',
            'view_mode': 'calendar',
            'views':
                [[self.env.ref('hr_holidays.hr_leave_view_dashboard').id, 'calendar']],
            # 'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {
                'employee_id': self.id,
            },
        }

    def _create_user(self):
        """ create a new user for wizard_user.partner_id
            :returns record of res.users
        """
        return self.env['res.users'].create(dict(
            name=self.name,
            login=self.work_email,
            company_id=self.env.company.id,
        ))

    def action_create_users(self):
        for records in self:
            # self.ensure_one()
            group_user = records.env.ref('base.group_user')
            user_sudo = records.user_id.sudo()

            if not user_sudo:
                # create a user if necessary and make sure it is in the portal group
                company = records.env.company
                user_sudo = records.sudo().with_company(company.id)._create_user()
                if user_sudo:
                    user_sudo.write({'active': True, 'groups_id': [(4, group_user.id)]})
                    # prepare for the signup process
                    user_sudo.partner_id.signup_prepare()
            for rec in records:
                rec.user_id = user_sudo
                rec.work_email = user_sudo.login



class Documentsattach(models.Model):
    _name = 'document.attachment'

    name = fields.Char(string="Name of Document")
    file_attach = fields.Binary(string="Attach the File")
    doc_attach_emp = fields.Many2one('hr.employee', string='Employee Name')

class Emprelation(models.Model):
    _name = 'employee.relation'

    name = fields.Char(string='Name')
    designation = fields.Char(string='Designation')
    type = fields.Selection([('relation','Relation'),('friend','Friend')],string='Type')
    organization_relation = fields.Many2one('hr.employee',string='Organization')
#
#
#
# class EmployeeLifeCycle(models.Model):
#     _name = 'employee.life.cycle'
# #     _inherit = ['mail.thread','mail.activity.mixin']
# #     _rec_name = 'emp_name'
# #
# #
#     emp_code = fields.Many2one('hr.employee',string='Employee Name', tracking =True, required=True)
#     emp_name = fields.Char(related='emp_code.identification_id',string='Employee Code', tracking =True)
#     state = fields.Selection(([
#         ('new', 'New'),
#         ('submit', 'Submit'),
#         ('hr', 'Hr'),
#         ('hod', 'Hod'),
#         ('approved', 'Approved'),
#         ('post', 'Post'),
#         ('reject', 'Reject'),
#     ]), string="Status", default='new', tracking=True)
#     process = fields.Selection(([
#         ('tran_prob', 'Trainees to Probation'),
#         ('prob_to_conf', 'Probation to Confirmation'),
#         ('prob_ext', 'Probation Extension'),
#         ('transfers', 'Transfers'),
#         ('promotion', 'Promotions'),
#         ('increments', 'Increments'),
#         ('re_designation', 'Re-designation'),
#     ]), string="Transaction Type", tracking=True, required=True)
#     company_from = fields.Many2one('res.company',string="From Company", tracking =True)
#     unit_elc = fields.Many2many(related='emp_code.unit_name_hr',string='Unit', tracking =True)
#     department = fields.Many2one(related='emp_code.department_id',string='Department', tracking =True)
#     section_from_top_elc = fields.Many2many(related ='emp_code.section_name_hr',string='Section', tracking =True)





