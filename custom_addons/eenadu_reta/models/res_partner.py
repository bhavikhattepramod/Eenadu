from odoo import api, models, fields


class ResPartner(models.Model):
	_inherit = 'res.partner'

	hr_employee_id = fields.Many2one('hr.employee', string="Reporting Manager")
	cust_seq = fields.Char(string='Agent Sequence', readonly=True, copy=False, default='New')
	unit = fields.Many2one('unit.master', string="Unit")

	max_credit_limit = fields.Monetary('Maximum credit limit')
	agent_type_id = fields.Many2one('agent.type', 'Agent Type')
	ins_code = fields.Char('INS Code')
	ins_region = fields.Many2one('ins.region', 'INS Region')
	agency_start_date = fields.Date('Agency Start Date')
	deposit_amount = fields.Monetary('Deposit Amount')
	receipt_number = fields.Char('Receipt Number')
	is_nap_agent = fields.Boolean('Is nap agent')

	# alternative_mobile_number = fields.Char(string="Alternative Number")

	# @api.onchange('alternative_mobile_number', 'country_id', 'company_id')
	# def _onchange_mobile_validation(self):
	# 	if self.alternative_mobile_number:
	# 		self.mobile = self.phone_get_sanitized_number(number_fname='mobile',
	# 													  force_format='INTERNATIONAL') or self.mobile

	@api.model
	def create(self, vals_list):
		if vals_list.get('is_newsprint_agent'):
			reta_cio_seq_obj = self.env['ir.sequence'].search(
				[('code', '=', str(vals_list.get('agent_code')) + '.CIO')])
			reta_ro_seq_obj = self.env['ir.sequence'].search([('code', '=', str(vals_list.get('agent_code')) + '.RO')])

			classifieds_cio_seq_obj = self.env['ir.sequence'].search(
				[('code', '=', str(vals_list.get('agent_code')) + ' Classifieds.CIO')])
			classifieds_ro_seq_obj = self.env['ir.sequence'].search(
				[('code', '=', str(vals_list.get('agent_code')) + ' Classifieds.RO')])

			if not reta_cio_seq_obj:
				self.env['ir.sequence'].sudo().create({
					'name': str(vals_list.get('agent_code')),
					'code': str(vals_list.get('agent_code')) + '.CIO',
					'prefix': '/RETA/CIO/',
					'padding': 5
				})
			if not reta_ro_seq_obj:
				self.env['ir.sequence'].sudo().create({
					'name': str(vals_list.get('agent_code')),
					'code': str(vals_list.get('agent_code')) + '.RO',
					'prefix': '/RETA/RO/',
					'padding': 5
				})
			if not classifieds_cio_seq_obj:
				self.env['ir.sequence'].sudo().create({
					'name': str(vals_list.get('agent_code')) + ' Classifieds',
					'code': str(vals_list.get('agent_code')) + ' Classifieds.CIO',
					'prefix': '/Classified/CIO/',
					'padding': 5
				})
			if not classifieds_ro_seq_obj:
				self.env['ir.sequence'].sudo().create({
					'name': str(vals_list.get('agent_code')) + ' Classifieds',
					'code': str(vals_list.get('agent_code')) + ' Classifieds.RO',
					'prefix': '/Classified/RO/',
					'padding': 5
				})

		if self.env.user.partner_id.is_newsprint_agent:
			agent_customer_sequence_obj = self.env['ir.sequence'].search(
				[('code', '=', self.env.user.partner_id.agent_code + '.agent_code')])
			if not agent_customer_sequence_obj:
				self.env['ir.sequence'].sudo().create({
					'name': str(self.env.user.partner_id.agent_code),
					'code': str(self.env.user.partner_id.agent_code) + '.agent_code',
					'prefix': '/CUST/',
					'padding': 5
				})
		if vals_list.get('cust_seq', 'New') == 'New':
			agent_customer_sequence_obj = self.env['ir.sequence'].search(
				[('code', '=', str(vals_list.get('agent_code')) + '.agent_code')])
			if agent_customer_sequence_obj:
				vals_list['cust_seq'] = str(self.env.user.partner_id.agent_code) + self.env['ir.sequence'].next_by_code(
					str(vals_list.get('agent_code')) + '.agent_code') or 'New'
			else:
				vals_list['cust_seq'] = self.env['ir.sequence'].next_by_code('customer.sequence.code') or '/'
		return super(ResPartner, self).create(vals_list)












