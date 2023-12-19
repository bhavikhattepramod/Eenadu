# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class JobPositionRejected(models.Model):
    _name = "job.position.rejected"
    _description = "Job Positions Rejected"

    job_position_request_ids = fields.Many2many("job.position.request", readonly=True)
    reason = fields.Text("Remarks", required=True)

    def button_rejected(self):
        for record in self:
            for job_position_request_id in record.job_position_request_ids:
                job_position_request_id.rejected_reason = record.reason
                job_position_request_id.reject_request()
