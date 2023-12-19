from odoo import fields, models, api, _, exceptions
from odoo.fields import Command
from odoo.exceptions import UserError, ValidationError
import qrcode, base64
from io import BytesIO
from datetime import datetime, timedelta
import re


class CreateQuotationPayment(models.TransientModel):
    _name = 'create.quotation.payment'

    # @api.onchange('payee_mobile')
    # def _check_mob_length(self):
    #     for record in self:
    #         if record.payee_mobile and not record.payee_mobile.isdigit() or len(record.payee_mobile) > 10:
    #             raise ValidationError(_("Mobile number must be 10 digits or less and contain only numbers."))

    @api.onchange('payment_location')
    def _check_name(self):
        for record in self:
            if record.payment_location:
                if not re.match("^[a-zA-Z\s/.,\-_&]+$", record.payment_location):
                    raise ValidationError("Name must contain only alphabetical characters.")

    @api.constrains('payment_mode', 'payment_amount', 'payment_datetime', 'payee_mobile')
    def _check_payment_condition(self):
        for record in self:
            if record.payment_mode == 'cash' and record.payment_amount > 0:
                # Calculate the date without the time portion
                payment_date = record.payment_datetime

                # Find all records with the same payment date, mobile, and cash payment mode
                same_day_records = self.env['create.quotation.payment'].search([
                    ('payee_mobile', '=', record.payee_mobile),
                    ('payment_datetime', '>=', payment_date),
                    ('payment_datetime', '<', payment_date + timedelta(days=1)),
                    ('payment_mode', '=', 'cash')
                ])

                # Calculate the total cash payments for the day for the specific customer
                total_amount = sum(same_day_records.mapped('payment_amount'))

                if total_amount + record.payment_amount > 200000.0:
                    raise exceptions.ValidationError(
                        "Cash payment for this customer has exceeded 2 lakhs for the day.")

    # Manually trigger the constraint validation for existing records
    def validate_existing_records(self):
        existing_records = self.search([])  # Fetch all existing records
        existing_records._check_payment_condition()  # Call the constraint validation method

    @api.model
    def default_get(self, values):
        result = super(CreateQuotationPayment, self).default_get(values)
        quotation_obj = self.env['sale.order'].browse(self._context.get('active_id'))
        result['order_id'] = quotation_obj.id
        result['quotation_total_amount'] = quotation_obj.cio_amount_due
        result['agent_id'] = quotation_obj.agent_name.id
        result['payee_mobile'] = quotation_obj.phone_number
        result['payee_name'] = quotation_obj.partner_id.name
        # result['payment_amount'] = quotation_obj.amount_total

        return result

    bank_name = fields.Char("Bank Name")
    order_id = fields.Many2one('sale.order', string='CIO Reference')
    payment_type = fields.Selection([
        ('full', 'Full Payment'),
        ('partial', 'Partial Payment')
    ], string="Payment Type")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    quotation_total_amount = fields.Monetary('CIO Total Amount', currency_field="currency_id")
    payment_amount = fields.Monetary('Payment Amount', currency_field="currency_id")
    remaining_amount = fields.Monetary('Remaining Amount', currency_field="currency_id")
    customer_id = fields.Selection([('client', 'Client'), ('third_party', 'ThirdParty')], string="Customer")

    payment_mode = fields.Selection([
        ('cash', 'Cash'),
        ('upi', 'UPI/QR'),
        ('bank', 'Bank - NEFT'),
        ('pdc', 'Cheque'),
    ], string='Payment Mode')
    payee_name = fields.Char('Remitter', readonly=True)
    attach_concent = fields.Binary('Attach Concent Form')
    payee_mobile = fields.Char('Payee Mobile')
    payment_datetime = fields.Date('Payment Date', default=lambda self: fields.Date.today())
    payment_location = fields.Char('Place')
    agent_id = fields.Many2one('res.partner', string='Agent')
    tnx_id = fields.Char('Transaction ID')
    utr_no = fields.Char('UTR No')
    payment_media = fields.Selection([
        ('gpay', 'Google Pay'),
        ('phonepe', 'Phonepe'),
        ('paytm', 'Paytm'),
        ('upi', 'UPI'),
    ], string='Payment Media')
    payment_confirmation_file = fields.Binary('Attachments')
    sender_acc_no = fields.Char("Sender Acc No")
    micr_no = fields.Char('MICR No')
    acc_branch_name = fields.Char("Branch Name")
    ifsc = fields.Char("IFSC")
    cheque_no = fields.Char('Cheque No')
    cheque_date = fields.Date('Cheque Date')

    cheque_expiry_date = fields.Date('Cheque Expiry Date')
    siginig_authority = fields.Char('Signing Authority')

    qr_code_image = fields.Binary(string='QR Code Image', compute='_compute_qr_code')
    active = fields.Boolean()

    def _get_default_html_content(self):
        return """
    		       <div style="text-align: left;">
    		           <h2 style="text-align: left;">Insertion of new section 269ST.</h2>
    		           <p style="text-align: justify;">84. After section 269SS of the Income-tax Act, the following section shall be inserted, namely:</p>
    		           <p style="text-align: justify;">'269ST. Mode of undertaking transactions.—No person shall receive an amount of two lakh rupees or more—</p>
    		           <p style="text-align: justify;margin-left:150px;">(a) in aggregate from a person in a day; or</p>
    		           <p style="text-align: justify;margin-left:150px;">(b) in respect of a single transaction; or</p>
    		           <p style="text-align: justify;margin-left:150px;">(c) in respect of transactions relating to one event or occasion from a person,</p>
    		           <p style="text-align: justify;">otherwise than by an account payee cheque or an account payee bank draft or use of electronic clearing system through a bank account:</p>
    		           <p style="text-align: justify;"><b>Provided</b> that the provisions of this section shall not apply to:</p>
    		           <ul style="text-align: left;">
    		               <li style="margin-left:150px;">any receipt by:</li>
    		               <ul style="text-align: left;">
    		                   <li style="margin-left:200px;">Government;</li>
    		                   <li style="margin-left:200px;">any banking company, post office savings bank, or co-operative bank;</li>
    		               </ul>
    		               <li style="margin-left:150px;">transactions of the nature referred to in section 269SS;</li>
    		               <li style="margin-left:150px;">such other persons or class of persons or receipts, which the Central Government may, by notification in the Official Gazette, specify.</li>
    		           </ul>
    		           <p style="text-align: justify;">Explanation.—For the purposes of this section,—</p>
    		           <p style="text-align: justify;margin-left:100px;">(a) "banking company" shall have the same meaning as assigned to it in clause (i) of the Explanation to section 269SS;</p>
    		           <p style="text-align: justify;margin-left:100px;">(b) "co-operative bank" shall have the same meaning as assigned to it in clause (ii) of the Explanation to section 269SS.</p>
    		       </div>
    		       """

    add_note = fields.Html(string="Add Note", default=_get_default_html_content, readonly="1", store=False)

    @api.onchange('cheque_date')
    def _compute_cheque_expiry_date(self):
        for record in self:
            if record.cheque_date:
                # Calculate the expiry date as 90 days in the future
                expiry_date = record.cheque_date + timedelta(days=90)
                record.cheque_expiry_date = expiry_date
            else:
                pass

    @api.depends('payment_amount')
    def _compute_qr_code(self):
        for record in self:
            upi_id = 'suriyaece1396-2@okhdfcbank'
            data = f"upi://{upi_id}?amount={record.payment_amount}"
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(upi_id)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Convert the image to a binary representation
            qr_code_buffer = BytesIO()
            img.save(qr_code_buffer, format="PNG")
            record.qr_code_image = base64.b64encode(qr_code_buffer.getvalue())

    @api.onchange('payment_type')
    def onchange_payment_type(self):
        if self.payment_type == 'partial':
            self.payment_amount = 0.00
        elif self.payment_type == 'full':
            self.payment_amount = self.order_id.cio_amount_due
        else:
            self.payment_amount = 0.00

    @api.onchange('payment_amount')
    def onchange_payment_amount(self):
        self.remaining_amount = self.quotation_total_amount - self.payment_amount

    def action_create_quotation_payment(self):
        if self.payment_amount == 0.00:
            raise UserError('Please enter the Payment Amount')
        else:
            # date_format = "%Y-%m-%d %H:%M:%S"
            # if datetime.strptime(self.payment_datetime, date_format).date() > datetime.now().date():
            # 	raise ValidationError('Payment can not be done for Future date')
            # else:
            if self.order_id.cio_paid_amount == 0.00:
                inv_line = []
                for line in self.order_id.reta_order_line:
                    inv_line.append((0, 0, {
                        'display_type': line.display_type or 'product',
                        'sequence': line.sequence,
                        'name': line.name,
                        'product_id': line.product_id.id,
                        'product_uom_id': line.product_uom.id,
                        'quantity': line.product_uom_qty,
                        'discount': line.discount,
                        'price_unit': line.price_unit,
                        'tax_ids': [Command.set(line.tax_id.ids)],
                        'sale_line_ids': [Command.link(line.id)],
                        'is_downpayment': line.is_downpayment,
                    }))

                create_values = {
                    'ref': self.order_id.client_order_ref or '',
                    'move_type': 'out_invoice',
                    'narration': self.order_id.note,
                    'currency_id': self.order_id.currency_id.id,
                    'campaign_id': self.order_id.campaign_id.id,
                    'medium_id': self.order_id.medium_id.id,
                    'source_id': self.order_id.source_id.id,
                    'team_id': self.order_id.team_id.id,
                    'partner_id': self.order_id.partner_invoice_id.id,
                    'partner_shipping_id': self.order_id.partner_shipping_id.id,
                    'fiscal_position_id': (
                            self.order_id.fiscal_position_id or self.order_id.fiscal_position_id._get_fiscal_position(
                        self.order_id.partner_invoice_id)).id,
                    'invoice_origin': self.order_id.name,
                    'invoice_payment_term_id': self.order_id.payment_term_id.id,
                    'invoice_user_id': self.order_id.user_id.id,
                    'payment_reference': self.order_id.reference,
                    'transaction_ids': [Command.set(self.order_id.transaction_ids.ids)],
                    'company_id': self.order_id.company_id.id,
                    'reta_bool_field': True,
                    'invoice_line_ids': inv_line
                }

                new_inv_obj = self.env['account.move'].create(create_values)

                new_inv_obj.action_post()

                payment_values = {
                    'payment_type': 'inbound',
                    'partner_id': self.order_id.partner_id.id,
                    'amount': self.payment_amount,
                    'company_id': self.order_id.company_id.id,
                    'sale_order_id': self.order_id.id,
                }

                new_payment_obj = self.env['account.payment'].create(payment_values)

                new_payment_obj.action_post()
            else:
                payment_values = {
                    'payment_type': 'inbound',
                    'partner_id': self.order_id.partner_id.id,
                    'amount': self.payment_amount,
                    'company_id': self.order_id.company_id.id,
                    'sale_order_id': self.order_id.id,
                }

                new_payment_obj = self.env['account.payment'].create(payment_values)

                new_payment_obj.action_post()

            payment_info_create_obj = self.env['payment.informations'].create({
                'agent_id': self.agent_id.id,
                'payment_type': self.payment_type,
                'payment_amount': self.payment_amount,
                'payment_mode': self.payment_mode,
                'payee_name': self.payee_name,
                'payee_mobile': self.payee_mobile,
                'payment_datetime': self.payment_datetime,
                'payment_location': self.payment_location,
                'tnx_id': self.tnx_id,
                'utr_no': self.utr_no,
                'payment_media': self.payment_media,
                'payment_confirmation_file': self.payment_confirmation_file,
                'sender_acc_no': self.sender_acc_no,
                'micr_no': self.micr_no,
                'bank_name': self.bank_name,
                'acc_branch_name': self.acc_branch_name,
                'ifsc': self.ifsc,
                'cheque_no': self.cheque_no,
                'cheque_date': self.cheque_date,
                'cheque_expiry_date': self.cheque_expiry_date,
                'siginig_authority': self.siginig_authority,
                'payment_information_id': self.order_id.id
            })

            self.order_id.cio_paid_amount += self.payment_amount

        # self.order_id.payment_mode = self.payment_mode
        # self.order_id.payee_name = self.payee_name
        # self.order_id.payee_mobile = self.payee_mobile
        # self.order_id.payment_datetime = self.payment_datetime
        # self.order_id.payment_location = self.payment_location
        # self.order_id.tnx_id = self.tnx_id
        # self.order_id.utr_no = self.utr_no
        # self.order_id.payment_media = self.payment_media
        # self.order_id.payment_confirmation_file = self.payment_confirmation_file
        # self.order_id.sender_acc_no = self.sender_acc_no
        # self.order_id.micr_no = self.micr_no
        # self.order_id.acc_branch_name = self.acc_branch_name
        # self.order_id.ifsc = self.ifsc
        # self.order_id.cheque_date = self.cheque_date
        # self.order_id.cheque_expiry_date = self.cheque_expiry_date
        # self.order_id.siginig_authority = self.siginig_authority

        return {'type': 'ir.actions.act_window_close'}
