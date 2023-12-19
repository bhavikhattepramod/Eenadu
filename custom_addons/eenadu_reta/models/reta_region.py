from odoo import api, fields, models


class RetaRegions(models.Model):
    _name = 'reta.regions'
    _rec_name = 'name'

    name = fields.Char('Name')
    base_price = fields.Float('Base Price')
    sale_type = fields.Selection([
        ('main', 'Main'),
        ('mini', 'Mini'),
        # ('pellipandiri', 'Pellipandiri'),
        ], string="Sales Type", default='main')
    advertising_region_type = fields.Selection([
        ('region', 'Region'),
        ('edition', 'Editions'),
        ('district', 'District'),
        ('clusters', 'Clusters'),
        ('combined', 'Combination'),
        ], string="Advertising Region Type")
    product_id = fields.Many2many('product.product',string = 'Ads type')
