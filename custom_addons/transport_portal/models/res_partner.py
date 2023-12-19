from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class VendorApproval(models.Model):
    _inherit = 'res.partner'

    is_transport_vendor = fields.Boolean(string="Is Transport Vendor?")
    is_active_vendor = fields.Boolean(string="Active Vendor")
    vendor_state = fields.Selection([
        ('draft', 'Draft'),
        ('validated', 'Validated'),
        ('approved', 'Approved'),
        ('reject', 'Reject'),
    ], default='draft', help="The states are in Draft,Validated and Approved for Transport Vendor Approve")

    def action_vendor_validate(self):
        """
            customer or vendor can validate
        """
        for rec in self:
            rec.vendor_state = 'validated'
            rec.write({'vendor_state': 'validated'})

    def action_vendor_approve(self):
        """
            customer or vendor can Approve
        """
        for rec in self:
            rec.vendor_state = 'approved'
            rec.is_active_vendor = True
            rec.write({'vendor_state': 'approved'})

    def action_vendor_reject(self):
        """
            customer or vendor can Reject
        """
        for rec in self:
            rec.vendor_state = 'reject'
            rec.is_active_vendor = False
            rec.write({'vendor_state': 'reject'})

    def action_vendor_draft(self):
        """
        Reset To Draft and make vendor Inactive
        """
        for rec in self:
            rec.write({
                'vendor_state': 'draft',
                'is_transport_vendor': True,
                'is_active_vendor': False,
            })