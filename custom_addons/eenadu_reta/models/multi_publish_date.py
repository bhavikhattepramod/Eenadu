from odoo import api, fields, models
from odoo.exceptions import UserError


class MultiPublishDate(models.Model):
    _name = 'multi.publish.date'

    publish_date = fields.Date('Publish Date')
    sale_order = fields.Many2one('sale.order')

    @api.onchange('publish_date')
    def check_date(self):
        if self.publish_date:
            if self.publish_date < self.sale_order.from_date or self.publish_date > self.sale_order.to_date:
                raise UserError(
                    'Please select the date between {} to {}. '.format(self.sale_order.from_date,
                                                                       self.sale_order.to_date))
