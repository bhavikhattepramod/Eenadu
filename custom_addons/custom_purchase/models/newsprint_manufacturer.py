from odoo import fields, models, api, _

class NewsprintManufacturer(models.Model):
	_name = "newsprint.manufacturer"

	name = fields.Char('Name')
	country_id = fields.Many2one('res.country', string = "Country")