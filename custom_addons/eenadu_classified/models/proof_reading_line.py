from odoo import fields, api, models
from odoo.exceptions import UserError


class ProofReadingLine(models.Model):
    _name = 'proof.reading.line'

    product_id = fields.Many2one('product.product', string="Product", tracking=True)
    name = fields.Char('Description', tracking=True)
    publication_id = fields.Many2one('publication.details', string="Publications", tracking=True)
    no_of_lines = fields.Float('No of lines')
    region_ids = fields.Many2many('reta.regions', string='Publication Regions', tracking=True)
    publish_date = fields.Date('Publish Date', tracking=True)
    status = fields.Selection([('approve', 'Approved'),
                               ('reject', 'Rejected')], 'Status')
    sale_order = fields.Many2one('sale.order')
    reject_reason = fields.Char('Reject Reason')

    def status_approve(self):
        for rec in self:
            if rec.status != 'reject':
                rec.status = 'approve'
                proof_reading_line = {
                    'product_id': self.product_id.id,
                    'name': self.name,
                    'publish_date':self.publish_date,
                    'no_of_lines':self.no_of_lines,
                    'status':self.status,
                    'proof_reading_line_id':self.id,
                    'region_ids':self.region_ids.ids,
                    'publication_id':self.publication_id.id
                }
                proof_reading_create_obj = self.env['proof.reading.details'].create(proof_reading_line)
            else:
                raise UserError('You cannot approve rejected proof reading line')

    def wizard_update_approve(self):
        # Assuming 'some.action' is the XML ID of the action you want to call
        action = self.env.ref('eenadu_classified.action_update_approve').read()[0]
        return action

    def wizard_reject_reason(self):
        # Assuming 'some.action' is the XML ID of the action you want to call
        action = self.env.ref('eenadu_classified.action_reject_reason').read()[0]
        return action
