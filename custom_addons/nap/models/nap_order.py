from odoo import fields, models, _, api
from odoo.exceptions import ValidationError, UserError


class NapOrder(models.Model):
    _inherit = 'sale.order'

    nap_bool_field = fields.Boolean('Is Nap')
    nap_seq = fields.Char('CIO', readonly=True, copy=False, default='New')
    nap_order_line = fields.One2many('sale.order.line', 'order_id')
    nap_state = fields.Selection([("draft", "Draft"), ("done", "Done")], string="Status",
                                 readonly=True, copy=False, index=True,
                                 tracking=3,
                                 default='draft')

    code_agent = fields.Char('Agent Code')
    nap_ro_seq = fields.Char('RO', readonly=True, copy=False, default='New')

    @api.onchange('code_agent')
    def get_agent_by_code(self):
        for rec in self:
            if rec.code_agent:
                agent = self.env['res.partner'].search([('agent_code', '=', rec.code_agent)], limit=1)
                if agent:
                    rec.partner_id = agent.id
                else:
                    raise ValidationError("Agent code not found")

    @api.model
    def create(self, vals_list):
        if vals_list.get('nap_bool_field') == True:
            agent = self.env['res.partner'].browse(vals_list.get('agent_name'))
            nap_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', str(agent.name) + ' nap.CIO')])
            if nap_next_sequence_obj:
                if vals_list.get('nap_seq', 'New') == 'New':
                    vals_list['name'] = str(agent.agent_code) + self.env['ir.sequence'].next_by_code(
                        str(agent.name) + ' nap.CIO') or 'New'
                    vals_list['nap_seq'] = vals_list['name']
            else:
                vals_list['name'] = self.env['ir.sequence'].next_by_code('nap.quotation.sequence') or 'New'
                vals_list['nap_seq'] = vals_list['name']

        return super(NapOrder, self).create(vals_list)

    @api.depends('reta_state')
    def _compute_custom_sequence_nap(self):
        for order in self:
            print('seq')
            agent = self.env['res.partner'].browse(order.agent_name.id)
            if order.state == 'sale':
                if order.nap_bool_field:
                    ro_next_sequence_obj = self.env['ir.sequence'].search(
                        [('code', '=', str(order.agent_name.name) + ' nap.RO')])

                    if ro_next_sequence_obj:
                        sequence = str(agent.agent_code) + self.env['ir.sequence'].next_by_code(
                            str(agent.name) + 'nap.RO') or "New"
                        order.nap_ro_seq = sequence
                    else:
                        sequence = self.env['ir.sequence'].next_by_code('nap.sale.sequence')
                        order.nap_ro_seq = sequence
                else:
                    order.nap_ro_seq = 'New Sale'
            else:
                order.nap_ro_seq = 'New Sale'

    def print_button(self):
        if self.nap_bool_field:
            self.state = 'print'
            self.reta_state = 'print'
        return super(NapOrder, self).print_button()

    def send_for_scheduling(self):
        scheduling_line_nap = []
        if self.nap_bool_field:
            for line in self.nap_order_line:
                if self.scheduling_date == 'specific_date':
                    for publication_line in line.publication_line_ids:
                        scheduling_line_nap.append((0, 0, {
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'size': line.size,
                            'length': line.length,
                            'width': line.width,
                            'publication_ids': line.publication_ids.ids,
                            'region_ids': publication_line.publication_region_ids.ids,
                            'publication_id': publication_line.publication_id.id,
                            'page_no': line.page.id,
                            'ad_position': line.ad_position.id,
                            'publish_date': self.specific_date,
                        }))
                else:
                    for pub_date in self.multi_publish_date:
                        # if i == 0:
                        #     for publication_line in line.publication_line_ids:
                        #         scheduling_line.append((0,0, {
                        #                 'product_id': line.product_id.id,
                        #                 'name': line.name,
                        #                 'size': line.size,
                        #                 'length': line.length,
                        #                 'width': line.width,
                        #                 'publication_ids': line.publication_ids.ids,
                        #                 'region_ids': publication_line.publication_region_ids.ids,
                        #                 'publication_id': publication_line.publication_id.id,
                        #                 'page_no': line.page.id,
                        #                 'ad_position': line.ad_position.id,
                        #                 'publish_date': self.publish_start_date,
                        #             }))
                        #     publishing_date = self.publish_start_date
                        # else:
                        #     new_date = publishing_date + timedelta(days=self.time_interval)
                        #     publishing_date = new_date
                        for publication_line in line.publication_line_ids:
                            scheduling_line_nap.append((0, 0, {
                                'product_id': line.product_id.id,
                                'name': line.name,
                                'size': line.size,
                                'length': line.length,
                                'width': line.width,
                                'publication_ids': line.publication_ids.ids,
                                'region_ids': publication_line.publication_region_ids.ids,
                                'publication_id': publication_line.publication_id.id,
                                'page_no': line.page.id,
                                'ad_position': line.ad_position.id,
                                'publish_date': pub_date.publish_date,
                            }))

            self.scheduling_line_ids.unlink()
            self.scheduling_line_ids = scheduling_line_nap
            self.state = 'sent'
        return super(NapOrder, self).send_for_scheduling()

    # discuss
    @api.depends('scheduling_line_ids')
    def _compute_scheduling_cancelled(self):
        for rec in self:
            is_scheduling_cancelled = False
            i = 0
            if len(rec.scheduling_line_ids) != 0:
                for line in rec.scheduling_line_ids:
                    if line.scheduling_status == 'rejected':
                        i += 1
                if i == len(rec.scheduling_line_ids):
                    is_scheduling_cancelled = True
                if rec.reta_bool_field and is_scheduling_cancelled == True:
                    rec.is_scheduling_cancelled = is_scheduling_cancelled
                    rec.state = 'cancel'
                    rec.reta_state = 'cancel'
                #  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                elif rec.nap_bool_field and is_scheduling_cancelled == True:
                    rec.is_scheduling_cancelled = is_scheduling_cancelled
                    rec.state = 'cancel'
                    rec.reta_state = 'cancel'
                else:
                    rec.is_scheduling_cancelled = is_scheduling_cancelled
                    rec.state = rec.state
                    rec.reta_state = rec.reta_state
            else:
                rec.is_scheduling_cancelled = is_scheduling_cancelled
                rec.state = rec.state
                rec.reta_state = rec.reta_state

    def action_confirm(self):
        result = super(NapOrder, self).action_confirm()
        self._compute_custom_sequence_nap()
        # if self.nap_bool_field:
        #     if not self.is_terms_and_conditions and not self.is_consent_form:
        #         raise ValidationError('Please Accept the Consent Form and Terms&conditions')

        return result
