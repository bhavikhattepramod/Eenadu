from odoo import fields,api,models,_


class IncentiveWizard(models.TransientModel):
    _name = 'incentive.wizard'

    def _default_journal_id(self):
        return self.env["account.journal"].search(
            [("type", "=", "purchase"), ("company_id", "=", self.env.company.id)],
            limit=1,
        )

    journal_id = fields.Many2one(
        comodel_name="account.journal",
        required=True,
        domain="[('type', '=', 'purchase')]",
        default=lambda self: self._default_journal_id(),
    )
    company_id = fields.Many2one(
        comodel_name="res.company", related="journal_id.company_id", readonly=True
    )
    date = fields.Date(default=fields.Date.context_today)
    product_id = fields.Many2one(
        string="Product for invoicing", comodel_name="product.product", required=True
    )

    def button_create(self): # method to create payment in wizard
        active_id = self._context.get('active_id')
        incentive = self.env['partner.incentive'].browse(active_id)
        account_move = self.env['account.move'].search([])

        for lines in incentive.incentive_line:
            if lines.recieved_payment >= lines.target_amt:
                account_move.create({
                    'move_type': 'in_invoice',
                    'state': 'draft',
                    'invoice_line_ids': [(0, 0, {
                            'product_id': self.product_id.id,
                            'price_unit': lines.incentive_amt
                        })],
                    'partner_id': lines.employee_id.user_partner_id.id,
                    'invoice_date': self.date,
                    'journal_id': self.journal_id.id,
                    'incentive_ref' : incentive.id,
                })

        incentive.incentive_state = 'paid'  # line of code to move the stage
