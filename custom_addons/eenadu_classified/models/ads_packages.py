from odoo import api, fields, models


class AdsPackages(models.Model):
    _name = 'ads.packages'

    name = fields.Char('Name')


class ClassifiedRates(models.Model):
    _name = 'classified.rates'

    product_id = fields.Many2one('product.product', string='Product',
                                 domain=[('categ_id.category_for', '=', 'classified')])
    packages = fields.Many2one('ads.packages', string='Packages')
    regions_id = fields.Many2one('reta.regions', string='Regions')
    publication_id = fields.Many2one('publication.details', string="Publications")
    minimum_lines = fields.Float('Minimum Lines')
    minimum_lines_price = fields.Float('Minimum Lines Price')
    additional_line_price = fields.Float('Additional Line Price')
    pricelist_id = fields.Many2one('product.pricelist')



class ProductForCategory(models.Model):
    _inherit = 'product.category'

    category_for = fields.Selection([
        ('reta', 'Reta'),
        ('classified', 'Classified'),
    ], string="Category For")



class ProductPricelistinheritItem(models.Model):
    _inherit = "product.pricelist.item"

    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string="Product",
        ondelete='cascade', check_company=True,
        domain=[('categ_id.category_for', '=', 'reta')],
        help="Specify a template if this rule only applies to one product template. Keep empty otherwise.")


class ProductPricelistinherit(models.Model):
    _inherit = 'product.pricelist'

    classified_rate_o2m = fields.One2many('classified.rates', 'pricelist_id')
