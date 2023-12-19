from odoo import api, fields, models


class DepositWizard(models.TransientModel):
    _name = 'deposit.wizard'

    add_deposit = fields.Float('Deposit')

    # for adding the addition deposit amt to the total outstanding
    # and create credit note based on add_deposit and creating line in deposit history
    def add_amt(self):
        active_id = self._context.get('active_id')
        deposit = self.env['account.deposit'].browse(active_id)
        if deposit.paid_bool == False:
            deposit.update({
                'total_outstanding': deposit.total_outstanding + self.add_deposit,

            })
        # elif deposit.paid_bool == True:
        #     deposit.update({
        #         'total_outstanding': deposit.total_outstanding + self.add_deposit
        #     })

        journal = self.env['account.journal'].search([('is_deposit', '=', True)])
        product = self.env['product.product'].search([('is_deposit', '=', True)])
        line_vals = {
            'product_id': product.id,
            'price_unit': self.add_deposit,
            'tax_ids': False,
        }
        vals = {
            'move_type': 'out_refund',
            'journal_id': journal.id,
            'partner_id': deposit.partner_id.id,
            'account_deposit': deposit.id,

            # 'deposit_ref': rec.id,
            'invoice_line_ids': [(0, 0, line_vals)]
        }
        self.env['account.move'].create(vals).action_post()
