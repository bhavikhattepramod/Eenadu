from datetime import datetime, date
from odoo import fields, models, api


class NameChangeHrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_name_ids1 = fields.One2many('employee.disciplinary', 'disp_name')

    def name_get(self):
        result = []
        for record in self:
            if self.env.context.get('new_custom_name', False):
                result.append((record.id, "{} - {}".format(record.name, record.identification_id)))
            else:
                return super(NameChangeHrEmployee, self).name_get()
        return result


class EmployeeDisciplinary(models.Model):
    _name = 'employee.disciplinary'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'incident_type'

    incident_date = fields.Datetime(string='Incident Date & Time', tracking=True, default=datetime.now(), required=True)
    incident_type = fields.Many2one('incident.employee', string='Incident Type', tracking=True, required=True)
    incident_sub_type = fields.Many2many('incident.sub.employee', string='Incident Sub Type', tracking=True,
                                         required=True)
    incident_details = fields.Char(string='Incident Details', tracking=True, required=True)
    seized_items = fields.Char(string='Seized Items', tracking=True)
    incident_summary = fields.Text(string='Incident Summary', tracking=True, required=True)
    attach = fields.Many2many('ir.attachment', string='Attachments', tracking=True)
    emp_many_disp = fields.Many2many('hr.employee', 'new_custom_table', string='Employees Involved in the Incident',
                                     tracking=True, required=True)
    date_action = fields.Date(string='Date')
    employee = fields.Many2one('manage.incident')
    employee_code = fields.Many2one("hr.employee", string="Employee Name", required=True)
    employee_name = fields.Char(related="employee_code.identification_id")
    disp_name = fields.Many2one('hr.employee')

    @api.onchange('incident_type')
    def return_incident_sub_type(self):
        print(self.incident_type.sub_type)
        listed = []
        for recs in self.incident_type.sub_type:
            listed.append(recs.id)
        return {'domain': {'incident_sub_type': [('id', 'in', listed)]}}

    @api.constrains('incident_type')
    def create_manage_incidents(self):
        for rec in self:
            print('created')
            self.env['manage.incident'].create({
                'employee_disciplinary_id': rec.id,
            })

    @api.constrains('employee')
    def holds_hr_employee(self):
        for rec in self:
            rec.disp_name = rec.employee.employee_code_list1


class IncidentEmployee(models.Model):
    _name = 'incident.employee'

    name = fields.Char(string='Incident')
    sub_type = fields.Many2many('incident.sub.employee', string='Sub type')


class IncidentSubEmployee(models.Model):
    _name = 'incident.sub.employee'

    name = fields.Char(string='Incident Sub')


class EmployeeDisciplinaryLines(models.Model):
    _name = 'employee.disciplinary.line'
    _rec_name = 'hr_emp_many'

    emp_many = fields.Many2one('employee.disciplinary', string='Employee Disp')
    hr_emp_many = fields.Many2one('hr.employee', string='Employee Number')
    hr_emp_many_name = fields.Char(related='hr_emp_many.name', string='Employee Name')


class ManageIncident(models.Model):
    _name = 'manage.incident'

    # employee_name_ids = fields.One2many('employee.disciplinary','employee',string="Employee Name")
    employee_disciplinary_id = fields.Many2one("employee.disciplinary", string="Employee Code")
    employee_code_list1 = fields.Many2many("hr.employee", string="Employees Involved in the Incident",
                                           related='employee_disciplinary_id.emp_many_disp')
    incident_dat = fields.Datetime(related='employee_disciplinary_id.incident_date', string='Incident Date & Time',
                                   tracking=True)
    employee_by_code = fields.Many2one(related='employee_disciplinary_id.employee_code',
                                       string="Reported By Employee Name")
    incident_sum = fields.Text(related='employee_disciplinary_id.incident_summary', string='Incident Summary',
                               tracking=True)
    incident_typ = fields.Many2one(related='employee_disciplinary_id.incident_type', string="Incident Type",
                                   tracking=True)
    incident_sub_typ = fields.Many2many(related='employee_disciplinary_id.incident_sub_type',
                                        string="Incident Sub Type", tracking=True)
    # corrective_action_emp_id = fields.Many2one(related='employee_disciplinary_id.corrective_action_id',
    #                                            string="Corrective Action", tracking=True)
    state = fields.Selection(([
        ('pending_inquiry', 'Pending Inquiry'),
        ('in_progress', 'In Process'),
        ('closed', 'Closed')
    ]), string="Status", default='pending_inquiry', tracking=True)
    emp_incident = fields.Many2one('hr.employee')
    employee_inquiry = fields.One2many('manage.incident.line', 'employee_inquiry_state')

    def button_in_progress(self):
        self.state = 'in_progress'

    def button_closed(self):
        self.state = 'closed'


class CorrectiveActions(models.Model):
    _name = "corrective.actions"

    name = fields.Char(string="Name")


class ManageIncidentLine(models.Model):
    _name = 'manage.incident.line'

    corrective_action_id = fields.Many2one('corrective.actions', string="Corrective Action", tracking=True,
                                           required=True)
    internal_panel = fields.Many2many('hr.employee', string="Internal Panel Members", tracking=True,
                                           required=True)
    external_panel = fields.Char(string="External Panel Members")
    due_date = fields.Date(string="Due Date")
    last_action_date = fields.Datetime(string="Last Action Date", compute='_compute_last_action_date',
                                       default=date.today())
    recommendation = fields.Char(string="Recommendation", tracking=True, required=True)
    venue = fields.Char(string='Venue')
    inquiry_summary = fields.Char(string='Inquiry Summary', tracking=True, required=True)
    is_guilty = fields.Selection(([
        ('yes', 'Yes'),
        ('no', 'No'),
    ]), string="Is the Employee Guilt of the Incident", default='no', tracking=True)
    inquiry_date = fields.Datetime(string="Inquiry Date and Time", required=True)
    employee_inquiry_state = fields.Many2one('manage.incident')

    @api.depends('inquiry_date')
    def _compute_last_action_date(self):
        for line in self:
            if not line.employee_inquiry_state or line == line.employee_inquiry_state.employee_inquiry[0]:
                line.last_action_date = False
            else:
                previous_line = line.employee_inquiry_state.employee_inquiry.filtered(lambda l: l.inquiry_date < line.inquiry_date)
                sorted_previous_line = previous_line.sorted(key=lambda l: l.inquiry_date, reverse=True)
                if sorted_previous_line:
                    line.last_action_date = sorted_previous_line[0].inquiry_date
                else:
                    line.last_action_date = False
