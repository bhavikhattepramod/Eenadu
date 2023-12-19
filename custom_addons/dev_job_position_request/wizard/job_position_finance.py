# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class JobPositionFinanceApproved(models.Model):
    _name = "job.position.finance_approve"
    _description = "Job Positions Finance Approved"

    job_position_request_ids = fields.Many2many("job.position.request", readonly=True)
    reason = fields.Text("Remarks", required=True)

    def button_to_approve(self):
        for record in self:
            for job_position_request_id in record.job_position_request_ids:
                job_position_request_id.approved_reason = record.reason
                job_position_request_id.approve_finance()