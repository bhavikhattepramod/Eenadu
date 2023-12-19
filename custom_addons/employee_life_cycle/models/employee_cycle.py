from odoo import fields ,models ,api
from datetime import date


class EmployeeLifeCycle(models.Model):
    _name = 'employee.life.cycle'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'emp_name'

    process = fields.Selection(([
        ('tran_prob', 'Trainees to Probation'),
        ('prob_to_conf', 'Probation to Confirmation'),
        ('prob_ext', 'Probation Extension'),
        ('transfers', 'Transfers'),
        ('promotion', 'Promotions'),
        ('increments', 'Increments'),
        ('re_designation', 'Re-designation'),
        ('extension_of_training', 'Extension of Training'),
        ('service_extension', 'Service Extension'),
        ('probation_discharge', 'Probation Discharge'),
        ('trainee_discharge', 'Trainee Discharge'),
    ]), string="Transaction Type", tracking =True, required=True)
    emp_code = fields.Many2one('hr.employee',string='Employee Name', tracking =True, required=True)
    emp_name = fields.Char(related='emp_code.identification_id',string='Employee Code', tracking =True)
    unit_elc = fields.Many2many(related='emp_code.unit_name_hr',string='Unit', tracking =True)
    department = fields.Many2one(related='emp_code.department_id',string='Department', tracking =True)
    designation = fields.Many2one(related='emp_code.job_id',string="Designation", tracking =True)
    general_category = fields.Many2one(related='emp_code.emp_cat',string='General Category', tracking =True)
    work_category = fields.Selection(related='emp_code.emp_category',string="Work Category", tracking =True)
    date_of_join = fields.Date(related="emp_code.date_join",string="Join Date", tracking =True)
    transfer_effective_date =fields.Date(string='Effective Date', tracking =True)
    effective_date = fields.Date(string='Effective Date', tracking =True)
    from_unit_elc = fields.Many2many(related='emp_code.unit_name_hr',string='From Unit', tracking =True)
    from_department = fields.Many2one(related='emp_code.department_id',string='From Department', tracking =True)
    remarks = fields.Text(string='Remarks', tracking =True)
    remarks2 = fields.Text(string='Remarks', tracking =True)
    remarks3 = fields.Text(string='Remarks', tracking =True)
    remarks4 = fields.Text(string='Remarks', tracking =True)
    remarks5 = fields.Text(string='Remarks', tracking =True)
    remarks6 = fields.Text(string='Remarks', tracking =True)
    remarks7 = fields.Text(string='Remarks', tracking =True)
    remarks8 = fields.Text(string='Remarks', tracking =True)
    remarks9 = fields.Text(string='Remarks', tracking =True)
    remarks10 = fields.Text(string='Remarks', tracking =True)
    remarks11 = fields.Text(string='Remarks', tracking =True)
    reason = fields.Char(string='Reason for Trainees to Probation', tracking =True)
    reason2 = fields.Char(string='Reason for Probation to Confirmation', tracking =True)
    reason3 = fields.Char(string='Reason for Extension', tracking =True)
    reason4 = fields.Char(string='Reason for Transfer', tracking=True)
    reason5 = fields.Char(string='Reason', tracking=True)
    reason6 = fields.Char(string='Reason for Extension', tracking=True)
    reason7 = fields.Char(string='Reason for Extension', tracking=True)
    to_unit_emp = fields.Many2many('unit.master',string='To Unit', tracking =True)
    to_department = fields.Many2one('hr.department',string='To Department', tracking =True)
    state = fields.Selection(([
        ('new', 'New'),
        ('submit', 'Submit'),
        ('hr', 'Hr'),
        ('hod', 'Hod'),
        ('approved', 'Approved'),
        ('post', 'Post'),
        ('reject', 'Reject'),
    ]), string="Status",default='new',tracking=True)
    probation_date = fields.Date(string='Probation Start Date', tracking =True)
    confirm_date = fields.Date(string='Confirmation Date', tracking =True)
    confirm_effective_date = fields.Date(string='Effective Date', tracking =True)
    no_of_months = fields.Integer(string='No of Months Extension')
    no_of_months_extension = fields.Char(string='No of Months Extension')
    no_of_months_extension_service = fields.Char(string='No of Months Extension')
    extension_start_date = fields.Date(string='Extension Start Date', tracking =True)
    extension_start_date_tr = fields.Date(string='Extension Start Date', tracking =True)
    extension_start_date_ex = fields.Date(string='Extension Start Date', tracking =True)
    section_to_elc = fields.Many2many('section.master',string='To Section', tracking =True)
    section_from_elc = fields.Many2many(related ='emp_code.section_name_hr',string='From Section', tracking =True)
    section_from_top_elc = fields.Many2many(related ='emp_code.section_name_hr',string='Section', tracking =True)
    new_designation = fields.Many2one('hr.job',string='New Designation', tracking =True)
    new_re_designation = fields.Many2one('hr.job',string='New Designation', tracking =True)
    promotion_effective_date = fields.Date(string='Effective Date', tracking =True)
    increment_effective_date = fields.Date(string='Effective Date', tracking =True)
    re_designation_effective_date = fields.Date(string='Effective Date', tracking =True)
    company = fields.Many2one('res.company',string="Company", tracking =True)
    company_to = fields.Many2one('res.company',string="To Company", tracking =True)
    company_from = fields.Many2one('res.company',string="From Company", tracking =True)
    salary_structure = fields.Float(string="Salary Structure", tracking =True)
    transaction_date_tp = fields.Date('Transaction Date', readonly=True, tracking =True)
    transaction_date_pc = fields.Date('Transaction Date', readonly=True, tracking =True)
    transaction_date_pe = fields.Date('Transaction Date', readonly=True, tracking =True)
    transaction_date_ex_pr = fields.Date('Transaction Date', readonly=True, tracking =True)
    transaction_date_tr = fields.Date('Transaction Date', readonly=True, tracking =True)
    transaction_date_pr = fields.Date('Transaction Date', readonly=True, tracking =True)
    transaction_date_in = fields.Date('Transaction Date', readonly=True, tracking =True)
    transaction_date_rd = fields.Date('Transaction Date', readonly=True, tracking =True)
    transaction_date_ex_sr = fields.Date('Transaction Date', readonly=True, tracking =True)
    transaction_date = fields.Date(string='Transaction Date',compute='compute_transaction_date_field')

    @api.onchange('confirm_effective_date','transfer_effective_date','promotion_effective_date','increment_effective_date','re_designation_effective_date')
    def _onchange_effective_date_form(self):
        if self.process == 'prob_to_conf':
            self.effective_date = self.confirm_effective_date
        elif self.process == 'transfers':
            self.effective_date = self.transfer_effective_date
        elif self.process == 'promotion':
            self.effective_date = self.promotion_effective_date
        elif self.process == 'increments':
            self.effective_date = self.increment_effective_date
        elif self.process == 're_designation':
            self.effective_date = self.re_designation_effective_date


    def button_submit(self):
        self.state = 'submit'

    def button_hr(self):
        self.state = 'hr'


    def compute_transaction_date_field(self):
        for rec in self:
            if rec.process == 'tran_prob':
                rec.transaction_date = rec.transaction_date_tp
            elif rec.process == 'prob_to_conf':
                rec.transaction_date = rec.transaction_date_pc
            elif rec.process == 'prob_ext':
                rec.transaction_date = rec.transaction_date_pe
            elif rec.process == 'transfers':
                rec.transaction_date = rec.transaction_date_tr
            elif rec.process == 'promotion':
                rec.transaction_date = rec.transaction_date_pr
            elif rec.process == 'increments':
                rec.transaction_date = rec.transaction_date_in
            elif rec.process == 're_designation':
                rec.transaction_date = rec.transaction_date_rd
            elif rec.process == 'extension_of_training':
                rec.transaction_date = rec.transaction_date_ex_pr
            elif rec.process == 'service_extension':
                rec.transaction_date = rec.transaction_date_ex_sr

    def button_hod(self):
        if self.process == 'tran_prob':
            self.state = 'approved'
            self.transaction_date_tp = date.today()
        elif self.process == 'prob_to_conf':
            self.state = 'approved'
            self.transaction_date_pc = date.today()
        elif self.process == 'prob_ext':
            self.state = 'approved'
            self.transaction_date_pe = date.today()
        elif self.process == 'transfers':
            self.state = 'approved'
            self.transaction_date_tr = date.today()
        elif self.process == 'promotion':
            self.state = 'approved'
            self.transaction_date_pr = date.today()
        elif self.process == 'increments':
            self.state = 'approved'
            self.transaction_date_in = date.today()
        elif self.process == 're_designation':
            self.state = 'approved'
            self.transaction_date_rd = date.today()
        elif self.process == 'extension_of_training':
            self.state = 'approved'
            self.transaction_date_ex_pr = date.today()
        elif self.process == 'service_extension':
            self.state = 'approved'
            self.transaction_date_ex_sr = date.today()

    def button_reject(self):
        self.state = 'reject'

    @api.onchange('company')
    def onchange_company(self):
        self.company_from = self.company

    def record_post(self):
        self.state = 'post'
        data = self.env['hr.employee'].search([('name', '=', self.emp_name)])
        records = []
        for rec in self:
            if rec.process == 'transfers':
                records = {
                    'section_name_hr': rec.section_to_elc,
                    'unit_name_hr': rec.to_unit_emp,
                    'department_id': rec.to_department.id
                }
                data.write(records)
            elif rec.process == 'promotion':
                records = {
                    'job_id': rec.new_designation.id
                }
                data.write(records)
            elif rec.process == 're_designation':
                records = {
                    'job_id': rec.new_re_designation.id
                }
                data.write(records)
        return records

    @api.model
    def get_data(self):
        total_tran_prob = self.env['employee.life.cycle'].search([('process', '=', 'tran_prob'), ('state', 'in', ['new', 'submit', 'hr', 'hod'])])
        total_prob_to_conf = self.env['employee.life.cycle'].search([('process', '=', 'prob_to_conf'), ('state', 'in',  ['new', 'submit', 'hr', 'hod'])])
        total_prob_ext = self.env['employee.life.cycle'].search([('process', '=', 'prob_ext'), ('state', 'in',  ['new', 'submit', 'hr', 'hod'])])
        total_transfers = self.env['employee.life.cycle'].search([('process', '=', 'transfers'), ('state', 'in',  ['new', 'submit', 'hr', 'hod'])])
        total_promotion = self.env['employee.life.cycle'].search([('process', '=', 'promotion'), ('state', 'in',  ['new', 'submit', 'hr', 'hod'])])
        total_increments = self.env['employee.life.cycle'].search([('process', '=', 'increments'), ('state', 'in',  ['new', 'submit', 'hr', 'hod'])])
        total_re_designation = self.env['employee.life.cycle'].search([('process', '=', 're_designation'), ('state', 'in',  ['new', 'submit', 'hr', 'hod'])])

        final_tran_prob = self.env['employee.life.cycle'].search([('process', '=', 'tran_prob'), ('state', 'in', ['approved', 'post'])])
        final_prob_to_conf = self.env['employee.life.cycle'].search([('process', '=', 'prob_to_conf'), ('state', 'in', ['approved', 'post'])])
        final_prob_ext = self.env['employee.life.cycle'].search([('process', '=', 'prob_ext'), ('state', 'in', ['approved', 'post'])])
        final_transfers = self.env['employee.life.cycle'].search([('process', '=', 'transfers'), ('state', 'in', ['approved', 'post'])])
        final_promotion = self.env['employee.life.cycle'].search([('process', '=', 'promotion'), ('state', 'in', ['approved', 'post'])])
        final_increments = self.env['employee.life.cycle'].search([('process', '=', 'increments'), ('state', 'in', ['approved', 'post'])])
        final_re_designation = self.env['employee.life.cycle'].search([('process', '=', 're_designation'), ('state', 'in', ['approved', 'post'])])

        total_incident = self.env['employee.disciplinary'].search([])
        total_incident_progress = self.env['manage.incident'].search([('state', '=', 'in_progress')])
        total_incident_approved = self.env['manage.incident'].search([('state', '=', 'closed')])
        return {
            'total_tran_prob': len(total_tran_prob),
            'total_prob_to_conf': len(total_prob_to_conf),
            'total_prob_ext': len(total_prob_ext),
            'total_transfers': len(total_transfers),
            'total_promotion': len(total_promotion),
            'total_increments': len(total_increments),
            'total_re_designation': len(total_re_designation),
            'final_tran_prob': len(final_tran_prob),
            'final_prob_to_conf': len(final_prob_to_conf),
            'final_prob_ext': len(final_prob_ext),
            'final_transfers': len(final_transfers),
            'final_promotion': len(final_promotion),
            'final_increments': len(final_increments),
            'final_re_designation': len(final_re_designation),
            'total_incident': len(total_incident),
            'total_incident_progress': len(total_incident_progress),
            'total_incident_approved': len(total_incident_approved),
        }


class CareerHistory(models.Model):
    _inherit = "hr.employee"
    # _rec_name = 'identification_id'

    career_history_field = fields.One2many('employee.life.cycle', 'emp_name', domain=[('state', '=', 'post')])

    # @api.model
    # def create(self, vals):
    #     employee = super(CareerHistory, self).create(vals)
    #     if employee:
    #         template = self.env.ref('employee_life_cycle.new_employee_email_template')
    #         if template:
    #             template.send_mail(employee.id, force_send=True)
    #             print('sent')
    #     return employee




class ResCompany(models.Model):
    _inherit = 'res.company'

    employee_emails = fields.Many2many('hr.employee', string='Employee Emails For Alerts')

    def get_employee_emails(self):
        return ', '.join(self.employee_emails.mapped('work_email'))





