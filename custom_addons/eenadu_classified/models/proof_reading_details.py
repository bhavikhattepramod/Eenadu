from odoo import fields, models, api, _

class ProofReadingDetails(models.Model):
	_name = "proof.reading.details"

	proof_reading_sequence = fields.Char('Sequence', default='New')

	proof_reading_line_id = fields.Many2one('proof.reading.line', string='Prood Reading Line Ref')
	product_id = fields.Many2one('product.product', string="Product", tracking=True)
	name = fields.Char('Description', tracking=True)
	publication_id = fields.Many2one('publication.details', string="Publications", tracking=True)
	no_of_lines = fields.Float('No of lines')
	region_ids = fields.Many2many('reta.regions', string='Publication Regions', tracking=True)
	publish_date = fields.Date('Publish Date', tracking=True)
	status = fields.Selection([
    	('new', 'New'),
    	('approve', 'Approved'),
    	('reject', 'Rejected')], 'Status')
	reject_reason = fields.Char('Reject Reason')

	@api.model
	def create(self,vals):
		if vals.get('proof_reading_sequence', 'New') == 'New':
			vals['proof_reading_sequence'] = self.env['ir.sequence'].next_by_code('proof.reading.seq') or '/'

		res = super(ProofReadingDetails, self).create(vals)

		return res

