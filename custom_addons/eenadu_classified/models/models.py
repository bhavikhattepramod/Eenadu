from odoo import api, models, fields, _
from datetime import datetime
from ftplib import FTP, error_perm
from io import BytesIO
import time, base64
from odoo.exceptions import ValidationError

class SaleOrderClassified(models.Model):
    _inherit = 'sale.order'

    classified_bool_field = fields.Boolean(default=False)
    is_sthirasthi = fields.Boolean(default=False)

    classified_order_line = fields.One2many('sale.order.line', 'order_id')

    classified_state = fields.Selection(
    selection=[
        ('draft', "Classified"),
        ('billing','Billing'),
        ('sent', "Proof Reading"),
        ('waiting_for_approval', "Waiting For Approval"),
        ('sale', "Release Order"),
        ('print', "Published"),
        ('done', "Locked"),
        ('cancel', "Rejected"),
    ], string="Status",
    readonly=True, copy=False, index=True,
    tracking=3,
    default='draft')

    length_classified = fields.Integer(string='Length')
    width_classified = fields.Integer(string='Width')

    custom_classified_cio_seq = fields.Char(string='CIO Reference',readonly=True,copy=False,default='New')
    custom_classified_seq = fields.Char(string='RO Sequence',readonly=True,copy=False,default='New Sale')

    product_id = fields.Many2one('product.product', string='Product')
    packages = fields.Many2one('ads.packages', string='Packages')

    lipi_converted_file = fields.Binary('Lipi File')

    proof_reading_line = fields.One2many('proof.reading.line','sale_order')

    is_proof_reading_done = fields.Boolean('Is Proof Reading Done?', default=False, compute="compute_proof_reading_done")
    is_proof_reading_cancelled = fields.Boolean('Is Proof Reading Cancelled?', default=False, compute='_compute_proof_reading_cancelled')

    def send_for_billing(self):
        self.classified_state = 'billing'
        self.write({'state':'billing'})

    def confirm_action(self):

        # if self.reta_bool_field or self.classified_bool_field:
        # if not self.is_terms_and_conditions:
        #     raise ValidationError('Please Accept the Consent Form and Terms&conditions')

        result = super(SaleOrderClassified, self).action_confirm()
        self._compute_classified_custom_sequence()
        return result

    @api.depends('proof_reading_line')
    def compute_proof_reading_done(self):
        for rec in self:
            if self.proof_reading_line:
                i = 0
                for line in rec.proof_reading_line:
                    if line.status:
                        i += 1
                    else:
                        i = i
                if len(rec.proof_reading_line) == i:
                    rec.is_proof_reading_done = True
                else:
                    rec.is_proof_reading_done = False
            else:
                rec.is_proof_reading_done = False

    def send_for_proof_reading(self):
        proof_reading_line = []
        if self.classified_bool_field:
            for line in self.classified_order_line:
                if self.scheduling_date == 'specific_date':
                    for publication_line in line.publication_line_ids:
                        proof_reading_line.append((0,0, {
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'no_of_lines':line.product_uom_qty,
                            'region_ids': publication_line.publication_region_ids.ids,
                            'publication_id': publication_line.publication_id.id,
                            'publish_date': self.specific_date,
                        }))
                else:
                    for pub_date in self.multi_publish_date:
                        for publication_line in line.publication_line_ids:
                            proof_reading_line.append((0,0, {
                                    'product_id': line.product_id.id,
                                    'name': line.name,
                                    'no_of_lines':line.product_uom_qty,
                                    'region_ids': publication_line.publication_region_ids.ids,
                                    'publication_id': publication_line.publication_id.id,
                                    'publish_date': pub_date.publish_date,
                                }))

        self.proof_reading_line.unlink()
        self.proof_reading_line = proof_reading_line
        self.state = 'sent'

    @api.depends('proof_reading_line')
    def _compute_proof_reading_cancelled(self):
        for rec in self:
            is_proof_reading_cancelled = False
            i = 0
            if len(rec.proof_reading_line) != 0: 
                for line in rec.proof_reading_line:
                    if line.status == 'reject':
                        i += 1
                if i == len(rec.proof_reading_line):
                    is_proof_reading_cancelled = True
                if rec.classified_bool_field and is_proof_reading_cancelled == True:
                    rec.is_proof_reading_cancelled = is_proof_reading_cancelled
                    rec.state = 'cancel'
                    rec.classified_state = 'cancel'
                else:
                    rec.is_proof_reading_cancelled = is_proof_reading_cancelled
                    rec.state = rec.state
                    rec.classified_state = rec.classified_state
            else:
                rec.is_proof_reading_cancelled = is_proof_reading_cancelled
                rec.state = rec.state
                rec.classified_state = rec.classified_state

    def print_button(self):
        res = super().print_button()
        if self.classified_bool_field:
            self.state = 'print'
            self.classified_state = 'print'
        return res

    def print_word_file(self):
        # ftp_host = '172.18.2.126'
        ftp_host = '13.232.56.99'
        ftp_user = 'sunbright'
        ftp_password = "Iloveindia@91"

        input_folder = '/unisource'
        output_folder = '/dest'

        try:
            ftp = FTP(ftp_host)
            ftp.login(ftp_user, ftp_password)

            ftp.cwd(input_folder)
            ftp.dir()

            for res in self.advertisement_line_ids:
                remote_file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{self.custom_classified_cio_seq}-{self.env.user.name}.txt"
                remote_file_content = base64.b64encode(res.advertisement_description.encode('utf-8'))
                remote_file = BytesIO(remote_file_content)
                sent = ftp.storbinary(f'STOR {remote_file_name}', remote_file)
                ftp.cwd(output_folder)
                ftp.dir()
                convert_file = BytesIO()
                time.sleep(5)
                ftp.retrbinary(f'RETR {remote_file_name}', convert_file.write)
                res.advertisement_line_id.lipi_converted_file = convert_file.getvalue()
                if res.advertisement_line_id.lipi_converted_file:
                    client_action = {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'success',
                            'message': 'File received successfully',
                            'sticky': False, }
                    }
                    return client_action

        except error_perm as e:
            raise ValidationError(f"FTP Error: {e}")

        except Exception as e:
            raise ValidationError(f"An error occurred: {e}")

    # @api.onchange('pricelist_id', 'product_id', 'packages')
    # def unit_price_classified_Rate(self):
    #     for rec in self:
    #         if rec.classified_bool_field == True:
    #             price_list = self.env['product.pricelist'].search([('id', '=', rec.pricelist_id.id)])
    #             for pricelist in price_list.classified_rate_o2m:
    #                 for order_line in rec.reta_order_line:
    #                     if rec.product_id == pricelist.product_id and rec.packages == pricelist.packages:
    #                         if order_line.product_uom_qty <= pricelist.minimum_lines:
    #                             qty = pricelist.minimum_lines_price / order_line.product_uom_qty
    #                             order_line.price_unit = qty
    #                         else:
    #                             sub = order_line.product_uom_qty - pricelist.minimum_lines
    #                             multi = (sub * pricelist.additional_line_price) + pricelist.minimum_lines_price
    #                             div = multi / order_line.product_uom_qty
    #                             # div = round(multi / order_line.product_uom_qty, 3)
    #                             order_line.price_unit = div
    #                     else:
    #                         order_line.price_unit = order_line.product_id.list_price

    # @api.model
    # def create(self,vals):
    #     if vals.get('classified_bool_field'):
    #         if vals.get('custom_classified_cio_seq','New') == 'New':
    #             vals['custom_classified_cio_seq'] = self.env['ir.sequence'].next_by_code('classified.quotation.sequence') or 'New'
    #     result = super(SaleOrderClassified,self).create(vals)
    #     return result

    @api.model
    def create(self, vals):
        if vals.get('classified_bool_field'):
            print(vals)
            agent = self.env['res.partner'].browse(vals.get('agent_name'))

            cio_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', str(agent.name)+' Classifieds.CIO')])
        
            if cio_next_sequence_obj:
                if vals.get('custom_classified_cio_seq', 'New') == 'New':
                    vals['custom_classified_cio_seq'] = str(agent.agent_code) + self.env['ir.sequence'].next_by_code(
                        str(agent.name)+' Classifieds.CIO') or 'New'
            else:
                vals['custom_classified_cio_seq'] = self.env['ir.sequence'].next_by_code('classified.quotation.sequence') or 'New'
        result = super(SaleOrderClassified, self).create(vals)
        return result

    # @api.depends('classified_state')
    # def _compute_classified_custom_sequence(self):
    #     for order in self:
    #         if order.classified_bool_field:
    #             if order.state == 'sale':
    #                 sequence = self.env['ir.sequence'].next_by_code('classified.sale.sequence')
    #                 order.custom_classified_seq = sequence
    #             else:
    #                 order.custom_classified_seq = 'New Sale'
    #         else:
    #             order.custom_classified_seq = 'New Sale'

    @api.depends('classified_state')
    def _compute_classified_custom_sequence(self):
        for order in self:
            agent = self.env['res.partner'].browse(order.agent_name.id)
            if order.state == 'sale':
                if order.classified_bool_field:
                    ro_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', str(order.agent_name.name) + ' Classifieds.RO')])

                    if ro_next_sequence_obj:
                        sequence = str(agent.agent_code) + self.env['ir.sequence'].next_by_code(
                            str(agent.name)+' Classifieds.RO') or "New"
                        order.custom_classified_seq = sequence
                    else:
                        sequence = self.env['ir.sequence'].next_by_code('classified.sale.sequence')
                        order.custom_classified_seq = sequence
                else:
                    order.custom_classified_seq = 'New Sale'
            else:
                order.custom_classified_seq = 'New Sale'


    def action_confirm(self):
        result = super(SaleOrderClassified, self).action_confirm()
        self._compute_classified_custom_sequence()
        return result

    @api.constrains('state')
    def states_change_classified(self):
        if self.state == 'draft':
            self.classified_state = 'draft'
        elif self.state == 'sent':
            self.classified_state = 'sent'
        elif self.state == 'sale':
            self.classified_state = 'sale'
        elif self.state == 'done':
            self.classified_state = 'done'
        elif self.state == 'cancel':
            self.classified_state = 'cancel'

class ClassifiedOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    pricelist_id = fields.Many2one('product.pricelist.item')
    length_classified = fields.Integer(string='Length')
    width_classified = fields.Integer(string='Width')
    packages = fields.Many2one('ads.packages', string='Packages')

    main_category = fields.Many2one('sale.category', 'Main Category', domain="[('parent_category','=',None)]")
    sub_category = fields.Many2one('sale.category', 'Sub Category')

    classified_sale_type = fields.Selection([
        ('main', 'Main'),
        ('mini', 'Mini'),
        # ('pellipandiri', 'Pellipandiri')
        ], default='mini', string='Sale Type')

    main_area = fields.Many2one('area.area', 'Main Area', domain="[('parent_name','=',None)]")
    sub_area = fields.Many2one('area.area', 'Sub Area', domain="[('parent_name','=',main_area)]")

    # @api.onchange('product_id', 'price_unit')
    # def on_change_product(self):
    #     self.order_id.unit_price_classified_Rate()

    # @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    # def _compute_amount(self):
    #     """
    #     Compute the amounts of the SO line.
    #     """
    #     for line in self:
    #         tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
    #         totals = list(tax_results['totals'].values())[0]
    #         if line.order_id.classified_bool_field == True:
    #             amount_untaxed = round(totals['amount_untaxed'])
    #         else:
    #             amount_untaxed = totals['amount_untaxed']
    #         amount_tax = totals['amount_tax']
    #         line.update({
    #             'price_subtotal': amount_untaxed,
    #             'price_tax': amount_tax,
    #             'price_total': amount_untaxed + amount_tax,
    #         })

    @api.onchange('main_category')
    def _onchange_main_category_get_sub_category(self):
        # to get regions based on the product in sale order line and in the reta.region
        for rec in self:
            sub_category_list = []
            products = self.env['sale.category'].search([('parent_category', '=', rec.main_category.id)])
            for product in products:
                sub_category_list.append(product.id)
            res_domain = {'domain': {
                'sub_category': "[('id', '=', False)]"
            }}
            res_domain['domain']['sub_category'] = "[('id', 'in', %s)]" % sub_category_list
            return res_domain


class ClassifiedAccounting(models.Model):
    _inherit = 'account.move'

    classified_bool_field_account = fields.Boolean(string='Classifieds Boolean',store=True)

    def compute_agent_name(self):
        result = super(ClassifiedAccounting, self).compute_agent_name()
        for rec in self:
            classifieds = self.env['sale.order'].search([('name', '=', rec.invoice_origin)])
            if classifieds:
                rec.classified_bool_field_account = classifieds.classified_bool_field
            if not rec.agent_name and rec.classified_bool_field_account:
                continue
        return result


class ProductsClassified(models.Model):
        _inherit = 'product.product'


        is_sthirasthi = fields.Boolean(default=False)

class PayInformation(models.Model):
    _inherit = 'payment.informations'

    cio_no = fields.Char(string="CIO Reference", related="payment_information_id.custom_classified_cio_seq")