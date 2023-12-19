from odoo import fields, models, api, _
import math
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    advertisement_line_ids = fields.One2many('advertisement.content.line', 'advertisement_line_id',
                                             string="Advertisement line ref")
    advertisement_language = fields.Selection([
        ('telugu', 'Telugu'),
        ('english', 'English'),
        ('english_telugu', 'English & Telugu')
    ], string="Advertisement Language", default='telugu')

    scheduling_line_ids = fields.One2many('scheduling.lines', 'scheduling_line_id', string="Scheduling Lines ref")
    is_schedule_done = fields.Boolean('Is Schedule Done?', default=False, compute="compute_done_schedule")
    scheduling_date = fields.Selection([
        ('specific_date', 'Single Insertion'),
        ('multiple_date', 'Multiple Insertion')], string="Publish Type")
    specific_date = fields.Date('Single Insertion')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    publish_start_date = fields.Date('Publish Start Date')
    no_of_occurence = fields.Integer('Number Of Occurance')
    time_interval = fields.Integer('Time Interval')

    sale_related_document_ids = fields.One2many('sale.related.documents', 'sale_related_document_id',
                                                string='AD-Material')

    is_terms_and_conditions = fields.Boolean('Accept Terms and conditions')
    is_consent_form = fields.Boolean('Accept Consent')

    cio_paid_amount = fields.Monetary('Amount Paid', currency_field='currency_id')
    cio_amount_due = fields.Monetary('Amount Due', currency_field='currency_id', compute="_compute_cio_amount_due")

    is_fully_paid = fields.Boolean('Is CIO Paid?', compute='_compute_is_cio_paid')

    cio_payment_count = fields.Integer('Payment Count', compute='_compute_payemnt_count')

    mob_seq_number = fields.Char('Mobile Sequence')
    mob_seq_id = fields.Integer('Mobile ID')
    is_online = fields.Boolean('Is Online')

    is_created_from_app = fields.Boolean('Is created from Mobile?', default=False)

    payment_mode = fields.Selection([
        ('cash', 'Cash'),
        ('upi', 'UPI/QR'),
        ('bank', 'Bank - NEFT'),
        ('pdc', 'Cheque'),
    ], string='Payment Mode')

    payee_name = fields.Char('Payee Name')
    payee_mobile = fields.Char('Payee Mobile')
    payment_datetime = fields.Datetime('Payment Date')
    payment_location = fields.Char('Place')
    # agent_id = fields.Many2one('Agent')
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
    bank_name = fields.Char("Bank Name")
    acc_branch_name = fields.Char("Branch Name")
    ifsc = fields.Char("IFSC")
    cheque_no = fields.Char('Cheque No')
    cheque_date = fields.Date('Cheque Date')
    cheque_expiry_date = fields.Date('Cheque Expiry Date')
    siginig_authority = fields.Char('Signing Authority')

    payment_information_ids = fields.One2many('payment.informations', 'payment_information_id',
                                              string="Payment Information Lines")

    is_scheduling_cancelled = fields.Boolean('Is Scheduling Cancelled?', default=False)

    tracking_description = fields.Char(string='Adv Description', tracking=True)

    multi_publish_date = fields.One2many('multi.publish.date', 'sale_order')

    # nap_bool_field = Boolean()

    @api.onchange('multi_publish_date')
    def onchange_multi_publish_date(self):
        self.no_of_occurence = len(self.multi_publish_date)

    @api.onchange('to_date')
    def onchange_to_date(self):
        if self.scheduling_date == 'multiple_date':
            if self.to_date <= self.from_date:
                raise UserError('To Date should be greater From Date')

    @api.onchange('advertisement_line_ids')
    def onchange_advertisement_description(self):
        self.tracking_description = self.advertisement_line_ids.advertisement_description

    @api.depends('scheduling_line_ids')
    def _compute_scheduling_cancelled(self):
        for rec in self:
            is_scheduling_cancelled = False
            i = 0
            if len(rec.scheduling_line_ids) != 0:
                for line in rec.scheduling_line_ids:
                    if line.scheduling_status == 'rejected':
                        i += 1
                if i == len(rec.scheduling_line_ids):
                    is_scheduling_cancelled = True
                if rec.reta_bool_field and is_scheduling_cancelled == True:
                    rec.is_scheduling_cancelled = is_scheduling_cancelled
                    rec.state = 'cancel'
                    rec.reta_state = 'cancel'
                else:
                    rec.is_scheduling_cancelled = is_scheduling_cancelled
                    rec.state = rec.state
                    rec.reta_state = rec.reta_state
            else:
                rec.is_scheduling_cancelled = is_scheduling_cancelled
                rec.state = rec.state
                rec.reta_state = rec.reta_state

    # @api.constrains('is_scheduling_cancelled')
    # @api.onchange('is_scheduling_cancelled')
    # def _onchange_is_scheduling_cancelled(self):
    #     print(self,'--Onchange--')
    #     if self.is_scheduling_cancelled:
    #         print(self.is_scheduling_cancelled,'--scheduling cancel--')
    #         if self.reta_bool_field:
    #             print(self.reta_bool_field,'--reta bool field--')
    #             print(self.state,'--state--')
    #             print(self.reta_state,'--reta_state--')
    #             self.state = 'cancel'
    #             self.reta_state = 'cancel'
    #         elif self.classified_bool_field:
    #             print(self.classified_bool_field,'--reta bool field--')
    #             print(self.state,'--state--')
    #             print(self.classified_state,'--classified_state--')
    #             self.state = 'cancel'
    #             self.classified_state = 'cancel'

    @api.constrains('sale_order_template_id')
    @api.onchange('sale_order_template_id')
    def _onchange_sale_order_template_id(self):
        return super(SaleOrder, self)._onchange_sale_order_template_id()

    def _compute_payemnt_count(self):
        for rec in self:
            account_payment_obj = self.env['account.payment'].search([('sale_order_id', '=', rec.id)])

            rec.cio_payment_count = len(account_payment_obj)

    @api.depends('cio_paid_amount', 'amount_total')
    def _compute_cio_amount_due(self):
        for rec in self:
            rec.cio_amount_due = rec.amount_total - rec.cio_paid_amount

    @api.depends('cio_amount_due')
    def _compute_is_cio_paid(self):
        for rec in self:
            if rec.cio_amount_due == 0.00:
                rec.is_fully_paid = True
            else:
                rec.is_fully_paid = False

    @api.depends('scheduling_line_ids')
    def compute_done_schedule(self):
        for rec in self:
            if self.scheduling_line_ids:
                i = 0
                for line in rec.scheduling_line_ids:
                    if line.scheduling_status:
                        i += 1
                    else:
                        i = i
                if len(rec.scheduling_line_ids) == i:
                    rec.is_schedule_done = True
                else:
                    rec.is_schedule_done = False
            else:
                rec.is_schedule_done = False

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()

        # if self.reta_bool_field or self.classified_bool_field:
        #     if not self.is_terms_and_conditions and not self.is_consent_form:
        #         raise ValidationError('Please Accept the Consent Form and Terms&conditions')

        return result

    def open_consent_form(self):
        return

    # def add_order_line(self):
    #     for line in self.advertisement_line_ids:
    #         product_line = []
    #         product_present = False
    #         for order_line in self.classified_order_line:
    #             if order_line.product_id.id == self.product_id.id:
    #                 product_present = True
    #         if product_present == True:
    #             sale_order_line_obj = self.env['sale.order.line'].search([('product_id', '=', self.product_id.id),('order_id', '=', self.id)],limit=1)
    #             sale_order_line_obj.product_uom_qty = line.no_of_lines
    #         else:
    #             product_line.append((0, 0, {
    #                 'product_id': line.product_id.id,
    #                 'name': line.advertisement_description,
    #                 'product_uom_qty': line.no_of_lines,
    #                 'price_unit': line.product_id.list_price,
    #                 'product_uom': line.product_id.uom_id.id,
    #                 'order_id': self.id,
    #             }))
    #             self.classified_order_line = product_line

    def add_order_line(self):
        for line in self.advertisement_line_ids:
            product_line = []
            product_present = False
            for order_line in self.classified_order_line:
                if order_line.product_id.id == line.product_id.id:
                    product_present = True
            if product_present == True:
                sale_order_line_obj = self.env['sale.order.line'].search(
                    [('product_id', '=', self.product_id.id), ('order_id', '=', self.id)], limit=1)
                sale_order_line_obj.product_uom_qty = line.no_of_lines
                order_line.name = line.advertisement_description
                order_line.product_uom_qty = line.no_of_lines
                print('called condition')
                # sale_order_line_obj.name = line.advertisement_description
            else:
                product_line.append((0, 0, {
                    'product_id': line.product_id.id,
                    'name': line.advertisement_description,
                    'product_uom_qty': line.no_of_lines,
                    'price_unit': line.product_id.list_price,
                    'product_uom': line.product_id.uom_id.id,
                    'order_id': self.id,
                }))
                self.classified_order_line = product_line

    def nap_scheduling_details(self):
        if len(self.scheduling_line_ids) > 0:
            nap_scheduling_pool = self.env['nap.scheduling.details']
            for scheduling_details in self.scheduling_line_ids:
                if scheduling_details:
                    data = nap_scheduling_pool.create({
                        'product_id': scheduling_details.product_id.id,
                        'name': scheduling_details.name,
                        'length': scheduling_details.length,
                        'width': scheduling_details.width,
                        'size': scheduling_details.size,
                        'publication_ids': [(6, 0, scheduling_details.publication_ids.ids)],
                        'page': scheduling_details.page,
                        'page_no': scheduling_details.page_no.id,
                        'ad_position': scheduling_details.ad_position.id,
                        'publish_date': scheduling_details.publish_date,
                        'scheduling_status': scheduling_details.scheduling_status,
                        'rejected_reason': scheduling_details.rejected_reason,
                        'scheduling_line_id': scheduling_details.scheduling_line_id.id,
                        'region_ids': [(6, 0, scheduling_details.region_ids.ids)],
                        'publication_id': scheduling_details.publication_id.id,
                        'scheduling_lines': scheduling_details.id,
                        'customer_id': scheduling_details.scheduling_line_id.partner_id.id,
                        'agent_id': scheduling_details.scheduling_line_id.agent_name.id,
                        'ad_template':'template_1',
                        'edition_type':'single',
                        'paper_number':'one'
                    })
                    if bool(self.reta_bool_field) == True:
                        data.generate_sequence('reta')
                    elif bool(self.nap_bool_field) == True:
                        data.generate_sequence('nap')

    def send_for_scheduling(self):
        scheduling_line = []
        if self.reta_bool_field or self.nap_bool_field:
            if len(self.reta_order_line) > 0:
                order_line = self.reta_order_line
            elif len(self.nap_order_line) > 0:
                order_line = self.nap_order_line
            else:
                raise ValidationError("Please Add order lines")

            for line in order_line:
                if self.scheduling_date == 'specific_date':
                    for publication_line in line.publication_line_ids:
                        scheduling_line.append((0, 0, {
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'size': line.size,
                            'length': line.length,
                            'width': line.width,
                            'publication_ids': line.publication_ids.ids,
                            'region_ids': publication_line.publication_region_ids.ids,
                            'publication_id': publication_line.publication_id.id,
                            'page_no': line.page.id,
                            'ad_position': line.ad_position.id,
                            'publish_date': self.specific_date,
                            'ad_template':'template_1',
                            'edition_type':'single',
                            'paper_number':'one'
                        }))
                else:
                    for pub_date in self.multi_publish_date:
                        for publication_line in line.publication_line_ids:
                            scheduling_line.append((0, 0, {
                                'product_id': line.product_id.id,
                                'name': line.name,
                                'size': line.size,
                                'length': line.length,
                                'width': line.width,
                                'publication_ids': line.publication_ids.ids,
                                'region_ids': publication_line.publication_region_ids.ids,
                                'publication_id': publication_line.publication_id.id,
                                'page_no': line.page.id,
                                'ad_position': line.ad_position.id,
                                'publish_date': pub_date.publish_date,
                                'ad_template':'template_1',
                                'edition_type':'single',
                                'paper_number':'one'
                            }))

            self.scheduling_line_ids.unlink()
            self.scheduling_line_ids = scheduling_line
            self.state = 'sent'
            self.nap_scheduling_details()

    def action_view_payments(self):

        return {
            'name': _('View Payments'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'domain': [('sale_order_id', '=', self[0].id)],
            'views_id': False,
            'views': [(self.env.ref('account.view_account_payment_tree').id or False, 'tree'),
                      (self.env.ref('account.view_account_payment_form').id or False, 'form')],
        }


class AdvertisementContentLine(models.Model):
    _name = 'advertisement.content.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    advertisement_language = fields.Selection([
        ('telugu', 'Telugu'),
        ('english', 'English'),
        ('english_telugu', 'English & Telugu')
    ], string="Advertisement Language", default='telugu')
    product_id = fields.Many2one('product.product', string="Ads Type")
    advertisement_description = fields.Text('Description', tracking=True)
    advertisement_description_as_per_lipi = fields.Text('Converted Description')
    no_of_characters = fields.Integer('No of Characters')
    no_of_lines = fields.Integer('No of Lines')
    advertisement_line_id = fields.Many2one('sale.order', string='Sale Order Ref')

    @api.onchange('product_id')
    def product_categ_domain(self):
        domain = []
        user = self.env['res.users'].browse(self._uid)
        restricted_categories = user.product_category_ids.ids
        domain.append(('categ_id', 'in', restricted_categories))

        return {'domain': {'product_id': domain}}

    @api.onchange('advertisement_description')
    def onchange_advertisement_description(self):
        if self.advertisement_description:
            description_len = len(str(self.advertisement_description))
            if self.advertisement_language == 'english':
                description_line = int(description_len) / 18
            else:
                description_line = int(description_len) / 15
            if math.ceil(description_line) > 18:
                raise UserError('Advertisement Description can not be greater than 18 Lines')
            else:
                self.no_of_characters = description_len
                self.no_of_lines = math.ceil(description_line)

            ascii_list = []
            for char in self.advertisement_description:
                ascii_value = ord(char)
                ascii_list.append(ascii_value)
            self.advertisement_description_as_per_lipi = ascii_list


