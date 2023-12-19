from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class AgentCommission(models.Model):
    _name = 'agent.commission.capturing'
    _description = "AgentCommission"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'agent_name'

    agent_name = fields.Many2one('res.partner', string="Agent Name")
    unit = fields.Integer(string="Unit")
    order_date = fields.Date(string="Order Date")
    total_amount = fields.Float(string="Total Amount")
    comm_amount = fields.Float(string="Comm Amount")
    paid_amount = fields.Float(string="Paid Amount")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
        ('cancel', 'Cancel')
    ], string='Status', default='draft', track_visibility='onchange', copy=False)
    sale_order_ids = fields.One2many('sale.order', 'agent_commission_capturing_id', string="Agent Reserved")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    @api.onchange('start_date',end_date)
    def values_updation_sale_order(self):
        order_ref = self.env['sale.order'].search([('agent_commission_capturing_id','=',self.id)])
        if order_ref:
            order_ref.write({'agent_commission_capturing_id':False})

        order_data = self.env['sale.order'].search([('date_order', '>=', self.start_date),('date_order', '<=', self.end_date),('agent_name', '=', self.agent_name.id),])
        for data in order_data:
            data.agent_commission_capturing_id = self.id

    def action_pending(self):
        self.state = 'pending'

    def action_approved(self):
        self.state = 'approved'

    def action_paid(self):
        self.state = 'paid'

    def action_rejected(self):
        self.state = 'rejected'

    def action_cancel(self):
        self.state = 'cancel'
