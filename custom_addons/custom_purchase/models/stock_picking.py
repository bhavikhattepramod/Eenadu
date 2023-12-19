# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError



class Picking(models.Model):
    _inherit = "stock.picking"

    delivery_challan_id = fields.Many2one('distribute.shipments', string = "Delivery Challan No")
    is_distibution_picking = fields.Boolean('Is distribution?')
    invoice_id = fields.Many2one('account.move', string="Invoice No", compute='compute_invoice_id')
    vendor_partner_id = fields.Many2one('res.partner', string="Vendor Name")
    vendor_bill_no = fields.Char('Vendor Bill No')
    vendor_bill_date = fields.Date('Vendor Bill Date')
    vendor_bill_accounting_date = fields.Date('Vendor Bill Accounting Date')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    vendor_bill_amount = fields.Monetary('Amount', currency_field="currency_id")

    lorry_no = fields.Char('Lorry No')
    lr_no = fields.Char('LR No')
    lr_date = fields.Date('LR Date')
    bill_no = fields.Char('Bill No')
    bill_date = fields.Date('Bill Date')

    # def button_validate(self):
    #     # OVERRIDE
    #     res = super(Picking, self).button_validate()
    #     po_obj = self.env['purchase.order'].search([('name', '=', self.origin)])
    #     if po_obj:
    #         if po_obj.ship_onboard_count == 0:
    #             raise ValidationError('Ship On-Board is not created!\nPlease complete the Ship On-board before validating the shipment')

    @api.depends('origin')
    def compute_invoice_id(self):
        for rec in self:
            purchase_obj = self.env['purchase.order'].search([('name', '=', str(rec.origin))])
            if purchase_obj:
                for line in purchase_obj.order_line:
                    for inv_line in line.invoice_lines:
                        rec.invoice_id = inv_line.move_id.id
                rec.vendor_partner_id = rec.invoice_id.partner_id.id
                rec.vendor_bill_no = rec.invoice_id.name
                rec.vendor_bill_date = rec.invoice_id.invoice_date
                rec.vendor_bill_accounting_date = rec.invoice_id.date
                rec.vendor_bill_amount = rec.invoice_id.amount_total
            else:
                rec.invoice_id = None
                rec.vendor_partner_id = rec.invoice_id.partner_id.id
                rec.vendor_bill_no = rec.invoice_id.name
                rec.vendor_bill_date = rec.invoice_id.invoice_date
                rec.vendor_bill_accounting_date = rec.invoice_id.date
                rec.vendor_bill_amount = rec.invoice_id.amount_total

    def action_create_landing_cost(self):
        ctx = dict()

        ctx = ({
            'default_picking_ids': [self.id],
        })

        form_id = self.env.ref('stock_landed_costs.view_stock_landed_cost_form').id

        return {
            'name': _('Landing Costs'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.landed.cost',
            'views_id': False,
            'views': [(form_id or False, 'form')],
            'target': 'new',
            'context': ctx,
        }