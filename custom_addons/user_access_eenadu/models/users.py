from odoo import models,fields,api


class ProductCategoryNew(models.Model):
    _inherit = "res.users"

    product_category_ids = fields.Many2many('product.category', 'product_categ_users_rel', 'user_id', 'categ_id', string="Product Category")

    is_product_category = fields.Boolean("Restrict Product Category")


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):

        res_user = self.env['res.users'].search([])
        for rec in res_user:
            if rec.is_product_category == True:
                if self._uid and self._uid != 1:
                    user = self.env['res.users'].browse(self._uid)
                    restricted_categories = user.product_category_ids.ids

                    if restricted_categories:
                        args.append(('categ_id', 'in', restricted_categories))

        return super(ProductTemplate, self).search(args, offset, limit, order, count)


class ProductProduct(models.Model):
    _inherit = 'product.product'


    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        res_user = self.env['res.users'].search([])
        for rec in res_user:
            if rec.is_product_category == True:
                if self._uid and self._uid != 1:
                    user = self.env['res.users'].browse(self._uid)
                    restricted_categories = user.product_category_ids.ids

                    if restricted_categories:
                        args.append(('categ_id', 'in', restricted_categories))

        return super(ProductProduct, self).search(args, offset, limit, order, count)