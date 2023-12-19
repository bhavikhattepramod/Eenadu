from odoo import fields, models, api, _

class SchedulingPositionDetails(models.Model):
	_name = 'scheduling.position.details'
	_rec_name = 'ad_sequence'

	ad_sequence = fields.Char('Sequence', default='New')

	scheduling_line_id = fields.Many2one('scheduling.lines', string='Scheduling Line Ref')
	product_id = fields.Many2one('product.product', string="Product")
	name = fields.Char('Description')
	length = fields.Integer('Length')
	width = fields.Integer('Width')
	size = fields.Char('Size(Sq.cm)')
	publication_ids = fields.Many2many('publication.details','publication_details_position_help_ref', string="Publications")
	page = fields.Many2one('newspaper.page.details', string='Page No')
	ad_position = fields.Many2one('advertisement.position', string="Position")
	publish_date = fields.Date('Publish Date', readonly=True)

	region_ids = fields.Many2many('reta.regions', string='Publication Regions')
	publication_id = fields.Many2one('publication.details', string="Publications")

	is_reta = fields.Boolean('Is Reta?')
	is_classifieds = fields.Boolean('Is Classifieds?')

	state = fields.Selection([
		('approved', 'Approved'),
		('rejected', 'Rejected')
		], string="Status", readonly=True)

	edition_type = fields.Selection([
		('single', 'Single'),
		('twin', 'Twin')
		],string="Edition Type", default='single')

	paper_number = fields.Selection([
		('one', '1'),
		('two', '2')
		],string="Paper Number", default='one')

	dummy_chart_position = fields.Char('Dummy Chart Position')
	dummy_chart_position_x = fields.Char('Dummy Chart Position X')
	dummy_chart_position_y = fields.Char('Dummy Chart Position Y')
	ad_template = fields.Selection([
		('template_1', 'Template 1'),
		('template_2', 'Template 2'),
		('template_3', 'Template 3')
	],string="Ad Template", default='template_1')

	@api.model
	def create(self,vals):
		if vals.get('ad_sequence', 'New') == 'New':
			vals['ad_sequence'] = self.env['ir.sequence'].next_by_code('ads.position.id') or '/'

		res = super(SchedulingPositionDetails, self).create(vals)

		return res