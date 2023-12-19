from odoo import fields, api, models
from datetime import datetime, timedelta

import datetime


class VendorBillsApproval(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('circulation_incharge', 'Circulation Incharge'),
            ('unit_incharge', 'Unit Incharge'),
            ('accounts_incharge', 'Accounts Incharge'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='draft',
    )

    def action_approve_circulation_incharge(self):
        for res in self:
            res.state = 'circulation_incharge'

    def action_approve_unit_incharge(self):
        for res in self:
            res.state = 'unit_incharge'

    def action_approve_accounts_incharge(self):
        for res in self:
            res.state = 'accounts_incharge'


class VendorBillsOfTransportation(models.Model):
    _inherit = 'account.move.line'

    vehicle_no = fields.Many2one('transport.vehicle', string="Vehicle")
    drop_location = fields.Many2one('transport.routes', string="Drop Location")
    source_location = fields.Many2one('transport.routes', string="Source Location")
    destination_location = fields.Many2one('transport.routes', string="Destination Location")
    distance = fields.Float(string="Distance (KM)")
    hours = fields.Float(string="Hours")
    no_of_parcels = fields.Integer(string="No Of Parcels")
    drop_location_vehicle = fields.Char(string="Drop Location")


class TransportationBills(models.Model):
    _inherit = 'transport.entry.details'

    active = fields.Boolean('Active', default=True, tracking=True)

    def action_create_vendor_bills(self):
        current_date = fields.Date.today()
        one_month_ago = current_date - timedelta(days=30)
        vendor_bills = self.env['transport.entry.details'].search([('hand_off_date_time', '>=', one_month_ago),
                                                                   ('hand_off_date_time', '<=', current_date)])
        vendor_list = []
        for vendor in vendor_bills:
            if vendor.vehicle.partner_id.id not in vendor_list:
                vendor_list.append(vendor.vehicle.partner_id.id)
        product_type = self.env['product.product'].search([('is_transportation', '=', True)], limit=1)
        user = self.env.uid
        # Parse the date string into a date object
        user_id = self.env['res.users'].browse(user)
        for vendors in vendor_list:
            vendor = self.env['res.partner'].browse(vendors)
            invoice_line_list = []
            for vehicle in vendor_bills:
                if vehicle.vehicle.partner_id.id == vendor.id:
                    invoice_line_list.append((0, 0, {
                        'product_id': product_type.id,
                        'quantity': vehicle.distance,
                        'price_unit': product_type.list_price,
                        'name': product_type.name,
                        'vehicle_no': vehicle.vehicle.id,
                        'drop_location_vehicle': vehicle.location.name,
                        'distance': vehicle.distance,
                        'hours': vehicle.hours,
                        'no_of_parcels': vehicle.no_of_parcels,
                    }))
            invoice_vals = {
                'partner_id': vendor.id,
                'invoice_date': datetime.date.today(),
                'is_transportation': True,
                'move_type': 'in_invoice',  # Specify the invoice type (in_invoice for vendor invoice)
                'user_id': user_id.id,
                'line_ids': invoice_line_list,
            }

            self.env['account.move'].create(invoice_vals)




