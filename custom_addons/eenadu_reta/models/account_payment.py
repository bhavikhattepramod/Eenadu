# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    sale_order_id = fields.Many2one('sale.order', string='Sale Order Ref')

    def action_open_expense_report(self):
        res = super(AccountPayment, self).action_open_expense_report()

        return res