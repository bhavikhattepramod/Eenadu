from odoo import api, models, fields, _

class ProductPriceList(models.Model):
    _inherit = 'product.pricelist'

    district_page_details = fields.Many2one('res.partner', domain=[('is_district', '=', True)], string='District')
    edition_page_details = fields.Many2one('res.partner', domain=[('is_additions', '=', True)], string='Editions')
    zone_page_details = fields.Many2one('res.partner', domain=[('is_zone', '=', True)], string='Zones')
    default_pricelist = fields.Boolean('Default Pricelist')

    @api.constrains('default_pricelist')
    def check_default_pricelist(self):
        price_list = self.env['product.pricelist'].search_count([('default_pricelist', '=', True)])
        if price_list > 1:
            raise ValidationError('Default Pricelist Already Exist.')