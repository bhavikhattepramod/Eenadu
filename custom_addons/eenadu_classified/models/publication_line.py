from odoo import api, fields, models


class PublicationLineInherit(models.Model):
    _inherit = 'publication.line'

    @api.onchange('publication_id', 'publication_region_ids')
    def unit_price_classified_Rate_publication_lines(self):
        for rec in self:
            if rec.publication_line_id.order_id.classified_bool_field == True:
                lines_amt = 0.00
                extra_amt = 0.00
                lines = 0
                for regions in rec.publication_region_ids:
                    classified_rates = self.env['classified.rates'].search([
                        ('product_id', '=', rec.publication_line_id.product_id.id),
                        ('pricelist_id', '=', rec.publication_line_id.product_pricelist_id.id),
                        ('packages', '=', rec.publication_line_id.packages.id),
                        ('publication_id', '=', rec.publication_id.id),
                        ('regions_id.name', '=', regions.name)
                    ])
                    # if regions.name == classified_rates.reta_regions_id.name:
                    lines_amt += classified_rates.minimum_lines_price
                    extra_amt += classified_rates.additional_line_price
                    lines += classified_rates.minimum_lines
                if rec.publication_line_id.product_uom_qty <= lines:
                    qty = lines_amt / rec.publication_line_id.product_uom_qty
                    rec.price_unit = round(qty)
                else:
                    sub = rec.publication_line_id.product_uom_qty - lines
                    multi = (sub * extra_amt) + lines_amt
                    div = multi / rec.publication_line_id.product_uom_qty
                    # div = round(multi / order_line.product_uom_qty, 3)
                    rec.price_unit = round(div)
