# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class JobPositionApproved(models.Model):
    _name = "job.position.approved"
    _description = "Job Positions Approved"

    job_position_request_ids = fields.Many2many("job.position.request", readonly=True)
    reason = fields.Text("Remarks", required=True)

    def button_approved(self):
        for record in self:
            for job_position_request_id in record.job_position_request_ids:
                job_position_request_id.approved_reason = record.reason
                job_position_request_id.approve_request()
