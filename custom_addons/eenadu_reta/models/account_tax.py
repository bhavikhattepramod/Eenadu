from odoo import models

class AccountTaxReta(models.Model):
    _inherit = 'account.tax'

    #for rounding off total amount in reta and classified
    # def _prepare_tax_totals(self, base_lines, currency, tax_lines=None):
        # res = super(AccountTaxReta, self)._prepare_tax_totals(base_lines, currency, tax_lines=None)
        # sale_order_line_id = base_lines[0].get('record')
        # if sale_order_line_id.order_id.reta_bool_field == True or sale_order_line_id.order_id.classified_bool_field == True:
        #     res.update({
        #         'formatted_amount_total': '₹ ' + str(round(res['amount_total'])) + '.00'
        #     })
        # return res