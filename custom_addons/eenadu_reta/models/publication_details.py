from odoo import fields, models, api, _
from odoo.exceptions import UserError

class PublicationDetails(models.Model):
	_name = 'publication.details'

	name = fields.Char('Publication Name')
	related_publications = fields.Many2many(
	    'publication.details',
	    'publication_publication_rel',
	    'publication_id',
	    'related_publication_id',
	    string='Related Publications'
	)
	is_default_publication = fields.Boolean('Is Default Publication?')

	@api.constrains('is_default_publication')
	def default_publication_if_exist(self):
		publication_id = (self.env['publication.details'].search_count([('is_default_publication', '=', True)]))
		if publication_id > 1:
			raise UserError('Default Publication already exist.')
