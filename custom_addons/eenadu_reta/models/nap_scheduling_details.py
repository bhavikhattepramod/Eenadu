from odoo import fields, models, api, _


class NAPSchedulingDetails(models.Model):
    _name = 'nap.scheduling.details'
    _rec_name = 'ad_sequence'
    description = 'NewsPaper Advertisement Program'

    ad_sequence = fields.Char('Sequence', default='New')
    product_id = fields.Many2one('product.product', string="Ad Name")
    name = fields.Char('Description')
    length = fields.Integer('Length')
    width = fields.Integer('Width')
    size = fields.Char('Size(Sq.cm)')
    publication_ids = fields.Many2many('publication.details', 'nap_publication_details_scheduling_ref',
                                       string="Publications")
    page = fields.Integer('Page No')
    page_no = fields.Many2one('newspaper.page.details', string='Page No')
    ad_position = fields.Many2one('advertisement.position', string="Position")
    publish_date = fields.Date('Publish Date', readonly=True)
    scheduling_status = fields.Selection([
        ('draft', 'draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Status", readonly=True, default='draft')
    ad_template = fields.Selection([
        ('template_1', 'Template 1'),
        ('template_2', 'Template 2'),
        ('template_3', 'Template 3')
    ],string="Ad Template", default='template_1')
    
    rejected_reason = fields.Char('Reject Reason', readonly=True)
    scheduling_line_id = fields.Many2one('sale.order', string="Sale Order ref")
    region_ids = fields.Many2many('reta.regions', string='Publication Regions')
    publication_id = fields.Many2one('publication.details', string="Publications")
    scheduling_lines = fields.Many2one('scheduling.lines')
    customer_id = fields.Many2one('res.partner', string='Customer')
    agent_id = fields.Many2one('res.partner', string='Agent')
    # slug_material = fields.

    source = fields.Selection([('reta', 'RETA'), ('nap', 'NAP'),], readonly=True)
    max_credit_limit = fields.Float('Maximum credit limit')
    agent_type_id = fields.Many2one('agent.type', 'Agent Type')
    ins_code = fields.Char('INS Code')
    ins_region = fields.Many2one('ins.region', 'INS Region')
    agency_start_date = fields.Date('Agency Start Date')
    deposit_amount = fields.Float('Deposit Amount')

    edition_type = fields.Selection([
		('single', 'Single'),
		('twin', 'Twin')
		],string="Edition Type", default="single")
    
    paper_number = fields.Selection([
		('one', '1'),
		('two', '2')
		],string="Paper Number", default="one")
    
    dummy_chart_position = fields.Char('Dummy Chart Position')
    dummy_chart_position_x = fields.Char('Dummy Chart Position X')
    dummy_chart_position_y = fields.Char('Dummy Chart Position Y')

    def update_nap_agent_details(self):
        self.max_credit_limit = self.agent_id.max_credit_limit
        self.agent_type_id = self.agent_id.agent_type_id.id
        self.ins_code = self.agent_id.ins_code
        self.ins_region = self.agent_id.ins_region.id
        self.agency_start_date = self.agent_id.agency_start_date
        self.deposit_amount = self.agent_id.deposit_amount

    def generate_sequence(self, source):
        if self.agent_id.is_nap_agent:
            self.update_nap_agent_details()
        else:
            pass

        self.source = source
        model = self.env['nap.sequence.tracker']
        last_record = model.sudo().search([('partner_id', '=', self.scheduling_line_id.agent_name.id),('source', '=', source)],
                                                              order='sequence_number desc', limit=1)
        if last_record:
            next_sequence_number = last_record.sequence_number + 1
        else:
            data = model.sudo().create({
                'partner_id': self.scheduling_line_id.agent_name.id,
                'sequence_number': 1,
                'source': source,
            })
            next_sequence_number = 1
            data.sequence_number = next_sequence_number
        formatted_sequence_number = str(next_sequence_number).zfill(3)
        sequence_string = f'{self.source.upper()}/{self.scheduling_line_id.agent_code}/{formatted_sequence_number}'
        last_record.sequence_number = next_sequence_number
        self.ad_sequence = sequence_string

    def action_approve_schedule(self):
        self.scheduling_status = 'approved'
        if self.scheduling_lines:
            self.scheduling_lines.write({
                'scheduling_status': self.scheduling_status,
                'page_no': self.page_no.id,
                'page': self.page
            })

        scheduling_line = {
            'product_id': self.product_id.id,
            'name': self.name,
            'size': self.size,
            'length': self.length,
            'width': self.width,
            'page': self.page_no.id,
            'publication_ids': self.publication_ids.ids,
            'ad_position': self.ad_position.id,
            'publish_date': self.publish_date,
            'state': self.scheduling_status,
            'scheduling_line_id': self.scheduling_lines.id,
            'region_ids': self.region_ids.ids,
            'publication_id': self.publication_id.id,
            'is_reta': self.scheduling_line_id.reta_bool_field,
            'is_classifieds': self.scheduling_line_id.classified_bool_field,
        }
        position_help_create_obj = self.env['scheduling.position.details'].create(scheduling_line)

    def open_position_help(self):
        position_help_obj = self.env['scheduling.position.details'].search([
                ('publish_date', '=', self.publish_date),
                ('page','=',self.page_no.id),
                ('publication_id','=',self.publication_id.id)
            ])
        position_help_list = []
        for position in position_help_obj:
            position_help_list.append(position.id)
        if self.scheduling_line_id.reta_bool_field:
            domain = [('id', '=', position_help_list),('is_reta', '=', True)]
        if self.scheduling_line_id.classified_bool_field:
            domain = [('id', '=', position_help_list),('is_classifieds', '=', True)]
        return {
            'name': _('Position Help'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'scheduling.position.details',
            'domain': domain,
            'target':'new',
            'views_id': False,
            'views': [(self.env.ref('eenadu_reta.scheduling_position_details_tree_view').id or False, 'tree'),
                      (self.env.ref('eenadu_reta.scheduling_position_details_form_view').id or False, 'form')],
        }