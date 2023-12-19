from odoo import fields, models, api, _

class ChangeRejectSchedule(models.TransientModel):
    _name = 'change.reject.scheduling.line'


    @api.model
    def default_get(self, fields_name):
        res = super(ChangeRejectSchedule, self).default_get(fields_name)
        active_id = self._context.get('active_id')

        schedule_line_obj = self.env['scheduling.lines'].browse(active_id)

        if schedule_line_obj:
            res['scheduling_line_id'] = schedule_line_obj.id

        return res

    scheduling_line_id = fields.Many2one('scheduling.lines', string="Scheduling Line")
    action_to_perform = fields.Selection([
        ('change', 'Change Date'),
        ('reject', 'Reject')
        ], string="Action", default='change')
    updation_date = fields.Date('New Date')
    rejected_reason = fields.Char('Reject Reason')

    def action_update_schedule(self):
        if self.scheduling_line_id:
            if self.action_to_perform == 'change':
                self.scheduling_line_id.publish_date = self.updation_date
                self.scheduling_line_id.rejected_reason = self.rejected_reason
                self.scheduling_line_id.scheduling_status = 'approved'
            else:
                self.scheduling_line_id.publish_date = self.updation_date
                self.scheduling_line_id.rejected_reason = self.rejected_reason
                self.scheduling_line_id.scheduling_status = 'rejected'


        return {'type': 'ir.actions.act_window_close'}