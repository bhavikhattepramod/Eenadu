from odoo import models, fields, _, api
class Holidays(models.Model):

    _name = "hr.holidays.cancel"
    _description = "Leave Cancellation"
    # _order = "type desc, date_from desc"
    _inherit = ['mail.thread','mail.activity.mixin']

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    name = fields.Char('Description')
    state = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm', 'To Approve'),
        ('refuse', 'Refused'),
        ('validate', 'Approved')
    ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft',
        help="The status is set to 'To Submit', when a holiday cancel request is created." +
             "\nThe status is 'To Approve', when holiday cancel request is confirmed by user." +
             "\nThe status is 'Refused', when holiday request cancel is refused by manager." +
             "\nThe status is 'Approved', when holiday request cancel is approved by manager.")
    report_note = fields.Text('HR Comments')
    holiday = fields.Many2one("hr.leave", string="Leaves", required=True, domain="[('state', '=', 'validate')]")
    employee_id = fields.Many2one('hr.employee', string='Employee', index=True, readonly=True,
                                  states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
                                  default=_default_employee)
    emp_unit_leave = fields.Many2many(related='employee_id.unit_name_hr', string='Unit Name')
    emp_section_leave = fields.Many2many(related='employee_id.section_name_hr', string='Section Name')
    emp_dep_leave = fields.Many2one(related='employee_id.job_id', string='Department Name')
    leave_date_from_self = fields.Date(related='holiday.request_date_from', string='Date From')
    leave_date_to_self = fields.Date(related='holiday.request_date_to', string='Date To')
    leaves_count = fields.Float(related='holiday.number_of_days_display', string='Number of Days')

    def action_approve(self):
        for record in self:
            record.holiday.action_refuse()
            record.write({'state': 'validate'})

    def action_refuse(self):
        for record in self:
            record.write({'state': 'refuse'})

    def action_confirm(self):
        """
        Confirm leave cancel requests and send a mail to the concerning department head.
        :return:
        """
        for record in self:
            if record.employee_id and record.employee_id.parent_id and record.employee_id.parent_id.work_email:
                vals = {
                        'email_to': record.employee_id.parent_id.work_email,
                        'subject': 'Leave Cancel Request: From {employee} , {description}'
                                    .format(employee=record.employee_id.name, description=record.name),
                        'body_html': """
                                    <p>
                                        Hello Mr {manager},
                                    </p>
                                    <p>
                                        There is a leave cancellation request on an approved leave {leave}
                                    </p>
                                    <p>
                                        Thank You.
                                    </p>
                                """.format(manager=record.employee_id.parent_id.name, leave=record.holiday.display_name)}
                mail = self.env['mail.mail'].sudo().create(vals)
                mail.send()
            record.write({'state': 'confirm'})




