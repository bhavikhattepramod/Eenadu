from odoo import fields, models, api, _
import logging
from datetime import datetime


_logger = logging.getLogger(__name__)


class PageMasterFields(models.Model):
    _name = 'page.master.fields'
    _rec_name = 'page_name'

    page_no = fields.Char('Page Number')
    page_name = fields.Char('Page Name')
    length = fields.Float('Length')
    width = fields.Float('Width')
    total_size = fields.Float('Total Size(Sq.cm)', compute='_compute_page_size')
    date = fields.Date(sting='Date')

    # dates = self.env['page.master.fields'].search([])
    # filter_dates = self.env['page.master.fields'].search([]).filtered(lambda l: l.date)

    def test_date(self):
        for rec in self:
            partners = self.env['res.partner'].search([])
            print(" Filtered partners...", partners.filtered('date'))

    @api.depends('length', 'width')
    def _compute_page_size(self):
        for rec in self:
            rec.total_size = rec.length * rec.width


class PageMasterInfo(models.Model):
    _name = 'page.master.info'
    _rec_name = 'page_name_id'

    # page_name = fields.Many2one('page.master.fields', string='Page Name', readonly="1")
    page_name_id = fields.Many2one('newspaper.page.details', string='Page Name', readonly="1")
    page_no = fields.Char('Page Number', readonly="1")
    length = fields.Float('Length', readonly="1")
    width = fields.Float('Width', readonly="1")
    date = fields.Date(string='Date', readonly="1")
    total_size = fields.Float('Total Size(Sq.cm)', readonly="1")
    reserved = fields.Float(string='Reserved', compute="compute_reserved")
    remaining = fields.Float(string='Remaining', compute='_compute_remaining_size')
    page_reserve_ids = fields.One2many('sale.order.line','page_id',string="Default Page Creation")


    @api.depends('total_size', 'reserved')
    def _compute_remaining_size(self):
        for rec in self:
            rec.remaining = rec.total_size - rec.reserved

    def values_updation(self):
        page_data = self.env['page.master.info'].search([('date', '>=', datetime.now().date())])
        for rec in page_data:
            order_data = self.env['sale.order.line'].search([('page', '=', rec.page_name_id.id), ('order_id.specific_date', '>=', rec.date),('order_id.reta_state','!=','cancel')])
            for data in order_data:
                data.page_id = rec.id

    @api.depends('page_reserve_ids.product_uom_qty')
    def compute_reserved(self):
        for rec in self:
            reserved_value = sum(rec.page_reserve_ids.mapped('product_uom_qty'))
            rec.reserved = reserved_value
