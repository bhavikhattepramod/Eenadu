# -*- coding: utf-8 -*-
from odoo import _, _lt, api, fields, models


class Warehouse(models.Model):
    _inherit = "stock.warehouse"

    code = fields.Char('Short Name', required=True, help="Short name used to identify your warehouse")