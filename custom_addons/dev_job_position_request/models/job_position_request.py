# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from odoo import models, fields, api, _
from datetime import datetime, date
from odoo.exceptions import ValidationError
from ast import literal_eval


class JobPositionRequest(models.Model):
    _name = "job.position.request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Create new job positions from here"

    def make_url(self):
        menu_id = self.env.ref("dev_job_position_request.menu_job_position_request").id
        action_id = self.env.ref("dev_job_position_request.action_dev_job_position_request").id
        ir_param = self.env['ir.config_parameter'].sudo()
        base_url = ir_param.get_param('web.base.url')
        if base_url:
            base_url += '/web#id=%s&action=%s&model=%s&view_type=form&cids=&menu_id=%s' % (
                self.id, action_id, self._name, menu_id)
        return base_url

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('job.position.request.sequence') or 'New'
        return super(JobPositionRequest, self).create(vals)

    @api.returns('self')
    def _get_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1) or False

    def submit_to_manager(self):
        self.state = "to_approve"
        if not self.env.user.has_group('hr_recruitment.group_hr_recruitment_manager'):
            authorized_group = self.env.ref('hr_recruitment.group_hr_recruitment_manager')
            if authorized_group and authorized_group.users:
                authorized_users = authorized_group.users
                email_from = self.env.user and self.env.user.partner_id and self.env.user.partner_id.email or ''
                template = self.env.ref("dev_job_position_request.email_template_job_position_request")
                if template and email_from and authorized_users:
                    template_id = self.env['mail.template'].browse(int(template))
                    if template_id:
                        for user in authorized_users:
                            if user.partner_id and user.partner_id.email:
                                template_id.write({'email_from': email_from})
                                template_id.write({'email_to': user.partner_id.email})
                                template_id.send_mail(self.id, force_send=True)

    def send_job_position_created_email(self, job_id):
        if self.job_id and self.employee_id:
            if self.employee_id.user_id and self.employee_id.user_id.partner_id and self.employee_id.user_id.partner_id.email:
                if self.env.user and self.env.user.partner_id and self.env.user.partner_id.email:
                    template = self.env.ref("dev_job_position_request.template_manger_to_user")
                    if template:
                        template_id = self.env['mail.template'].browse(int(template))
                        if template_id:
                            template_id.write({'email_from': self.env.user.partner_id.email})
                            template_id.write({'email_to': self.employee_id.user_id.partner_id.email})
                            template_id.send_mail(self.id, force_send=True)

    def send_job_position_rejected_email(self):
        if self.employee_id.user_id and self.employee_id.user_id.partner_id and self.employee_id.user_id.partner_id.email:
            if self.env.user and self.env.user.partner_id and self.env.user.partner_id.email:
                template = self.env.ref("dev_job_position_request.email_template_job_position_request_rejected")
                if template:
                    template_id = self.env['mail.template'].browse(int(template))
                    if template_id:
                        template_id.write({'email_from': self.env.user.partner_id.email})
                        template_id.write({'email_to': self.employee_id.user_id.partner_id.email})
                        template_id.send_mail(self.id, force_send=True)

    def send_job_position_approved_email(self):
        if self.employee_id.user_id and self.employee_id.user_id.partner_id and self.employee_id.user_id.partner_id.email:
            if self.env.user and self.env.user.partner_id and self.env.user.partner_id.email:
                template = self.env.ref("dev_job_position_request.email_template_job_position_request_approved").id
                # print(template, 'temp')
                if template:
                    template_id = self.env['mail.template'].browse(int(template))
                    if template_id:
                        template_id.write({'email_from': self.env.user.partner_id.email})
                        template_id.write({'email_to': self.employee_id.user_id.partner_id.email})
                        template_id.send_mail(self.id, force_send=True)

    # def action_approve_stage(self):
    #     # logic for approving the stage
    #     self.stage_approved = True
    #     # send email
    #     if self.partner_id.email:
    #         template_id = self.env.ref('module_name.email_template_id').id
    #         if template_id:
    #             self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)
    #     else:
    #         raise UserError('Partner does not have an email address.')

    def form_submit(self):
        self.state = "submit"
        # return {
        #     'effect': {
        #         'fadeout': 'slow',
        #         'message': 'Requisition is Submitted',
        #         'type': 'rainbow_man',
        #     }
        # }

    # changed
    # def submit_to_hod_wizard(self):
    #     self.state = "submit"

    def button_submit(self):
        self.state = "hod_approve"

    def hod_approve_request_wizard(self):
        context = dict(self.env.context)
        context.update({
            'hr_approved': True,
            'default_job_position_request_ids': self.ids,
        })
        return {
            'name': 'Confirm HOD Approved',
            'view_mode': 'form',
            'res_model': 'job.position.hod_approve',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
        }

    def hod_approve_request(self):
        if self.finance_exempted == False:
            self.state = "hod_approve"
            print('---------------')
            self.send_job_position_approved_email()
        else:
            self.state = "finance_approve"
            print('++++++++++++++++')
            self.send_job_position_approved_email()

    def approve_finance_wizard(self):
        context = dict(self.env.context)
        context.update({
            'finance_approve': True,
            'default_job_position_request_ids': self.ids,
        })
        return {
            'name': 'Confirm Finance Approve',
            'view_mode': 'form',
            'res_model': 'job.position.finance_approve',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
        }

    def approve_finance(self):
        self.state = "finance_approve"
        self.send_job_position_approved_email()

    def hr_approve_request_wizard(self):
        # self.state = "approved"
        context = dict(self.env.context)
        context.update({
            'hr_approved': True,
            'default_job_position_request_ids': self.ids,
        })
        return {
            'name': 'Confirm Hr Approved',
            'view_mode': 'form',
            'res_model': 'job.position.hr_approve',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
        }

    def hr_approve_request(self):
        self.state = "approved"
        self.send_job_position_approved_email()

    def approve_request(self):
        self.state = "approved"
        self.send_job_position_approved_email()

    # def approve_request_wizard(self):
    #     context = dict(self.env.context)
    #     context.update({
    #         'approve': True,
    #         'default_job_position_request_ids': self.ids,
    #     })
    #     return {
    #         'name': 'Confirm Finance Approved',
    #         'view_mode': 'form',
    #         'res_model': 'job.position.approved',
    #         'view_id': False,
    #         'type': 'ir.actions.act_window',
    #         'context': context,
    #         'target': 'new',
    #     }

    def reject_request_wizard(self):
        context = dict(self.env.context)
        context.update({
            'reject': True,
            'default_job_position_request_ids': self.ids,
        })
        return {
            'name': 'Confirm Rejected',
            'view_mode': 'form',
            'res_model': 'job.position.rejected',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
        }

    def reject_request(self):
        if not self.finance_exempted:
            self.state = "rejected"
            if self.employee_id and self.employee_id.user_id:
                if self.env.user.id == self.employee_id.user_id.id:
                    pass
                else:
                    self.send_job_position_rejected_email()
            else:
                self.send_job_position_rejected_email()

    def set_to_new(self):
        self.state = "new"

    def view_job_position(self):
        form_id = self.env.ref("hr.view_hr_job_form").id
        return {'name': 'Job Position',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hr.job',
                'views': [(form_id, 'form')],
                'target': 'current',
                'res_id': self.job_id.id
                }

    def job_position_details(self):
        position_details = '''<table border=1 width=40% style="border-collapse: collapse;">'''
        tr_start = '''<tr>'''
        tr_end = '''</tr>'''
        td_start = '''<td>'''
        td_end = '''</td>'''
        th_end = '''</th>'''
        colspan_th_start = '''<th colspan=2 style="text-align: center";>'''
        colspan_th_start2 = '''<th style="text-align: left;">'''
        colspan_th_end = '''</th>'''
        position_details += tr_start + colspan_th_start + str(self.name) + colspan_th_end + tr_end
        date = datetime.strptime(str(self.date), "%Y-%m-%d").strftime('%d-%m-%Y')
        position_details += tr_start + colspan_th_start2 + 'Requested On' + th_end
        position_details += td_start + str(date) + td_end + tr_end + tr_end
        position_details += tr_start + colspan_th_start2 + 'Requested by' + th_end
        position_details += td_start + str(self.employee_id.name) + td_end + tr_end
        position_details += tr_start + colspan_th_start2 + 'Employees Required' + th_end
        position_details += td_start + str(self.expected_new_employees) + td_end + tr_end
        position_details += '''</table>'''
        return position_details

    @api.onchange('expected_date')
    def onchange_expected_date(self):
        if self.expected_date:
            if self.expected_date < fields.Date.today():
                raise models.UserError('Date should be greater than requested date')

    name = fields.Many2one('hr.job', string="Job Position", required=True, tracking=True)
    sequence = fields.Char(string="Sequence", copy=False, readonly=1, tracking=True)
    employee_id = fields.Many2one("hr.employee", string="Requested By", default=_get_employee, readonly=1,
                                  tracking=True)
    employee_name_val = fields.Char(related='employee_id.name', tracking=True)
    onrefer_id = fields.Many2one("hr.employee", string="Requested (On Behalf)", tracking=True)
    onrefer_name = fields.Char(related='onrefer_id.name', tracking=True)
    department_id = fields.Many2one("hr.department", string="Department", tracking=True, required=True)
    expected_new_employees = fields.Integer(string="Number of New Positions required", required=True, tracking=True)
    date = fields.Date(string="Requested On", default=fields.Datetime.now, tracking=True, required=True)
    job_id = fields.Many2one("hr.job", string="Job Position", copy=False, tracking=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.user.company_id,
                                 copy=False, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    state = fields.Selection(selection=[('new', 'New'),
                                        ('submit', 'Submitted'),
                                        ('hod_approve', 'HOD Approve'),
                                        ('finance_approve', 'Finance Approve'),
                                        ('hr_approved', 'HR Approve'),
                                        ('approved', 'Approved Requisitions'),
                                        ('rejected', 'Rejected')], default='new', string="MPR Status", tracking=True)
    to_approve_reason = fields.Text(tracking=True)
    hod_approve_reason = fields.Text(tracking=True)
    approved_reason = fields.Text(tracking=True)
    rejected_reason = fields.Text(tracking=True)

    emp_type = fields.Selection([('fresher', 'Fresher'), ('experienced', 'Experienced')], string="Employee Type"
                                , tracking=True, required=True)
    # employment_type = fields.Many2one("hr.contract.type", string="Employment Type")
    contract_type = fields.Selection([('permanent', 'Permanent'), ('temporary', 'Temporary'), ('contract', 'Contract'),
                                      ('hourly', 'Hourly Basis')], string='Employment Type', tracking=True,
                                     required=True)
    descrip = fields.Text(string='Description')
    request_emp = fields.Selection([('new', 'New'), ('addition', 'Addition'), ('replacement', 'Replacement')],
                                   string="Nature of Request", tracking=True, required=True)
    expected_date = fields.Date(string="Expected DOJ", tracking=True)
    reason_require = fields.Selection(
        [('resignation', 'Resignation'),
         ('termination', 'Termination'),
         ('death', 'Death'),
         ('retired', 'Retired'),
         ('relocation', 'Relocation'),
         ('others', 'Others')], string="Reason For Requirement", tracking=True, required=True)
    unit_place_ids = fields.Many2many('unit.master', string="Unit Name", tracking=True, required=True)
    qualifications_ids = fields.Many2many("educate.qualification", string="Qualification", tracking=True)
    job_experience = fields.Char(string="Total Job Experience", tracking=True)
    salary_min_range = fields.Float(string="Minimum (₹)", Tracking=True, required=True)
    salary_max_range = fields.Float(string="Maximum (₹)", Tracking=True, required=True)
    multiple_skill_ids = fields.Many2many('hr.skill.type', string="Required Skill", tracking=True)
    remarks = fields.Text(string="Additional Remarks", tracking=True)
    amount = fields.Float(string='Wages', tracking=True)
    type_hours = fields.Selection(
        [('per_hour', 'Per Hourly'),
         ('per_day', 'Per Day')],
        string="Hourly / Daily")
    salary_type_min = fields.Selection([('ctc', 'CTC'),
                                        ('gross salary', 'Gross Salary'),
                                        ('monthly salary', 'Monthly Salary')], tracking=True)
    salary_type_max = fields.Selection([('ctc', 'CTC'),
                                        ('gross salary', 'Gross Salary'),
                                        ('monthly salary', 'Monthly Salary')], tracking=True)
    wages_min = fields.Float('Minimum Wages', tracking=True)
    wages_max = fields.Float('Maximum Wages', tracking=True)
    finance_exempted = fields.Boolean(string='Finance Approval Exempted', default=False, tracking=True, required=True)
    finance_badge = fields.Selection([('finance', 'Finance Exempted')], string=" ")

    @api.onchange('name')
    @api.depends('name')
    def onchange_job_description(self):
        # print(des,'ggggggg')
        for record in self:
            des = self.env['hr.job'].search([('name', '=', record.name.name)])
            if des.description:
                html = des.description
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.text.strip()
                record.description = text
            else:
                print("No description in job position")

    @api.onchange('salary_type_min')
    def onchange_salary_type_min(self):
        for rec in self:
            if self.salary_type_min == 'monthly salary':
                rec.wages_min = self.salary_min_range * 12
            elif self.salary_type_min == 'ctc' or 'gross salary':
                rec.wages_min = self.salary_min_range / 12

    @api.onchange('salary_type_max')
    def onchange_salary_type_max(self):
        for record in self:
            if self.salary_type_max == 'monthly salary':
                record.wages_max = self.salary_max_range * 12
            elif self.salary_type_max == 'ctc' or 'gross salary':
                record.wages_max = self.salary_max_range / 12

    @api.onchange('finance_exempted')
    def onchange_finance_exempted(self):
        for rec in self:
            if rec.finance_exempted:
                rec.finance_badge = 'finance'
            else:
                rec.finance_badge = ''

    @api.model
    def get_data(self):
        total_records = self.env['job.position.request'].search([])
        total_new = self.env['job.position.request'].search([('state', '=', 'new')])
        total_submit = self.env['job.position.request'].search([('state', '=', 'submit')])
        total_hod = self.env['job.position.request'].search([('state', '=', 'hod_approve')])
        total_finance = self.env['job.position.request'].search([('state', '=', 'finance_approve')])
        total_hr = self.env['job.position.request'].search([('state', '=', 'hr_approved')])
        total_approved = self.env['job.position.request'].search([('state', '=', 'approved')])
        total_reject = self.env['job.position.request'].search([('state', '=', 'rejected')])
        total_finance_exempt = self.env['job.position.request'].search([('finance_exempted', '=', True)])
        return {
            'total_records': len(total_records),
            'total_new': len(total_new),
            'total_submit': len(total_submit),
            'total_hod': len(total_hod),
            'total_finance': len(total_finance),
            'total_hr': len(total_hr),
            'total_approved': len(total_approved),
            'total_reject': len(total_reject),
            'total_finance_exempt': len(total_finance_exempt)
        }

    # def _get_action(self, action_xmlid):
    #     print("22222")
    #     print(action_xmlid,'action_xmlid')
    #     action = self.env["ir.actions.actions"]._for_xml_id(action_xmlid)
    #     # print(action,'actionnnnnnnnnnnnnnn')
    #     return action
    #
    #
    # def get_action_manpower_tree_new(self):
    #     print("33333")
    #     return self._get_action('dev_job_position_request.action_dev_job_position_request_new')
    #
    # def get_action_manpower_tree_submit(self):
    #     print("4444444")
    #     return self._get_action('dev_job_position_request.action_dev_job_position_request_submit')
    #
    # def get_action_manpower_tree_hod(self):
    #     print("55555")
    #     return self._get_action('dev_job_position_request.action_dev_job_position_request_hod')
    #
    # def get_action_manpower_tree_finance(self):
    #     return self._get_action('dev_job_position_request.action_dev_job_position_request_finance')
    #
    # def get_action_manpower_tree_hr(self):
    #     return self._get_action('dev_job_position_request.action_dev_job_position_request_hr')
    #
    # def get_action_manpower_tree_approved(self):
    #     return self._get_action('dev_job_position_request.action_dev_job_position_request_approved')
    #
    # def get_action_manpower_tree_reject(self):
    #     return self._get_action('dev_job_position_request.action_dev_job_position_request_reject')


class HrApplicantInherit(models.Model):
    _inherit = 'hr.applicant'

    @api.onchange('job_id')
    def onchange_job_id(self):
        job = self.env['hr.job'].search([('name', '=', self.job_id.name)])
        for rec in job:
            self.interviewer_ids = rec.interviewer_ids
            self.user_id = rec.user_id
