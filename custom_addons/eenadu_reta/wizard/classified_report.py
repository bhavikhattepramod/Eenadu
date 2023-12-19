from odoo import api, fields, models

class ClassifiedReport(models.TransientModel):
	_name = 'classified.report'

	specific_date = fields.Date('Specific Date')

	def print_classified_report(self):
		classified_obj = self.env['sale.order'].search([('specific_date', '=', self.specific_date)])
		print(classified_obj,'---')
		for line in classified_obj.order_line:
			print(line.name)

		return {'type': 'ir.actions.act_window_close'}