from odoo import models, api, fields, _
from datetime import datetime, timedelta


class MrvTemplate(models.Model):
    _name = 'mrv.template'

    agency_code = fields.Integer('Agency Code Import')
    agency_name = fields.Char('Agency Name')
    previous_arrears = fields.Integer('Previous Arrears')
    classified_advt = fields.Integer('Classified Advertisement')
    display_advt = fields.Integer('Display Advertisement')
    digital = fields.Integer('Digital')
    receipts = fields.Integer('Receipts')
    late_payments = fields.Integer('Late Payments')
    disputed_amounts = fields.Integer('Disputed Amounts')
    cheque_dishonoured_amount = fields.Integer('Cheque Dishonoured Amount')
    next_month = fields.Integer('Next Month')
    next_to_nextmonth = fields.Integer('Next to Next Month')
    cash_carry_billing = fields.Integer('Cash Carry Billing')
    upto_3_months = fields.Integer('upto 3 months')
    upto_6_months = fields.Integer('upto 6 months')
    upto_12_months = fields.Integer('upto 12 months')
    over_one_year = fields.Integer('Over One Year')
    member_code = fields.Integer('Member Code')
    member_name = fields.Char('Member Name')
    mrv_no = fields.Char('MRV NO')
    record_date = fields.Datetime('created Date',default=datetime.today())

    @api.model
    def cron_delete_records(self):
        today = datetime.now()
        for rec in self.search([]):
            if rec.record_date and rec.record_date != False:
                expiration_date = rec.record_date + timedelta(days=4 * 30)
                if today >= expiration_date:
                    rec.unlink()
