from odoo import models, fields, api,_
from datetime import datetime as dt

class impdates(models.Model):
    _name='important.dates'

    name=fields.Char(string="Name")
    date=fields.Date(string="Date")
    type=fields.Selection([('event','Event'),('occasion','occasion')])
    date_month = fields.Char(string='Date Month')
    description= fields.Char(string="Event about it")

    # @api.depends('date')
    # def _get_date_month(self):
    #     self.date_month = dt.strptime(self.date,'%Y-%m-%d').strftime('%m')