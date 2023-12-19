from odoo import api, fields, models


class NapOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_pricelist_id', 'publication_line_ids', 'multi_discount')
    def _onchange_get_unit_price(self):
        print('lllllllllllllllll')
        if self.order_id.nap_bool_field:
            if self.product_id.price_type == 'variable':
                total = 0.00
                total_discount = 0.00
                for line in self.publication_line_ids:
                    total += line.price_unit
                    total_discount += line.multi_discount_applied
                self.price_unit = total
                # sep 19
                self.multi_discount_applied = total_discount * self.product_uom_qty
        return super(NapOrderLine, self)._onchange_get_unit_price()
