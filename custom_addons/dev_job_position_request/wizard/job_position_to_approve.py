# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class JobPositionToapprove(models.Model):
    _name = "job.position.to_approve"
    _description = "Job Positions to_approve"

    job_position_request_ids = fields.Many2many("job.position.request", readonly=True)
    reason = fields.Text("Remarks", required=True)

    def button_to_approve(self):
        for record in self:
            for job_position_request_id in record.job_position_request_ids:
                job_position_request_id.to_approve_reason = record.reason
                job_position_request_id.submit_to_manager()
