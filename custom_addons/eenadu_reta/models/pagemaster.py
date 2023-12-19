from odoo import models, api, fields, _


class PageMaster(models.Model):
    _name = 'page.master'


    page_number = fields.Char('Page Number')
    page_name = fields.Char('Page Name')
    page_height = fields.Float('Page Height')
    page_width = fields.Float('Page Width')
    total = fields.Float('Total', compute='_compute_total')


    @api.depends('page_height', 'page_width')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.page_height * rec.page_width


class PageInfo(models.Model):
    _name = 'page.info'

    page_name = fields.Many2one('page.master', string='name')
    page_number = fields.Char('Page Number', related='page_name.page_number')
    page_height = fields.Float('Page Height', related='page_name.page_height')
    page_width = fields.Float('Page Width', related='page_name.page_width')
    total = fields.Float('Total', related='page_name.total')
    reserved = fields.Float('Reserved')
    remaining = fields.Float('Remaining', compute='_compute_remaining')


    @api.depends('total', 'reserved')
    def _compute_remaining(self):
        for rec in self:
            rec.remaining = rec.total - rec.reserved