class SchedulingLines(models.Model):
    _name = 'scheduling.lines'

    product_id = fields.Many2one('product.product', string="Product")
    name = fields.Char('Description')
    length = fields.Integer('Length')
    width = fields.Integer('Width')
    size = fields.Char('Size(Sq.cm)')
    publication_ids = fields.Many2many('publication.details', 'publication_details_scheduling_ref',
                                       string="Publications")
    page = fields.Integer('Page No')
    page_no = fields.Many2one('newspaper.page.details', string='Page No')
    ad_position = fields.Many2one('advertisement.position', string="Position")
    publish_date = fields.Date('Publish Date', readonly=True)
    scheduling_status = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", readonly=True)
    rejected_reason = fields.Char('Reject Reason', readonly=True)
    scheduling_line_id = fields.Many2one('sale.order', string="Sale Order ref")

    region_ids = fields.Many2many('reta.regions', string='Publication Regions')
    publication_id = fields.Many2one('publication.details', string="Publications")

    def action_approve_schedule(self):
        self.scheduling_status = 'approved'

        scheduling_line = {
            'product_id': self.product_id.id,
            'name': self.name,
            'size': self.size,
            'length': self.length,
            'width': self.width,
            'page': self.page_no.id,
            'publication_ids': self.publication_ids.ids,
            'ad_position': self.ad_position.id,
            'publish_date': self.publish_date,
            'state': self.scheduling_status,
            'scheduling_line_id': self.id,
            'region_ids': self.region_ids.ids,
            'publication_id': self.publication_id.id,
            'is_reta': self.scheduling_line_id.reta_bool_field,
            'is_classifieds': self.scheduling_line_id.classified_bool_field,
        }
        position_help_create_obj = self.env['scheduling.position.details'].create(scheduling_line)

    def open_position_help(self):
        position_help_obj = self.env['scheduling.position.details'].search([
            ('publish_date', '=', self.publish_date),
            ('page', '=', self.page_no.id),
            ('publication_id', '=', self.publication_id.id)
        ])
        position_help_list = []
        for position in position_help_obj:
            position_help_list.append(position.id)
        if self.scheduling_line_id.reta_bool_field:
            domain = [('id', '=', position_help_list), ('is_reta', '=', True)]
        if self.scheduling_line_id.classified_bool_field:
            domain = [('id', '=', position_help_list), ('is_classifieds', '=', True)]
        return {
            'name': _('Position Help'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'scheduling.position.details',
            'domain': domain,
            'target': 'new',
            'views_id': False,
            'views': [(self.env.ref('eenadu_reta.scheduling_position_details_tree_view').id or False, 'tree'),
                      (self.env.ref('eenadu_reta.scheduling_position_details_form_view').id or False, 'form')],
        }


class SaleRelatedDocuments(models.Model):
    _name = 'sale.related.documents'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Many2one('sale.document.type', string='Name')
    related_document = fields.Binary('Attachment', attachment=True, store=True)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    sale_related_document_id = fields.Many2one('sale.order', string='Sale Order ref')
    file_name = fields.Char(string='Slug Number', compute='_compute_tiff_allocation', store=True)
    cio_ro_number = fields.Char(string='CIO/RO Number', related='sale_related_document_id.custom_seq')
    agent_name = fields.Char(string='Agent Name')
    agent_name_id = fields.Many2one('res.partner', string='Agent Name', related='sale_related_document_id.agent_name')
    publishing_date = fields.Date(string='Published Date', related='sale_related_document_id.specific_date')
    slug_material = fields.Char(string='Slug Number of the Material')
    activity_master = fields.Char(string='Activity Master')
    tiff_allocation = fields.Char(string='Tiff Allocation')
    state = fields.Selection([('material_receipt', 'Material Receipt '), ('dtp', 'DTP '),
                              ('client_confirmation', 'Client Confirmation'), ('till_allotted', 'Till Allotted'),
                              ('cancel', 'Cancel')],
                             default='material_receipt',
                             string="Status", tracking=True)
    is_locked = fields.Boolean(string="Locked", default=False)
    is_lock = fields.Boolean(string="Locked", default=False)


    @api.depends('tiff_allocation')
    def _compute_tiff_allocation(self):
        for record in self:
            record.file_name = record.tiff_allocation

    def button_lock(self):
        self.write({'is_locked': True})

    def button_unlock(self):
        self.write({'is_locked': False})

    def button_locks(self):
        self.write({'is_lock': True})


    def button_unlocks(self):
        self.write({'is_lock': False})

    def btn_cancel(self):
        self.state = 'material_receipt'

    def btn_material_receipt(self):
        self.state = 'material_receipt'

    def btn_dtp(self):
        self.state = 'dtp'

    def btn_client_confirmation(self):
        self.state = 'client_confirmation'

    def btn_till_allotted(self):
        self.state = 'till_allotted'

    # @api.onchange('file_name', 'related_document')
    # def _default_file_name(self):
    #     for rec in self:
    #         if rec.related_document:
    #             rec.file_name = rec.related_document

    @api.onchange('tiff_allocation', 'file_name')
    def _default_tiff_allocation(self):
        for rec in self:
            if rec.file_name:
                rec.tiff_allocation = rec.file_name

    # @api.onchange('tiff_allocation', 'file_name')
    # def _default_tiff(self):
    #     for rec in self:
    #         if rec.tiff_allocation:
    #             rec.file_name = rec.tiff_allocation


class PaymentInformation(models.Model):
    _name = 'payment.informations'

    payment_type = fields.Selection([
        ('full', 'Full Payment'),
        ('partial', 'Partial Payment')
    ], string="Payment Type")
    payment_mode = fields.Selection([
        ('cash', 'Cash'),
        ('upi', 'UPI/QR'),
        ('bank', 'Bank - NEFT'),
        ('pdc', 'Cheque'),
    ], string='Payment Mode')

    payee_name = fields.Char('Payee Name')
    payee_mobile = fields.Char('Payee Mobile')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    payment_amount = fields.Monetary('Payment Amount', currency_field="currency_id")
    payment_datetime = fields.Datetime('Payment Date')
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
    bank_name = fields.Char("Bank Name")
    acc_branch_name = fields.Char("Branch Name")
    ifsc = fields.Char("IFSC")
    cheque_no = fields.Char('Cheque No')
    cheque_date = fields.Date('Cheque Date')
    cheque_expiry_date = fields.Date('Cheque Expiry Date')
    siginig_authority = fields.Char('Signing Authority')
    payment_information_id = fields.Many2one('sale.order', string='Sale order ref')

    rio_no = fields.Char(string="CIO Reference", related="payment_information_id.custom_seq")
    amount_due = fields.Monetary(string='Amount Due', related="payment_information_id.cio_amount_due")
