# Copyright 2020 Tecnativa - Manuel Calero
# Copyright 2022 Quartile
# Copyright 2014-2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models, _


class CommissionSettlement(models.Model):
    _name = "commission.settlement"
    _description = "Settlement"

    # for classified commission commission_for classified_line total_commission_classified
    commission_for = fields.Selection([('reta', 'Reta'), ('classified', 'Classified')])
    classified_line = fields.One2many('classified.orders.commission',
                                      'commission_settlement_classified')
    total_commission_classified = fields.Float('total', compute='_compute_total_commission_classified')
    total_commission = fields.Float('total', compute='_compute_total_commission')
    reta_order = fields.One2many('reta.orders', 'commission_settlement')
    name = fields.Char()
    total = fields.Float(compute="_compute_total", readonly=True, store=True)
    date_from = fields.Date(string="From", required=True)
    date_to = fields.Date(string="To", required=True)
    agent_id = fields.Many2one(
        comodel_name="res.partner",

        required=True,
    )
    agent_type = fields.Selection(related="agent_id.agent_type")
    settlement_type = fields.Selection(
        selection=[("manual", "Manual")],
        default="manual",
        required=True,
        help="The source of the settlement, e.g. 'Sales invoice', 'Sales order', "
             "'Purchase order'...",
    )
    can_edit = fields.Boolean(
        compute="_compute_can_edit",
        help="Technical field for determining if user can edit settlements",
        store=True,
    )
    line_ids = fields.One2many(
        comodel_name="commission.settlement.line",
        inverse_name="settlement_id",
        string="Settlement lines",
    )
    state = fields.Selection(
        selection=[
            ("settled", "Settled"),
            ("cancel", "Canceled"),
        ],
        readonly=True,
        required=True,
        default="settled",
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        readonly=True,
        default=lambda self: self._default_currency_id(),
        required=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self._default_company_id(),
        required=True,
    )

    commission_type = fields.Selection([('fixed_amount', 'Fixed Amount'), ('percent', 'Commission Percentage')])
    commission_per = fields.Float('Commission Percentage')
    fixed_amt = fields.Float('Fixed Amount')

    def _compute_total_commission(self):
        total = 0
        for rec in self.reta_order:
            total += rec.commission
        self.total_commission = total

    # for classified commission
    def _compute_total_commission_classified(self):
        total = 0
        for classified in self.classified_line:
            total += classified.commission
        self.total_commission_classified = total

    # for adding the lines in order line page based on from and to date
    @api.constrains('date_to', 'date_from', 'agent_id')
    def reta_order_line(self):
        if self.commission_for == 'reta':
            reta_order_line = self.env['sale.order'].search(
                [('reta_bool_field', '=', True), ('agent_name', '=', self.agent_id.id),
                 ('date_order', '<=', self.date_to), ('date_order', '>=', self.date_from),
                 ('reta_state', 'in', ['sale', 'print'])])
            self.reta_order.unlink()
            for order in reta_order_line:
                # for order_lines in self.reta_order:
                #     if order.id == order_lines.cio.id:
                #         return
                # else:
                add = self.env['reta.orders'].create({
                    'cio': order.id,
                    'reta_order': order.custom_sale_seq,
                    'total_amt': order.amount_total,
                    'amount_paid': order.cio_paid_amount,
                    'date': order.date_order.date(),
                })
                self.reta_order += add

    # for classified commission
    @api.constrains('date_to', 'date_from', 'agent_id')
    def classified_order_line(self):
        if self.commission_for == 'classified':
            classified_order_line = self.env['sale.order'].search(
                [('classified_bool_field', '=', True), ('agent_name', '=', self.agent_id.id),
                 ('date_order', '<=', self.date_to), ('date_order', '>=', self.date_from),
                 ('classified_state', 'in', ['sale', 'print'])])
            print(classified_order_line, 'cll')
            self.classified_line.unlink()
            for order in classified_order_line:
                # for order_lines in self.reta_order:
                #     if order.id == order_lines.cio.id:
                #         return
                # else:
                add = self.env['classified.orders.commission'].create({
                    'classifed': order.id,
                    'reta_order': order.custom_classified_cio_seq,
                    'total_amt': order.amount_total,
                    'amount_paid': order.cio_paid_amount,
                    'date': order.date_order.date(),
                })
                self.classified_line += add

    def _default_currency_id(self):
        return self.env.company.currency_id.id

    def _default_company_id(self):
        return self.env.company.id

    @api.depends("line_ids", "line_ids.settled_amount")
    def _compute_total(self):
        for record in self:
            record.total = sum(record.mapped("line_ids.settled_amount"))

    @api.depends("settlement_type")
    def _compute_can_edit(self):
        for record in self:
            record.can_edit = record.settlement_type == "manual"

    def action_cancel(self):
        self.write({"state": "cancel"})

    def reta_dashboard_commissions(self):
        user = self.env.uid
        user_id = self.env['res.users'].browse(user)
        reta_incharge = [agent.id for agent in self.env['res.partner'].search([
            ('hr_employee_id.user_id', '=', user_id.id)])]
        reta_incharge_head = []
        for incharge_head in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for incharge in self.env['hr.employee'].search([('parent_id', '=', incharge_head.id)]):
                reta_incharge_head.append(incharge.user_partner_id.id)
                for agent in self.env['res.partner'].search([
                    ('hr_employee_id', '=', incharge.id)]):
                    reta_incharge_head.append(agent.id)
        unit_manager = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                unit_manager.append(loop_2.user_partner_id.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    unit_manager.append(loop_3.user_partner_id.id)
                    for agent in self.env['res.partner'].search([
                        ('hr_employee_id', '=', loop_3.id)]):
                        unit_manager.append(agent.id)
        reg_in_head = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                reg_in_head.append(loop_2.user_partner_id.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    reg_in_head.append(loop_3.user_partner_id.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        reg_in_head.append(loop_4.user_partner_id.id)
                        for agent in self.env['res.partner'].search([
                            ('hr_employee_id', '=', loop_4.id)]):
                            reg_in_head.append(agent.id)
        reta_head = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                reta_head.append(loop_2.user_partner_id.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    reta_head.append(loop_3.user_partner_id.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        reta_head.append(loop_4.user_partner_id.id)
                        for loop_5 in self.env['hr.employee'].search([
                            ('parent_id', '=', loop_4.id)]):
                            reta_head.append(loop_5.user_partner_id.id)
                            for agent in self.env['res.partner'].search([
                                ('hr_employee_id', '=', loop_5.id)]):
                                reta_head.append(agent.id)
        reta_super_admin = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                reta_super_admin.append(loop_2.user_partner_id.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    reta_super_admin.append(loop_3.user_partner_id.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        reta_super_admin.append(loop_4.user_partner_id.id)
                        for loop_5 in self.env['hr.employee'].search([
                            ('parent_id', '=', loop_4.id)]):
                            reta_super_admin.append(loop_5.user_partner_id.id)
                            for loop_6 in self.env['hr.employee'].search([
                                ('parent_id', '=', loop_5.id)]):
                                reta_super_admin.append(loop_6.user_partner_id.id)
                                for agent in self.env['res.partner'].search([
                                    ('hr_employee_id', '=', loop_6.id)]):
                                    reta_super_admin.append(agent.id)

        if reta_super_admin:
            reta_super_admin.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', reta_super_admin)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        if reta_head:
            reta_head.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', reta_head)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', reg_in_head)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', unit_manager)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        if reta_incharge_head:
            reta_incharge_head.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', reta_incharge_head)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }

        if reta_incharge:
            reta_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', reta_incharge)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        else:
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', '=', user_id.partner_id.id)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }

    def classifier_dashboard_commissions(self):
        user = self.env.uid
        user_id = self.env['res.users'].browse(user)
        classifier_incharge = [agent.id for agent in self.env['res.partner'].search([
            ('hr_employee_id.user_id', '=', user_id.id)])]

        classifier_incharge_head = []
        for incharge_head in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for incharge in self.env['hr.employee'].search([('parent_id', '=', incharge_head.id)]):
                classifier_incharge_head.append(incharge.user_partner_id.id)
                for agent in self.env['res.partner'].search([
                    ('hr_employee_id', '=', incharge.id)]):
                    classifier_incharge_head.append(agent.id)

        unit_manager = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                unit_manager.append(loop_2.user_partner_id.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    unit_manager.append(loop_3.user_partner_id.id)
                    for agent in self.env['res.partner'].search([
                        ('hr_employee_id', '=', loop_3.id)]):
                        unit_manager.append(agent.id)

        reg_in_head = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                reg_in_head.append(loop_2.user_partner_id.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    reg_in_head.append(loop_3.user_partner_id.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        reg_in_head.append(loop_4.user_partner_id.id)
                        for agent in self.env['res.partner'].search([
                            ('hr_employee_id', '=', loop_4.id)]):
                            reg_in_head.append(agent.id)

        classifier_head = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                classifier_head.append(loop_2.user_partner_id.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    classifier_head.append(loop_3.user_partner_id.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        classifier_head.append(loop_4.user_partner_id.id)
                        for loop_5 in self.env['hr.employee'].search([
                            ('parent_id', '=', loop_4.id)]):
                            classifier_head.append(loop_5.user_partner_id.id)
                            for agent in self.env['res.partner'].search([
                                ('hr_employee_id', '=', loop_5.id)]):
                                classifier_head.append(agent.id)

        classifier_super_admin = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                classifier_super_admin.append(loop_2.user_partner_id.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    classifier_super_admin.append(loop_3.user_partner_id.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        classifier_super_admin.append(loop_4.user_partner_id.id)
                        for loop_5 in self.env['hr.employee'].search([
                            ('parent_id', '=', loop_4.id)]):
                            classifier_super_admin.append(loop_5.user_partner_id.id)
                            for loop_6 in self.env['hr.employee'].search([
                                ('parent_id', '=', loop_5.id)]):
                                classifier_super_admin.append(loop_6.user_partner_id.id)
                                for agent in self.env['res.partner'].search([
                                    ('hr_employee_id', '=', loop_6.id)]):
                                    classifier_super_admin.append(agent.id)

        if classifier_super_admin:
            classifier_super_admin.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', classifier_super_admin)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        if classifier_head:
            classifier_head.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', classifier_head)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', reg_in_head)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', unit_manager)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        if classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', classifier_incharge_head)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }

        if classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', 'in', classifier_incharge)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }
        else :
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Commissions'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'commission.settlement',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('agent_id', '=', user_id.partner_id.id)],
                'views': [(self.env.ref('commission.view_settlement_form').id or False, 'form'),
                          (self.env.ref('commission.view_settlement_tree').id or False, 'tree')],

            }


class SettlementLine(models.Model):
    _name = "commission.settlement.line"
    _description = "Line of a commission settlement"

    settlement_id = fields.Many2one(
        "commission.settlement",
        readonly=True,
        ondelete="cascade",
        required=True,
    )
    date = fields.Date(
        compute="_compute_date",
        readonly=False,
        store=True,
        required=True,
    )
    agent_id = fields.Many2one(
        comodel_name="res.partner",
        related="settlement_id.agent_id",
        store=True,
    )
    settled_amount = fields.Monetary(
        compute="_compute_settled_amount", readonly=False, store=True)
    currency_id = fields.Many2one(
        related="settlement_id.currency_id",
        comodel_name="res.currency",
        store=True,
        readonly=True,
    )
    commission_id = fields.Many2one(
        comodel_name="commission",
        compute="_compute_commission_id",
        readonly=False,
        store=True,
        required=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        related="settlement_id.company_id",
        store=True,
    )

    # def default_get(self, fields_list):
    #     res = super(SettlementLine, self).default_get(fields_list)
    #     total = 0
    #     for rec in self.settlement_id.reta_order:
    #         total += rec.commission
    #     res['settled_amount'] = total
    #     return res

    def _compute_date(self):
        """Empty hook for allowing in children modules to auto-compute this field
        depending on the settlement line source.
        """

    def _compute_commission_id(self):
        """Empty hook for allowing in children modules to auto-compute this field
        depending on the settlement line source.
        """

    def _compute_settled_amount(self):
        """Empty container for allowing in children modules to auto-compute this
        amount depending on the settlement line source.
        """


class RetaOrders(models.Model):
    _name = 'reta.orders'

    cio = fields.Many2one('sale.order', domain=[('reta_bool_field', '=', True)])
    total_amt = fields.Float('Total Amount')
    amount_paid = fields.Float('Amount Paid')
    commission = fields.Float('Commission', compute='_compute_commision')
    date = fields.Date('Date')
    reta_order = fields.Char('Reta Order')
    commission_settlement = fields.Many2one('commission.settlement')

    def _compute_commision(self):
        for rec in self:
            if rec.commission_settlement.commission_type == 'fixed_amount' and rec.total_amt == rec.amount_paid:
                rec.commission = rec.commission_settlement.fixed_amt
            elif rec.commission_settlement.commission_type == 'percent' and rec.total_amt == rec.amount_paid:
                percent = rec.total_amt * rec.commission_settlement.commission_per
                rec.commission = percent / 100
            else:
                rec.commission = 0.00


# for classified commission
class ClassifiedOrdersCommission(models.Model):
    _name = 'classified.orders.commission'
    classifed = fields.Many2one('sale.order')
    total_amt = fields.Float('Total Sale')
    amount_paid = fields.Float('Amount Paid')
    commission = fields.Float('Commission', compute='_compute_commision')
    date = fields.Date('Date')
    reta_order = fields.Char('Classified Order')
    commission_settlement_classified = fields.Many2one('commission.settlement')

    def _compute_commision(self):
        for rec in self:
            print(rec)
            if rec.commission_settlement_classified.commission_type == 'fixed_amount' and rec.total_amt == rec.amount_paid:
                rec.commission = rec.commission_settlement_classified.fixed_amt
            elif rec.commission_settlement_classified.commission_type == 'percent' and rec.total_amt == rec.amount_paid:
                percent = rec.total_amt * rec.commission_settlement_classified.commission_per
                rec.commission = percent / 100
            else:
                rec.commission = 0.00
