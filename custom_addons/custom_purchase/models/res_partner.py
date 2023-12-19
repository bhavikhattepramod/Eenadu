# -*- coding: utf-8 -*-

from odoo import api, fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'

    is_newsprint_agent = fields.Boolean("Is Newsprint Agent?")
    is_clearing_agent = fields.Boolean("Is Clearing Agent")
    cust_seq = fields.Char(string='Agent Sequence', readonly=True, copy=False, default='New')

