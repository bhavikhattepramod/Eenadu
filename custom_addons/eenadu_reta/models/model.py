from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime
import re


class SaleOrderReta(models.Model):
    _inherit = 'sale.order'


    phone_number = fields.Char(string='Phone Number', required=True, size=10, help='Enter your phone number')

    sale_type = fields.Selection([
        ('main', 'Main'),
        ('mini', 'Mini'),
        # ('pellipandiri', 'Pellipandiri')
    ], default='mini', string='Sale Type')
    agent_commission_amount = fields.Float('Agent Commission', compute='_compute_agent_commission')
    final_amount = fields.Float('Final Amount', compute='_compute_agent_commission')

    agent_commission_capturing_id = fields.Many2one('agent.commission.capturing', string='Agent Commission Capturing')

    @api.onchange('reta_bool_field')
    def get_journal_id(self):
        journal_pool = self.env['account.journal']
        if bool(self.reta_bool_field) == True:
            journal_id = journal_pool.search([('so_type', '=', 'reta')], limit=1).id
            if journal_id:
                self.l10n_in_journal_id = journal_id
        elif bool(self.nap_bool_field) == True:
            journal_id = journal_pool.search([('so_type', '=', 'nap')], limit=1).id
            if journal_id:
                self.l10n_in_journal_id = journal_id
        elif bool(self.classified_bool_field) == True:
            journal_id = journal_pool.search([('so_type', '=', 'classifieds')], limit=1).id
            if journal_id:
                self.l10n_in_journal_id = journal_id

    @api.depends('amount_total')
    def _compute_agent_commission(self):
        for rec in self:
            if rec.amount_total > 0:
                if rec.agent_name.agent_commission > 0:
                    agent_commission_amount = (rec.amount_total * rec.agent_name.agent_commission / 100)
                    fn_amount = (rec.amount_total - rec.agent_commission_amount)
                    rec.write({'agent_commission_amount': agent_commission_amount})
                    rec.write({'final_amount': fn_amount})

                else:
                    rec.write({'agent_commission_amount': 0})
                    rec.write({'final_amount': 0})
            else:
                rec.write({'agent_commission_amount': 0})
                rec.write({'final_amount': 0})

    @api.onchange('phone_number')
    def _onchange_phn_no_get_customer(self):
        for rec in self:
            if rec.phone_number:
                if len(rec.phone_number) == 10:
                    cus1 = self.env['res.partner'].search([('mobile', '=', rec.phone_number)], limit=1)
                    cus2 = self.env['res.partner'].search([('mobile', '=', '+91 ' + rec.phone_number)], limit=1)
                    if cus1:
                        rec.partner_id = cus1.id
                    elif cus2:
                        rec.partner_id = cus2.id
                    else:
                        raise UserError(
                            'There is no customer with mobile number : {} . Please create the customer.'.format(
                                rec.phone_number))
                else:
                    raise UserError('Please enter correct mobile number.')

    reta_order_line = fields.One2many('sale.order.line', 'order_id')
    reta_bool_field = fields.Boolean(default=False)
    custom_seq = fields.Char(string='CIO Reference', readonly=True, copy=False, default='New')
    state = fields.Selection(
        selection_add=[('billing', 'Billing')], )
    reta_state = fields.Selection(
        selection=[
            ('draft', "CIO"),
            ('billing', "Billing"),
            ('sent', "Scheduling"),
            ('waiting_for_approval', "Waiting For Approval"),
            ('sale', "Release Order"),
            ('print', "Published"),
            ('done', "Locked"),
            ('cancel', "Rejected"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
    length = fields.Integer(string='Length')
    width = fields.Integer(string='Width')
    custom_sale_seq = fields.Char(string='RO Sequence', readonly=True, copy=False, default='New Sale')
    agent_name = fields.Many2one('res.partner', string='Newspaper Agent')
    agent_code = fields.Char(string="Agent Code")
    reta_agent_user_id = fields.Many2one('res.users', compute='_compute_agent_user_id')
    agent_commission_amount = fields.Float('Agent Commission')
    final_amount = fields.Float('Final Amount')

    def _get_default_publication_id(self):
        return self.env['publication.details'].search([('is_default_publication', '=', True)], limit=1).id

    publication_id = fields.Many2one('publication.details', string="Publications", default=_get_default_publication_id)
    phone_number = fields.Char(string='Mobile Number', required=True, size=10, help='Enter your phone number')

    @api.depends('agent_name')
    def _compute_agent_user_id(self):
        for rec in self:
            if rec.agent_name:
                user_obj = self.env['res.users'].search([('partner_id', '=', rec.agent_name.id)])
                rec.reta_agent_user_id = user_obj.id
            else:
                rec.reta_agent_user_id = None

    # @api.model
    def default_get(self, values):
        result = super(SaleOrderReta, self).default_get(values)
        result['agent_name'] = self.env.user.partner_id.id
        result['agent_code'] = self.env.user.partner_id.agent_code
        result['user_id'] = self.env.user.id

        return result

    def print_button(self):
        if self.reta_bool_field:
            self.state = 'print'
            self.reta_state = 'print'

    # def onchange_pricelist(self):

    #     for rec in self:
    #         pricelist = self.env['product.pricelist.item'].search(['product_tmpl_id','=',self.reta_order_line.product_id])
    #         if pricelist:
    #             rec.reta_order_line.length = pricelist.length

    # @api.model
    # def create(self,vals):
    #     if vals.get('reta_bool_field'):
    #         if vals.get('custom_seq','New') == 'New':
    #             vals['custom_seq'] = self.env['ir.sequence'].next_by_code('reta.quotation.sequence') or 'New'
    #     result = super(SaleOrderReta,self).create(vals)
    #     return result

    @api.model
    def create(self, vals):
        if vals.get('reta_bool_field'):
            agent = self.env['res.partner'].browse(vals.get('agent_name'))

            cio_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', str(agent.name) + '.CIO')])

            if cio_next_sequence_obj:
                if vals.get('custom_seq', 'New') == 'New':
                    vals['custom_seq'] = str(agent.agent_code) + self.env['ir.sequence'].next_by_code(
                        str(agent.name) + '.CIO') or 'New'
            else:
                vals['custom_seq'] = self.env['ir.sequence'].next_by_code('reta.quotation.sequence') or 'New'

        # if vals.get('date_order'):
        #     date_format = "%Y-%m-%d %H:%M:%S"
        #     if datetime.strptime(vals.get('date_order'), date_format).date() < datetime.now().date():
        #         raise ValidationError('Quotation date should be current or future date')
        # if vals.get('specific_date'):
        #     date_format = "%Y-%m-%d %H:%M:%S"
        #     if datetime.strptime(vals.get('specific_date'), date_format).date() < datetime.now().date():
        #         raise ValidationError('Specific Date should be current or future date')
        # if vals.get('from_date'):
        #     date_format = "%Y-%m-%d %H:%M:%S"
        #     if datetime.strptime(vals.get('from_date'), date_format).date() < datetime.now().date():
        #         raise ValidationError('From date should be current or future date')
        # if vals.get('to_date'):
        #     date_format = "%Y-%m-%d %H:%M:%S"
        #     if datetime.strptime(vals.get('to_date'), date_format).date() < datetime.now().date():
        #         raise ValidationError('To date should be current or future date')
        #     if datetime.strptime(vals.get('from_date'), date_format).date() < datetime.strptime(vals.get('to_date'), date_format).date():
        #         raise ValidationError('To date should be greater than from date')
        # if vals.get('publish_start_date'):
        #     date_format = "%Y-%m-%d %H:%M:%S"
        #     if datetime.strptime(vals.get('from_date'), date_format).date() < datetime.strptime(vals.get('publish_start_date'), date_format).date() and datetime.strptime(vals.get('publish_start_date'), date_format).date() < datetime.strptime(vals.get('to_date'), date_format).date():
        #         raise ValidationError('Publish Start Date should be between From and To Date')

        result = super(SaleOrderReta, self).create(vals)
        return result

    @api.depends('reta_state')
    def _compute_custom_sequence(self):
        for order in self:
            agent = self.env['res.partner'].browse(order.agent_name.id)
            if order.state == 'sale':
                if order.reta_bool_field:
                    ro_next_sequence_obj = self.env['ir.sequence'].search(
                        [('code', '=', str(order.agent_name.name) + '.RO')])

                    if ro_next_sequence_obj:
                        sequence = str(agent.agent_code) + self.env['ir.sequence'].next_by_code(
                            str(agent.name) + '.RO') or "New"
                        order.custom_sale_seq = sequence
                    else:
                        sequence = self.env['ir.sequence'].next_by_code('reta.sale.sequence')
                        order.custom_sale_seq = sequence
                else:
                    order.custom_sale_seq = 'New Sale'
            else:
                order.custom_sale_seq = 'New Sale'

    # @api.depends('reta_state')
    # def _compute_custom_sequence(self):
    #     for order in self:
    #         if order.state == 'sale':
    #             if order.reta_bool_field:
    #                 sequence = self.env['ir.sequence'].next_by_code('reta.sale.sequence')
    #                 order.custom_sale_seq = sequence
    #             else:
    #                 order.custom_sale_seq = 'New Sale'
    #         else:
    #             order.custom_sale_seq = 'New Sale'

    def action_confirm(self):
        result = super(SaleOrderReta, self).action_confirm()
        self._compute_custom_sequence()
        return result

    @api.constrains('state')
    def states_change_reta(self):
        if self.state == 'draft':
            self.reta_state = 'draft'
        elif self.state == 'billing':
            self.reta_state = 'billing'
        elif self.state == 'sent':
            self.reta_state = 'sent'
        elif self.state == 'sale':
            self.reta_state = 'sale'
        elif self.state == 'done':
            self.reta_state = 'done'
        elif self.state == 'cancel':
            self.reta_state = 'cancel'

    # @api.depends(
    #     'reta_order_line.price_subtotal',
    #     'reta_order_line.price_tax',
    #     'reta_order_line.price_total',
    #     'order_line.price_subtotal', 
    #     'order_line.price_tax', 
    #     'order_line.price_total')
    # def _compute_amounts(self):
    #     """Compute the total amounts of the SO."""
    #     for order in self:
    #         order_lines = order.order_line.filtered(lambda x: not x.display_type)
    #         order.amount_untaxed = sum(order_lines.mapped('price_subtotal'))
    #         order.amount_tax = sum(order_lines.mapped('price_tax'))
    #         order.amount_total = order.amount_untaxed + order.amount_tax


class RetaOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    def _get_default_pricelist_id(self):
        return self.env['product.pricelist'].search([('default_pricelist', '=', True)], limit=1).id

    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        change_default=True, ondelete='restrict', check_company=True, index='btree_not_null',
        domain="[('product_tmpl_id','=',product_template_id),('sale_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    pricelist_id = fields.Many2one('product.pricelist.item')
    length = fields.Integer(string='Length', readonly=False)
    width = fields.Integer(string='Width', readonly=False)
    size = fields.Char(string="Size")
    page = fields.Many2one('newspaper.page.details', string='Page No')
    page_id = fields.Many2one('page.master.info', string='Page Reservation ID')
    ad_position = fields.Many2one('advertisement.position', string="Position")
    publication_ids = fields.Many2many('publication.details', 'publication_details_ref', string="Publications")

    district_page_details = fields.Many2one('res.partner', domain=[('is_district', '=', True)], string='District')
    edition_page_details = fields.Many2one('res.partner', domain=[('is_additions', '=', True)], string='Editions')
    zone_page_details = fields.Many2one('res.partner', domain=[('is_zone', '=', True)], string='Zones')
    product_pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', default=_get_default_pricelist_id)

    region_ids = fields.Many2many('reta.regions', string='Publication Regions')
    publication_id = fields.Many2one('publication.details', string="Publications")

    special_discount = fields.Many2one('category.discount', 'Category')
    category_discount = fields.Integer('Category Discount')
    agent_id = fields.Many2one('res.partner', related='order_id.agent_name')
    customer_id = fields.Many2one('res.partner', related='order_id.partner_id')

    @api.onchange('publication_line_ids')
    def _compute_fixed_price_to_price_unit(self):
        fixed_price = 0.00
        for rec in self.publication_line_ids:
            fixed_price += rec.fixed_price_unit
        if self.product_id.price_type == 'fixed':
            if self.order_id.scheduling_date == 'multiple_date' and self.order_id.no_of_occurence > 0:
                mul = fixed_price * self.order_id.no_of_occurence
                # qty_mul = self.product_uom_qty * self.order_id.no_of_occurence
                div = mul / self.product_uom_qty
                # self.product_uom_qty = qty_mul
                self.price_unit = div
            else:
                div = fixed_price / self.product_uom_qty
                self.price_unit = div

    @api.onchange('category_discount')
    def _onchange_validate_category_discount(self):
        cat_dis = self.env['category.discount'].search([('id', '=', self.special_discount.id)])
        if self.category_discount > cat_dis.max_discount:
            raise UserError('You can apply maximum discount of {}%.'.format(cat_dis.max_discount))

    publication_line_ids = fields.One2many('publication.line', 'publication_line_id', string='Publication Lines')

    sale_type = fields.Selection([
        ('main', 'Main'),
        ('mini', 'Mini'),
        # ('pellipandiri', 'Pellipandiri')
    ], string='Sale Type', related='order_id.sale_type')

    multi_discount = fields.Many2many('multi.discount', string='Multi Discount', domain="[('sale_type','=',sale_type)]")

    multi_discount_applied = fields.Float('total Discount')

    multi_discount_bool = fields.Boolean('Is Multi discount')
    size_readonly = fields.Boolean('size readonly', default=False)

    @api.onchange('product_id')
    def check_product_is_sthirasthi(self):
        for rec in self:
            # print(rec.order_id.specific_date.strftime("%A"))
            if rec.product_id.is_sthirasthi == True:
                if rec.order_id.scheduling_date == 'specific_date':
                    if rec.order_id.specific_date.strftime("%A") not in ['Sunday', 'Saturday']:
                        raise ValidationError('Only on sunday and Saturday you can add this product')
                elif rec.order_id.scheduling_date == 'multiple_date':
                    for date in rec.order_id.multi_publish_date:
                        if date.publish_date.strftime("%A") not in ['Sunday', 'Saturday']:
                            raise ValidationError('Please select only Sunday or Saturday dates in multi publish date')

    @api.onchange('product_template_id')
    def product_categ_domain(self):
        domain = []
        user = self.env['res.users'].browse(self._uid)
        restricted_categories = user.product_category_ids.ids
        domain.append(('categ_id', 'in', restricted_categories))

        return {'domain': {'product_template_id': domain}}

    # multi discount 13
    @api.onchange('multi_discount')
    def onchange_region_publication(self):
        total = 0
        price_unit = 0.00
        # storing price for getting max value
        prices = []
        if self.order_id.reta_bool_field == True:
            if self.product_id.price_type == 'variable':
                for rec in self.publication_line_ids:
                    if rec.publication_id and rec.publication_region_ids:
                        # for loop for geeting max values
                        for region in rec.publication_region_ids:
                            pricelist_line_obj = self.env['product.pricelist.item'].search([
                                ('pricelist_id', '=', rec.publication_line_id.product_pricelist_id.id),
                                ('product_id', '=', rec.publication_line_id.product_id.id),
                                ('publication_id', '=', rec.publication_id.id),
                                ('reta_regions_id.name', '=', region.name)
                            ])
                            prices.append(pricelist_line_obj.fixed_price)
                        if prices:
                            max_value = max(prices)
                        if len(rec.publication_line_id.multi_discount) == 1:
                            #     for loop for calculation of discount
                            for region in rec.publication_region_ids:
                                pricelist_line_obj = self.env['product.pricelist.item'].search([
                                    ('pricelist_id', '=', rec.publication_line_id.product_pricelist_id.id),
                                    ('product_id', '=', rec.publication_line_id.product_id.id),
                                    ('publication_id', '=', rec.publication_id.id),
                                    ('reta_regions_id.name', '=', region.name)
                                ])
                                if len(rec.publication_region_ids) > 1:
                                    if rec.publication_line_id.multi_discount.is_multi_zone == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'district':
                                            if max_value != pricelist_line_obj.fixed_price:
                                                discount_amount = pricelist_line_obj.fixed_price * (
                                                        rec.publication_line_id.multi_discount.discount / 100)
                                                discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                price_unit += discounted_price
                                                total += pricelist_line_obj.fixed_price
                                            else:
                                                price_unit += pricelist_line_obj.fixed_price
                                                total += pricelist_line_obj.fixed_price
                                        # else:
                                        #     raise ValidationError(
                                        #         'Please select valid {}'.format(
                                        #             rec.publication_line_id.multi_discount.name))

                                    elif rec.publication_line_id.multi_discount.is_multi_edition == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'edition':
                                            discount_amount = pricelist_line_obj.fixed_price * (
                                                    rec.publication_line_id.multi_discount.discount / 100)
                                            discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                            price_unit += discounted_price
                                            total += pricelist_line_obj.fixed_price
                                        # else:
                                        #     raise ValidationError(
                                        #         'Please select valid {}'.format(
                                        #             rec.publication_line_id.multi_discount.name))
                                    elif rec.publication_line_id.multi_discount.is_multi_region == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                            sort_price = sorted(prices)
                                            if len(sort_price) >= 3:
                                                if sort_price[-1] == pricelist_line_obj.fixed_price:
                                                    price_unit += pricelist_line_obj.fixed_price
                                                    total += pricelist_line_obj.fixed_price
                                                elif sort_price[-2] == pricelist_line_obj.fixed_price:
                                                    discount_amount = pricelist_line_obj.fixed_price * (
                                                            rec.publication_line_id.multi_discount.second_hightest_discount / 100)
                                                    discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                    price_unit += discounted_price
                                                    total += pricelist_line_obj.fixed_price
                                                elif sort_price[-3] == pricelist_line_obj.fixed_price:
                                                    discount_amount = pricelist_line_obj.fixed_price * (
                                                            rec.publication_line_id.multi_discount.third_hightest_discount / 100)
                                                    discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                    price_unit += discounted_price
                                                    total += pricelist_line_obj.fixed_price
                                                else:
                                                    discount_amount = pricelist_line_obj.fixed_price * (
                                                            rec.publication_line_id.multi_discount.discount / 100)
                                                    discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                    price_unit += discounted_price
                                                    total += pricelist_line_obj.fixed_price
                                            elif len(sort_price) == 2:
                                                if sort_price[-1] == pricelist_line_obj.fixed_price:
                                                    price_unit += pricelist_line_obj.fixed_price
                                                    total += pricelist_line_obj.fixed_price
                                                elif sort_price[-2] == pricelist_line_obj.fixed_price:
                                                    discount_amount = pricelist_line_obj.fixed_price * (
                                                            rec.publication_line_id.multi_discount.second_hightest_discount / 100)
                                                    discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                    price_unit += discounted_price
                                                    total += pricelist_line_obj.fixed_price
                                        # else:
                                        #     raise ValidationError(
                                        #         'Please select valid {}'.format(
                                        #             rec.publication_line_id.multi_discount.name))
                                else:
                                    if rec.publication_line_id.multi_discount.is_multi_zone == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'district':
                                            price_unit += pricelist_line_obj.fixed_price
                                            total += pricelist_line_obj.fixed_price
                                        else:
                                            raise ValidationError(
                                                'Please select valid {}'.format(
                                                    rec.publication_line_id.multi_discount.name))
                                    elif rec.publication_line_id.multi_discount.is_multi_edition == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'edition':
                                            price_unit += pricelist_line_obj.fixed_price
                                            total += pricelist_line_obj.fixed_price
                                        # else:
                                        #     raise ValidationError(
                                        #         'Please select valid {}'.format(
                                        #             rec.publication_line_id.multi_discount.name))
                                    elif rec.publication_line_id.multi_discount.is_multi_region == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                            price_unit += pricelist_line_obj.fixed_price
                                            total += pricelist_line_obj.fixed_price
                                        # else:
                                        #     raise ValidationError(
                                        #         'Please select valid {}'.format(
                                        #             rec.publication_line_id.multi_discount.name))
                        elif len(rec.publication_line_id.multi_discount) > 1:
                            if len(rec.publication_region_ids) > 1:
                                regions_list = []
                                for region in rec.publication_region_ids:
                                    pricelist_line_obj = self.env['product.pricelist.item'].search([
                                        ('pricelist_id', '=', rec.publication_line_id.product_pricelist_id.id),
                                        ('product_id', '=', rec.publication_line_id.product_id.id),
                                        ('publication_id', '=', rec.publication_id.id),
                                        ('reta_regions_id.name', '=', region.name)
                                    ])
                                    for check_region in rec.publication_line_id.multi_discount:
                                        if check_region.is_multi_region == True:
                                            if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                                regions_list.append(pricelist_line_obj.fixed_price)

                                for region_rec in rec.publication_region_ids:
                                    pricelist_line_obj = self.env['product.pricelist.item'].search([
                                        ('pricelist_id', '=', rec.publication_line_id.product_pricelist_id.id),
                                        ('product_id', '=', rec.publication_line_id.product_id.id),
                                        ('publication_id', '=', rec.publication_id.id),
                                        ('reta_regions_id.name', '=', region_rec.name)
                                    ])
                                    for more_discount in rec.publication_line_id.multi_discount:
                                        if more_discount.is_multi_region == True:
                                            if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                                # max_region_list = max(regions_list)
                                                sort_price_division = sorted(regions_list)
                                                # if max_region_list == sort_price_division[-1]:
                                                if len(sort_price_division) >= 3:
                                                    if sort_price_division[-1] == pricelist_line_obj.fixed_price:
                                                        price_unit += pricelist_line_obj.fixed_price
                                                        total += pricelist_line_obj.fixed_price
                                                    elif sort_price_division[-2] == pricelist_line_obj.fixed_price:
                                                        discount_amount = pricelist_line_obj.fixed_price * (
                                                                more_discount.second_hightest_discount / 100)
                                                        discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                        price_unit += discounted_price
                                                        total += pricelist_line_obj.fixed_price
                                                    elif sort_price_division[-3] == pricelist_line_obj.fixed_price:
                                                        discount_amount = pricelist_line_obj.fixed_price * (
                                                                more_discount.third_hightest_discount / 100)
                                                        discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                        price_unit += discounted_price
                                                        total += pricelist_line_obj.fixed_price
                                                    else:
                                                        discount_amount = pricelist_line_obj.fixed_price * (
                                                                more_discount.multi_discount.discount / 100)
                                                        discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                        price_unit += discounted_price
                                                        total += pricelist_line_obj.fixed_price
                                                elif len(sort_price_division) == 2:
                                                    if sort_price_division[-1] == pricelist_line_obj.fixed_price:
                                                        price_unit += pricelist_line_obj.fixed_price
                                                        total += pricelist_line_obj.fixed_price
                                                    elif sort_price_division[-2] == pricelist_line_obj.fixed_price:
                                                        discount_amount = pricelist_line_obj.fixed_price * (
                                                                more_discount.second_hightest_discount / 100)
                                                        discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                        price_unit += discounted_price
                                                        total += pricelist_line_obj.fixed_price
                                                else:
                                                    price_unit += pricelist_line_obj.fixed_price

                                        if more_discount.is_multi_edition == True:
                                            if pricelist_line_obj.reta_regions_id.advertising_region_type == 'edition':
                                                discount_amount = pricelist_line_obj.fixed_price * (
                                                        more_discount.discount / 100)
                                                discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                price_unit += discounted_price
                                                total += pricelist_line_obj.fixed_price

                                        if more_discount.is_multi_zone == True:
                                            if pricelist_line_obj.reta_regions_id.advertising_region_type == 'district':
                                                # if max_value != pricelist_line_obj.fixed_price:
                                                discount_amount = pricelist_line_obj.fixed_price * (
                                                        more_discount.discount / 100)
                                                discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                price_unit += discounted_price
                                                total += pricelist_line_obj.fixed_price
                            else:
                                for discount in rec.publication_line_id.multi_discount:
                                    if discount.is_multi_zone == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'district':
                                            price_unit += pricelist_line_obj.fixed_price
                                            total += pricelist_line_obj.fixed_price
                                    if discount.is_multi_edition == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'edition':
                                            price_unit += pricelist_line_obj.fixed_price
                                            total += pricelist_line_obj.fixed_price
                                    if discount.is_multi_region == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                            price_unit += pricelist_line_obj.fixed_price
                                            total += pricelist_line_obj.fixed_price

                        else:
                            for region in rec.publication_region_ids:
                                pricelist_line_obj = rec.env['product.pricelist.item'].search([
                                    ('pricelist_id', '=', rec.publication_line_id.product_pricelist_id.id),
                                    ('product_id', '=', rec.publication_line_id.product_id.id),
                                    ('publication_id', '=', rec.publication_id.id),
                                    ('reta_regions_id.name', '=', region.name)
                                ])
                                for pricelist in pricelist_line_obj:
                                    price_unit += pricelist.fixed_price
                                    total += pricelist.fixed_price

                self.multi_discount_applied = (total - price_unit) * self.product_uom_qty
                self.price_unit = price_unit

                if self.special_discount:
                    if self.category_discount > 0:
                        special = self.price_unit * (self.category_discount / 100)
                        self.price_unit = self.price_unit - special
                        
                        disc = special * self.product_uom_qty
                        all_disc = disc + self.multi_discount_applied
                        self.multi_discount_applied = all_disc

    # @api.depends('product_id', 'product_uom', 'product_uom_qty')
    # def _compute_price_unit(self):
    #     res = super(RetaOrderLineInherit, self)._compute_price_unit()
    #     for product in self.product_id:
    #         if product.price_type and product.price_type == 'fixed':
    #             self.size = product.size
    #             # Splitting the input string at 'X' or 'x' to separate length and width
    #             if 'X' in self.size:
    #                 length, width = self.size.split("X")
    #             elif 'x' in self.size:
    #                 length, width = self.size.split("x")
    #             else:
    #                 raise UserError('Please enter a valid format')
    #             # Converting length and width to integers
    #             length = int(length)
    #             width = int(width)
    #
    #             # Calculating the product qty
    #             uom = length * width
    #             price = product.lst_price / uom
    #             if self.order_id.scheduling_date == 'multiple_date' and self.order_id.no_of_occurence > 0:
    #                 price_no_of_occurence = uom * self.order_id.no_of_occurence
    #                 price = product.lst_price / price_no_of_occurence
    #
    #             self.price_unit = price
    #
    #             self.size_readonly = True
    #         else:
    #             self.size_readonly = False
    #     return res

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        res = super(RetaOrderLineInherit, self)._compute_price_unit()
        for product in self.product_id:
            if product.price_type and product.price_type == 'fixed':
                self.price_unit = 0.00
                self.size = product.size
                self.size_readonly = True
        return res

    @api.onchange('product_id', 'product_template_id')
    def adding_analytic_distribution_reta(self):
        if self.order_id.reta_bool_field == True:
            distribution = self.env['account.analytic.account'].search([('is_advertisement', '=', True)])
            if distribution:
                self.analytic_distribution = {distribution.id: distribution.id}

    # @api.depends('product_id', 'product_uom', 'product_uom_qty')
    # def _compute_price_unit(self):
    #     for line in self:
    #         # check if there is already invoiced amount. if so, the price shouldn't change as it might have been
    #         # manually edited
    #         if line.order_id.reta_bool_field != True:
    #             if line.qty_invoiced > 0:
    #                 continue
    #             if not line.product_uom or not line.product_id or not line.order_id.pricelist_id:
    #                 line.price_unit = 0.0
    #             else:
    #                 price = line.with_company(line.company_id)._get_display_price()
    #                 line.price_unit = line.product_id._get_tax_included_unit_price(
    #                     line.company_id,
    #                     line.order_id.currency_id,
    #                     line.order_id.date_order,
    #                     'sale',
    #                     fiscal_position=line.order_id.fiscal_position_id,
    #                     product_price_unit=price,
    #                     product_currency=line.currency_id
    #                 )
    #         else:
    #             line.price_unit = 0.00

    @api.onchange('product_id', 'product_pricelist_id', 'publication_line_ids', 'multi_discount')
    def _onchange_get_unit_price(self):
        if self.order_id.reta_bool_field:
            if self.product_id.price_type == 'variable':
                total = 0.00
                total_discount = 0.00
                for line in self.publication_line_ids:
                    total += line.price_unit
                    total_discount += line.multi_discount_applied
                self.price_unit = total
                # sep 19
                self.multi_discount_applied = total_discount * self.product_uom_qty
        if self.order_id.classified_bool_field:
            if self.product_id.price_type == 'variable':
                classifieds_total = 0.00
                for publication_line in self.publication_line_ids:
                    classifieds_total += publication_line.price_unit
                self.price_unit = classifieds_total

    # @api.onchange('product_id', 'product_pricelist_id', 'publication_line_ids')
    # def add_price_unit_from_publication_lines(self):
    #     if self.order_id.classified_bool_field:
    #         total = 0.00
    #         for line in self.publication_line_ids:
    #             total += line.price_unit
    #         self.price_unit = total

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            publication_list = []
            for publication in rec.order_id.publication_id.related_publications:
                publication_list.append(publication.id)
            res_domain = {'domain': {
                'publication_id': "[('id', '=', False)]"
            }}
            res_domain['domain']['publication_id'] = "[('id', 'in', %s)]" % publication_list
            return res_domain

    @api.onchange('district_page_details', 'edition_page_details', 'zone_page_details')
    def _onchange_regions(self):
        if self.district_page_details:
            product_pricelist = self.env['product.pricelist'].search(
                [('district_page_details', '=', self.district_page_details.id),
                 ('edition_page_details', '=', self.edition_page_details.id),
                 ('zone_page_details', '=', self.zone_page_details.id)])
            price_list = []

            for price in product_pricelist:
                price_list.append(price.id)

            res_domain = {'domain': {
                'product_pricelist_id': "[('id', '=', False)]"
            }}

            res_domain['domain']['product_pricelist_id'] = "[('id', 'in', %s)]" % price_list

            return res_domain

    @api.onchange('size', 'product_id')
    def onchange_size(self):
        if self.size:
            # Splitting the input string at 'X' or 'x' to separate length and width
            if 'X' in self.size:
                length, width = self.size.split("X")
            elif 'x' in self.size:
                length, width = self.size.split("x")
            else:
                raise UserError('Please enter a valid format')
            # Converting length and width to integers
            length = int(length)
            width = int(width)

            # Calculating the product qty
            if self.order_id.scheduling_date == 'multiple_date' and self.order_id.no_of_occurence > 0:
                size = length * width
                product_uom_qty = size * self.order_id.no_of_occurence
                self.product_uom_qty = product_uom_qty
            else:
                self.product_uom_qty = length * width

    @api.onchange('length', 'width')
    def onchange_length_width(self):
        for qty in self:
            multiply = qty.length * qty.width
            type_multiply = float(multiply)
            qty.product_uom_qty = type_multiply


class publicationLine(models.Model):
    _name = 'publication.line'

    def _get_default_publication_id(self):
        return self.env['publication.details'].search([('is_default_publication', '=', True)], limit=1).id

    parent_publication_id = fields.Many2one('publication.details', 'Parent publication')
    parent_sale_type = fields.Selection([
        ('main', 'Main'),
        ('mini', 'Mini'),
        ('pellipandiri', 'Pellipandiri')
    ], default='mini', string="Parent Sale Type")
    publication_id = fields.Many2one('publication.details', 'Publication', default=_get_default_publication_id)
    publication_region_ids = fields.Many2many('reta.regions', 'region_id_ref', string='Regions')
    price_unit = fields.Float('Price Unit')

    publication_line_id = fields.Many2one('sale.order.line', 'Scheduling Line ref')
    multi_discount_applied = fields.Float('total Discount')
    product_id = fields.Many2one('product.product', 'Ads type', related='publication_line_id.product_id')

    fixed_price_unit = fields.Float('Fixed price unit', compute='_compute_fixed_price', )

    @api.onchange('publication_id', 'publication_region_ids', 'publication_line_id')
    def _compute_fixed_price(self):
        fixed_price = 0.00
        for rec in self:
            if rec.product_id.price_type == 'fixed':
                for item in rec.publication_region_ids:
                    pricelist_line_obj = self.env['product.pricelist.item'].search([
                        ('pricelist_id', '=', self.publication_line_id.product_pricelist_id.id),
                        ('product_id', '=', self.publication_line_id.product_id.id),
                        ('publication_id', '=', self.publication_id.id),
                        ('reta_regions_id.name', '=', item.name)
                    ])
                    fixed_price += pricelist_line_obj.fixed_price
            rec.fixed_price_unit = fixed_price

    @api.onchange('parent_publication_id')
    def onchange_parent_publication_id(self):
        if self.parent_publication_id:
            publication_list_list = []
            if self.parent_publication_id.related_publications:
                for publication in self.parent_publication_id.related_publications:
                    publication_list_list.append(publication.id)
            else:
                publication_list_list.append(self.parent_publication_id.id)

            res_domain = {'domain': {
                'publication_id': "[('id', '=', False)]"
            }}

            res_domain['domain']['publication_id'] = "[('id', 'in', %s)]" % publication_list_list

            return res_domain

    @api.onchange('parent_sale_type')
    def onchange_parent_sale_type(self):
        if self.parent_sale_type:
            regions_list = []
            regions_obj = self.env['reta.regions'].search([('sale_type', '=', self.parent_sale_type)])
            for region in regions_obj:
                regions_list.append(region.id)

            res_domain = {
                'domain': {
                    'publication_region_ids': "[('id', '=', False)]"
                }
            }

            res_domain['domain']['publication_region_ids'] = "[('id', 'in', %s)]" % regions_list

            return res_domain

    @api.onchange('publication_id', 'publication_region_ids', 'publication_line_id')
    def onchange_region_publication(self):
        total = 0.00
        price_unit = 0.00
        # storing price for getting max value
        prices = []
        if self.publication_line_id.order_id.reta_bool_field == True or self.publication_line_id.order_id.nap_bool_field == True:
            if self.publication_line_id.product_id.price_type == 'variable':
                if self.publication_id and self.publication_region_ids:
                    # for loop for geeting max values
                    for region in self.publication_region_ids:
                        pricelist_line_obj = self.env['product.pricelist.item'].search([
                            ('pricelist_id', '=', self.publication_line_id.product_pricelist_id.id),
                            ('product_id', '=', self.publication_line_id.product_id.id),
                            ('publication_id', '=', self.publication_id.id),
                            ('reta_regions_id.name', '=', region.name)
                        ])
                        prices.append(pricelist_line_obj.fixed_price)
                    if prices:
                        max_value = max(prices)
                    if len(self.publication_line_id.multi_discount) == 1:
                        #     for loop for calculation of discount
                        for region in self.publication_region_ids:
                            pricelist_line_obj = self.env['product.pricelist.item'].search([
                                ('pricelist_id', '=', self.publication_line_id.product_pricelist_id.id),
                                ('product_id', '=', self.publication_line_id.product_id.id),
                                ('publication_id', '=', self.publication_id.id),
                                ('reta_regions_id.name', '=', region.name)
                            ])
                            if len(self.publication_region_ids) > 1:
                                if self.publication_line_id.multi_discount.is_multi_zone == True:
                                    if pricelist_line_obj.reta_regions_id.advertising_region_type == 'district':
                                        if max_value != pricelist_line_obj.fixed_price:
                                            discount_amount = pricelist_line_obj.fixed_price * (
                                                    self.publication_line_id.multi_discount.discount / 100)
                                            discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                            price_unit += discounted_price
                                            total += pricelist_line_obj.fixed_price
                                        else:
                                            price_unit += pricelist_line_obj.fixed_price
                                            total += pricelist_line_obj.fixed_price
                                    # else:
                                    #     raise ValidationError(
                                    #         'Please select valid {}'.format(
                                    #             self.publication_line_id.multi_discount.name))
                                elif self.publication_line_id.multi_discount.is_multi_edition == True:
                                    if pricelist_line_obj.reta_regions_id.advertising_region_type == 'edition':
                                        discount_amount = pricelist_line_obj.fixed_price * (
                                                self.publication_line_id.multi_discount.discount / 100)
                                        discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                        price_unit += discounted_price
                                        total += pricelist_line_obj.fixed_price
                                    # else:
                                    #     raise ValidationError(
                                    #         'Please select valid {}'.format(
                                    #             self.publication_line_id.multi_discount.name))
                                elif self.publication_line_id.multi_discount.is_multi_region == True:
                                    if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                        sort_price = sorted(prices)
                                        if len(sort_price) >= 3:
                                            if sort_price[-1] == pricelist_line_obj.fixed_price:
                                                price_unit += pricelist_line_obj.fixed_price
                                                total += pricelist_line_obj.fixed_price
                                            elif sort_price[-2] == pricelist_line_obj.fixed_price:
                                                discount_amount = pricelist_line_obj.fixed_price * (
                                                        self.publication_line_id.multi_discount.second_hightest_discount / 100)
                                                discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                price_unit += discounted_price
                                                total += pricelist_line_obj.fixed_price
                                            elif sort_price[-3] == pricelist_line_obj.fixed_price:
                                                discount_amount = pricelist_line_obj.fixed_price * (
                                                        self.publication_line_id.multi_discount.third_hightest_discount / 100)
                                                discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                price_unit += discounted_price
                                                total += pricelist_line_obj.fixed_price
                                            else:
                                                discount_amount = pricelist_line_obj.fixed_price * (
                                                        self.publication_line_id.multi_discount.discount / 100)
                                                discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                price_unit += discounted_price
                                                total += pricelist_line_obj.fixed_price
                                        elif len(sort_price) == 2:
                                            if sort_price[-1] == pricelist_line_obj.fixed_price:
                                                price_unit += pricelist_line_obj.fixed_price
                                                total += pricelist_line_obj.fixed_price
                                            elif sort_price[-2] == pricelist_line_obj.fixed_price:
                                                discount_amount = pricelist_line_obj.fixed_price * (
                                                        self.publication_line_id.multi_discount.second_hightest_discount / 100)
                                                discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                price_unit += discounted_price
                                                total += pricelist_line_obj.fixed_price
                                    # else:
                                    #     raise ValidationError(
                                    #         'Please select valid {}'.format(
                                    #             self.publication_line_id.multi_discount.name))
                            else:
                                if self.publication_line_id.multi_discount.is_multi_zone == True:
                                    if pricelist_line_obj.reta_regions_id.advertising_region_type == 'district':
                                        price_unit += pricelist_line_obj.fixed_price
                                        total += pricelist_line_obj.fixed_price
                                    # else:
                                    #     raise ValidationError(
                                    #         'Please select valid {}'.format(
                                    #             self.publication_line_id.multi_discount.name))
                                elif self.publication_line_id.multi_discount.is_multi_edition == True:
                                    if pricelist_line_obj.reta_regions_id.advertising_region_type == 'edition':
                                        price_unit += pricelist_line_obj.fixed_price
                                        total += pricelist_line_obj.fixed_price
                                    # else:
                                    #     raise ValidationError(
                                    #         'Please select valid {}'.format(
                                    #             self.publication_line_id.multi_discount.name))
                                elif self.publication_line_id.multi_discount.is_multi_region == True:
                                    if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                        price_unit += pricelist_line_obj.fixed_price
                                        total += pricelist_line_obj.fixed_price
                                    # else:
                                    #     raise ValidationError(
                                    #         'Please select valid {}'.format(
                                    #             self.publication_line_id.multi_discount.name))
                    elif len(self.publication_line_id.multi_discount) > 1:
                        if len(self.publication_region_ids) > 1:
                            regions_list = []
                            for region in self.publication_region_ids:
                                pricelist_line_obj = self.env['product.pricelist.item'].search([
                                    ('pricelist_id', '=', self.publication_line_id.product_pricelist_id.id),
                                    ('product_id', '=', self.publication_line_id.product_id.id),
                                    ('publication_id', '=', self.publication_id.id),
                                    ('reta_regions_id.name', '=', region.name)
                                ])
                                for check_region in self.publication_line_id.multi_discount:
                                    if check_region.is_multi_region == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                            regions_list.append(pricelist_line_obj.fixed_price)

                            for region_rec in self.publication_region_ids:
                                pricelist_line_obj = self.env['product.pricelist.item'].search([
                                    ('pricelist_id', '=', self.publication_line_id.product_pricelist_id.id),
                                    ('product_id', '=', self.publication_line_id.product_id.id),
                                    ('publication_id', '=', self.publication_id.id),
                                    ('reta_regions_id.name', '=', region_rec.name)
                                ])
                                for more_discount in self.publication_line_id.multi_discount:
                                    if more_discount.is_multi_region == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                            # max_region_list = max(regions_list)
                                            sort_price_division = sorted(regions_list)
                                            # if max_region_list == sort_price_division[-1]:
                                            if len(sort_price_division) >= 3:
                                                if sort_price_division[-1] == pricelist_line_obj.fixed_price:
                                                    price_unit += pricelist_line_obj.fixed_price
                                                    total += pricelist_line_obj.fixed_price
                                                elif sort_price_division[-2] == pricelist_line_obj.fixed_price:
                                                    discount_amount = pricelist_line_obj.fixed_price * (
                                                            more_discount.second_hightest_discount / 100)
                                                    discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                    price_unit += discounted_price
                                                    total += pricelist_line_obj.fixed_price
                                                elif sort_price_division[-3] == pricelist_line_obj.fixed_price:
                                                    discount_amount = pricelist_line_obj.fixed_price * (
                                                            more_discount.third_hightest_discount / 100)
                                                    discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                    price_unit += discounted_price
                                                    total += pricelist_line_obj.fixed_price
                                                else:
                                                    discount_amount = pricelist_line_obj.fixed_price * (
                                                            more_discount.multi_discount.discount / 100)
                                                    discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                    price_unit += discounted_price
                                                    total += pricelist_line_obj.fixed_price
                                            elif len(sort_price_division) == 2:
                                                if sort_price_division[-1] == pricelist_line_obj.fixed_price:
                                                    price_unit += pricelist_line_obj.fixed_price
                                                    total += pricelist_line_obj.fixed_price
                                                elif sort_price_division[-2] == pricelist_line_obj.fixed_price:
                                                    discount_amount = pricelist_line_obj.fixed_price * (
                                                            more_discount.second_hightest_discount / 100)
                                                    discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                                    price_unit += discounted_price
                                                    total += pricelist_line_obj.fixed_price
                                            else:
                                                price_unit += pricelist_line_obj.fixed_price

                                    if more_discount.is_multi_edition == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'edition':
                                            discount_amount = pricelist_line_obj.fixed_price * (
                                                    more_discount.discount / 100)
                                            discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                            price_unit += discounted_price
                                            total += pricelist_line_obj.fixed_price

                                    if more_discount.is_multi_zone == True:
                                        if pricelist_line_obj.reta_regions_id.advertising_region_type == 'district':
                                            # if max_value != pricelist_line_obj.fixed_price:
                                            discount_amount = pricelist_line_obj.fixed_price * (
                                                    more_discount.discount / 100)
                                            discounted_price = pricelist_line_obj.fixed_price - discount_amount
                                            price_unit += discounted_price
                                            total += pricelist_line_obj.fixed_price
                        else:
                            for discount in self.publication_line_id.multi_discount:
                                if discount.is_multi_zone == True:
                                    if pricelist_line_obj.reta_regions_id.advertising_region_type == 'district':
                                        price_unit += pricelist_line_obj.fixed_price
                                        total += pricelist_line_obj.fixed_price
                                if discount.is_multi_edition == True:
                                    if pricelist_line_obj.reta_regions_id.advertising_region_type == 'edition':
                                        price_unit += pricelist_line_obj.fixed_price
                                        total += pricelist_line_obj.fixed_price
                                if discount.is_multi_region == True:
                                    if pricelist_line_obj.reta_regions_id.advertising_region_type == 'region':
                                        price_unit += pricelist_line_obj.fixed_price
                                        total += pricelist_line_obj.fixed_price
                            # print(max_region_list, 'jjjjj')

                        # for pricelist in pricelist_line_obj:
                        #     price_unit += pricelist.fixed_price
                        #     total += pricelist.fixed_price

                    else:
                        for region in self.publication_region_ids:
                            pricelist_line_obj = self.env['product.pricelist.item'].search([
                                ('pricelist_id', '=', self.publication_line_id.product_pricelist_id.id),
                                ('product_id', '=', self.publication_line_id.product_id.id),
                                ('publication_id', '=', self.publication_id.id),
                                ('reta_regions_id.name', '=', region.name)
                            ])
                            for pricelist in pricelist_line_obj:
                                price_unit += pricelist.fixed_price
                                total += pricelist.fixed_price

            self.price_unit = price_unit
            self.multi_discount_applied = total - price_unit

            if self.publication_line_id.special_discount:
                if self.publication_line_id.category_discount > 0:
                    special = self.price_unit * (self.publication_line_id.category_discount / 100)
                    self.price_unit = self.price_unit - special
                    
                    disc = special + self.multi_discount_applied
                    self.multi_discount_applied = disc

    # @api.onchange('publication_id','publication_region_ids')
    # def onchange_region_publication(self):
    #     price_unit = 0.00
    #     if self.publication_id and self.publication_region_ids:
    #         for region in self.publication_region_ids:
    #             pricelist_line_obj = self.env['product.pricelist.item'].search([
    #                 ('pricelist_id', '=', self.publication_line_id.product_pricelist_id.id),
    #                 ('product_id', '=', self.publication_line_id.product_id.id),
    #                 ('publication_id', '=', self.publication_id.id),
    #                 ('reta_regions_id.name', '=', region.name)
    #             ])
    #             price_unit += pricelist_line_obj.fixed_price
    #     self.price_unit = price_unit

    # @api.onchange('publication_id', 'publication_region_ids')
    # def _onchange_publication_id_get_regions(self):
    #     # to get regions based on the product in sale order line and in the reta.region
    #     for rec in self:
    #         region_list = []
    #         for product in rec.product_id:
    #             regions = self.env['reta.regions'].search([('product_id', '=', product.id)])
    #             for region in regions:
    #                 if region.id not in region_list:
    #                     if region.sale_type == rec.publication_line_id.sale_type:
    #                         region_list.append(region.id)
    #         res_domain = {'domain': {
    #             'publication_region_ids': "[('id', '=', False)]"
    #         }}
    #         res_domain['domain']['publication_region_ids'] = "[('id', 'in', %s)]" % region_list
    #         return res_domain


class ProductPriceListInherit(models.Model):
    _inherit = 'product.pricelist.item'

    length = fields.Integer(string='Length')
    width = fields.Integer(string='Width')
    reta_regions_id = fields.Many2one('reta.regions', string='Regions')
    publication_id = fields.Many2one('publication.details', string="Publications")


class AccountMoveInheritSale(models.Model):
    _inherit = 'account.move'

    agent_name = fields.Many2one('res.partner', string='Agent Name', readonly=True, compute='compute_agent_name',
                                 store=True)
    agent_user_id = fields.Many2one('res.users', string="Agent User Id", compute='compute_agent_user_id')
    reta_bool_field = fields.Boolean(string='Reta Orders')

    def compute_agent_name(self):
        for res in self:
            agent = self.env['sale.order'].search([('name', '=', res.invoice_origin)])
            if agent:
                res.agent_name = agent.agent_name.id
                res.reta_bool_field = agent.reta_bool_field
            if not res.agent_name and res.reta_bool_field:
                continue

    @api.depends('agent_name')
    def compute_agent_user_id(self):
        for rec in self:
            if rec.agent_name:
                agent_user_id = self.env['res.users'].search([('partner_id', '=', rec.agent_name.id)], limit=1)
                if agent_user_id:
                    rec.agent_user_id = agent_user_id.id
                else:
                    rec.agent_user_id = None
            else:
                rec.agent_user_id = None


class ResPartner(models.Model):
    _inherit = 'res.partner'



    @api.constrains('mobile', 'phone')
    def _check_phone_mobile_length(self):
        for record in self:
            if record.mobile:
                if not str(record.mobile).isdigit() or len(str(record.mobile)) != 10:
                    raise ValidationError(_("Mobile number must be numeric and have exactly 10 digits."))

            if record.phone:
                if not str(record.phone).isdigit() or len(str(record.phone)) != 10:
                    raise ValidationError(_("Phone number must be numeric and have exactly 10 digits."))

    @api.constrains('email')
    def _check_email_format(self):
        for record in self:
            if record.email and not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                raise ValidationError("Invalid email format.     Please enter a valid email address.")
