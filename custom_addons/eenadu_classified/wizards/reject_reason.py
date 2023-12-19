from odoo import api, fields, models


class RejectReason(models.Model):
    _name = 'reject.reason'

    reject_reason = fields.Char('Reject Reason')

    def rejection_reason(self):
        proof_reading_line_obj = self.env['proof.reading.line'].browse(self.env.context.get('active_id'))

        proof_reading_line_obj.reject_reason = self.reject_reason
        proof_reading_line_obj.status = 'reject'
