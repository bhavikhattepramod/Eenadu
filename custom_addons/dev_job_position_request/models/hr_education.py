from odoo import models, fields, api
from datetime import datetime


class HrEducationType(models.Model):
    _name = "hr.education.type"
    _description = "HR Education Type"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string="Name of Degree")
