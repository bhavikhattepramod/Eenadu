from odoo import api, fields, api, models
from odoo.exceptions import UserError


class UpdateApprove(models.Model):
    _name = 'update.approve'

    proof_reading_line_id = fields.Many2one('proof.reading.line', string = 'Proof Reading')
    original_description = fields.Char('Original Description', readonly=True)
    new_description = fields.Char('Update Description')

    def default_get(self, fields_list):
        res = super(UpdateApprove, self).default_get(fields_list)
        # active_id = self.env.context.get('params').get('id')
        # classified_order = self.env['sale.order'].browse(active_id)
        proof_reading_line_obj = self.env['proof.reading.line'].browse(self.env.context.get('active_id'))
        res['original_description'] = proof_reading_line_obj.name
        res['new_description'] = proof_reading_line_obj.name
        res['proof_reading_line_id'] = self.env.context.get('active_id')

        return res

    def update_approve_description(self):
        if not self.proof_reading_line_id.status == 'reject':
            active_id = self.env.context.get('params').get('id')
            classified_order = self.env['sale.order'].browse(active_id)

            self.proof_reading_line_id.name = self.new_description
            self.proof_reading_line_id.status = 'approve'

            # Advertisement Line Ids
            for ad_line in classified_order.advertisement_line_ids:
                # if ad_line.advertisement_description == self.original_description:
                ad_line.advertisement_description = self.new_description
                ad_line.onchange_advertisement_description()
                classified_order.add_order_line()
            # classified_order.advertisement_line_ids.advertisement_description = self.new_description
            # classified_order.advertisement_line_ids.onchange_advertisement_description()
            # classified_order.add_order_line()
            new_proof_reading_line = {
                'product_id': self.proof_reading_line_id.product_id.id,
                'name': self.proof_reading_line_id.name,
                'publish_date':self.proof_reading_line_id.publish_date,
                'no_of_lines':self.proof_reading_line_id.no_of_lines,
                'status':self.proof_reading_line_id.status,
                'proof_reading_line_id':self.proof_reading_line_id.id,
                'region_ids':self.proof_reading_line_id.region_ids.ids,
                'publication_id':self.proof_reading_line_id.publication_id.id
            }
            proof_reading_create_obj = self.env['proof.reading.details'].create(new_proof_reading_line)
        else:
            raise UserError('You cannot update for the rejected proof reading line')
