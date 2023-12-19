from odoo import fields, models, api


class ShiftManagement(models.Model):
    _name = 'shift.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Shift Name', tracking=True)
    shift_time_in = fields.Float(string='Shift Time In', tracking=True)
    shift_time_out = fields.Float(string='Shift Time Out', tracking=True)
    break_time_in = fields.Float(string='Break Time In', tracking=True)
    break_time_out = fields.Float(string='Break Time Out', tracking=True)
    grace_time_in = fields.Float(string='Grace Time In', tracking=True)
    grace_time_out = fields.Float(string='Grace Time Out', tracking=True)
    nsa_applicable = fields.Boolean(string='NSA Applicable')

    @api.onchange('break_time_in')
    def onchange_break_time_in(self):
        if self.break_time_in < self.shift_time_in:
            raise models.UserError('Break Time In Should between Shift Time In')

    @api.onchange('break_time_out')
    def onchange_break_time_out(self):
        if self.break_time_out > self.shift_time_out:
            raise models.UserError('Break Time Out Should between Shift Time Out')

    @api.onchange('grace_time_in')
    def onchange_grace_time_in(self):
        if self.grace_time_in < self.shift_time_in:
            raise models.UserError('Grace Time In Should between Shift Time In')

    @api.onchange('grace_time_out')
    def onchange_grace_time_out(self):
        if self.grace_time_out > self.shift_time_out:
            raise models.UserError('Grace Time Out Should between Shift Time Out')


class HrEmployeeTime(models.Model):
    _inherit = 'hr.employee'

    emp_time_id = fields.Many2one('shift.management', string='Employee Shift Timing', tracking=True)





