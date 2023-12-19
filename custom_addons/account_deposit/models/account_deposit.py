from odoo import api, fields, models, _
from datetime import datetime
import calendar
from odoo import exceptions
from odoo.exceptions import AccessError, UserError, ValidationError


class AccountDeposit(models.Model):
    _name = "account.deposit"

    name = fields.Char('Name', readonly=True, copy=False, default='DEP')

    @api.model
    def create(self, vals_list):
        deposit_agent = self.env['account.deposit'].search(
            [('partner_id', '=', vals_list['partner_id']), ('status', '=', 'running')])
        if deposit_agent:
            raise exceptions.ValidationError(
                "You can't create new deposit,Because your deposit {} is in running state.".format(deposit_agent.name))
        agent = self.env['res.partner'].browse(vals_list['partner_id'])
        if agent.agent_code:
            if vals_list.get('name', 'DEP') == 'DEP':
                vals_list['name'] = str(agent.agent_code) + self.env['ir.sequence'].next_by_code(
                    str(agent.name) + '.DEP') or 'DEP'
        return super(AccountDeposit, self).create(vals_list)

    reta = fields.Boolean('Is Reta Deposit')
    classifier = fields.Boolean('Is classifier Deposit')
    circulation = fields.Boolean('Is circulation')
    partner_id = fields.Many2one('res.partner', 'Partner')
    deposit_amt = fields.Float('Initial Amount')
    interest_percent = fields.Float('Interest Percentage', digits=(5, 2))
    total_outstanding = fields.Float('Total Outstanding', compute='compute_total_outstanding',
                                     help='It is visible when "paid_bool" field is False', store=True)

    deposit_history_ids = fields.One2many('account.deposit.history', 'account_m2n_h')
    deposit_increment = fields.One2many('deposit.outstanding', 'account_m2n')

    deposit_amt_interest_percent = fields.Float('Interest', compute='compute_deposit_amt_interest_percent')

    status = fields.Selection(selection=[('new', 'New'),
                                         ('running', 'Running'),
                                         ('completed', 'Completed')], default='new')
    remaining_amount_payment = fields.Integer('Total Outstanding', help='It is visible when "paid_bool" field is True')

    payments_made = fields.Float('Total Payments Made', compute='payments_count')
    account_payment = fields.One2many('account.payment', 'deposit_ref')

    user_id = fields.Many2one('res.users', related="partner_id.user_id")
    # display total amt paid
    paid_amt = fields.Float('Total Paid')
    # display last amt paid
    total_paid = fields.Float('last Paid')
    # bool field when the bool field is false then amt will be taken from the total outstanding
    # when its True amt will be taken from remaining_amount_payment
    # it will become true when the partial payment will be created
    # once after adding the line in outstanding total page with the remaining_amount_payment the bool field will become false
    # and for nxt line amt will be taken from total outstanding based on that the amt will be calculated
    paid_bool = fields.Boolean('', default=False)

    added_deposit = fields.Float('Added Deposit')
    invoices_count = fields.Integer('', compute='_compute_invoices_count')
    deposit_history_count = fields.Integer('', compute='_compute_deposit_history_count')
    deposit_interest_count = fields.Integer('', compute='_compute_deposit_interest_count')

    def _compute_deposit_interest_count(self):
        self.deposit_interest_count = self.env['account.move'].search_count(
            [('account_deposit_interest', '=', self.id)])

    def _compute_deposit_history_count(self):
        self.deposit_history_count = self.env['account.move'].search_count(
            ['|', ('account_deposit_interest', '=', self.id), ('account_deposit', '=', self.id)])

    def action_view_deposit_interest(self):
        domain = [('account_deposit_interest', '=', self.id)]
        action = {
            'name': 'Deposit Interest',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'target': 'current',
        }
        return action

    def action_view_deposit_history(self):
        # view_id = self.env.ref('account_deposit.deposit_history_tree_view').id
        domain = ['|', ('account_deposit_interest', '=', self.id), ('account_deposit', '=', self.id)]
        action = {
            'name': 'Deposit History',
            'view_mode': 'tree,form',
            # 'view_id': view_id,
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'target': 'current',
        }
        return action

    # for calling the action of the wizard (su)
    def add_deposit(self):
        action = self.env.ref('account_deposit.deposit_wizard_action').read()[0]
        return action

    def _compute_invoices_count(self):
        self.invoices_count = self.env['account.move'].search_count(
            [('agent_name', '=', self.partner_id.id), ('payment_state', 'in', ['not_paid', 'partial']),
             ('move_type', '=', 'out_invoice')])

    def action_view_invoices_deposit(self):
        domain = [('agent_name', '=', self.partner_id.id), ('payment_state', 'in', ['not_paid', 'partial']),
                  ('move_type', '=', 'out_invoice')]
        action = {
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'target': 'current',
        }
        return action

    # new
    def compute_remaining(self):
        for paid in self:
            if paid.total_paid:
                if paid.paid_bool == True:
                    if paid.remaining_amount_payment != 0:
                        total = paid.remaining_amount_payment - paid.total_paid
                        if total < 0:
                            paid.remaining_amount_payment = -(total)
                        else:
                            paid.remaining_amount_payment = total
                    else:
                        paid.remaining_amount_payment = paid.total_outstanding - paid.total_paid
            else:
                paid.remaining_amount_payment = 0

            # if paid.remaining_amount_payment < 0:
            #     paid.remaining_amount_payment = -(paid.remaining_amount_payment)

    def payments_count(self):
        for payments in self:
            payments.payments_made = len(payments.account_payment)

    def view_payment(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("account_deposit.action_view_deposit_adv_payment")
        return action

    def action_view_payment(self):
        return {
            'name': ('Deposit Payment Details'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'domain': [('deposit_ref', '=', self[0].id)],
            'views_id': False,
            'views': [(self.env.ref('account.view_account_payment_tree').id or False, 'tree'),
                      (self.env.ref('account.view_account_payment_form').id or False, 'form')]
        }

    def running(self):
        journal = self.env['account.journal'].search([('is_deposit', '=', True)])
        product = self.env['product.product'].search([('is_deposit', '=', True)])
        for rec in self:
            rec.status = 'running'
            if product:
                line_vals = {
                    'product_id': product.id,
                    'price_unit': rec.deposit_amt,
                    'tax_ids': False,
                }
            else:
                raise UserError('Please create Product named as Deposit and Check Is Deposit? checkbox')
            if journal:
                vals = {
                    'move_type': 'out_refund',
                    'journal_id': journal.id,
                    'partner_id': rec.partner_id.id,
                    'account_deposit': rec.id,
                    # 'deposit_ref': rec.id,
                    'invoice_line_ids': [(0, 0, line_vals)]
                }
            else:
                raise UserError('Please create a Journal named as Deposit and Check Is Deposit? checkbox')
            self.env['account.move'].create(vals).action_post()

    def completed(self):
        for rec in self:
            rec.status = 'completed'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Thank You',
                'type': 'rainbow_man',
            }
        }

    def compute_deposit_amt_interest_percent(self):
        for line in self:
            if line.total_outstanding == 0.00:
                interest = line.deposit_amt * line.interest_percent / 100
                line.deposit_amt_interest_percent = interest
            else:
                # if line.remaining_amount_payment == 0:
                if line.paid_bool == False:
                    interest = line.total_outstanding * line.interest_percent / 100

                    line.deposit_amt_interest_percent = interest
                else:
                    interest = line.remaining_amount_payment * line.interest_percent / 100
                    line.deposit_amt_interest_percent = interest

    @api.depends('deposit_increment', 'deposit_amt')
    def compute_total_outstanding(self):
        total = 0
        for rec in self:
            # if rec.total_outstanding == 0.00:
            for line in rec.deposit_increment:
                # total += line.outstanding_amt
                rec.total_outstanding = line.outstanding_amt
            if rec.total_outstanding == 0:
                rec.total_outstanding = rec.deposit_amt

    def add_cron_line(self):
        model = self.env['account.deposit'].search([('status', '=', 'running')])
        today = datetime.today()
        current_month = today.month
        month_name = calendar.month_name[current_month]
        current_year = today.year
        journal = self.env['account.journal'].search([('is_deposit_interest', '=', True)])
        product = self.env['product.product'].search([('is_deposit_interest', '=', True)])
        for rec in model:
            browse = self.env['account.deposit'].browse(rec.id)
            total = 1
            for res in browse.deposit_increment:
                total = res.periodd + 1
            if browse.total_outstanding == 0.00:
                add = browse.deposit_increment.create({
                    'period': str(month_name) + '/' + str(current_year),
                    'interest_amt': browse.deposit_amt_interest_percent,
                    'actual_amt': browse.deposit_amt,
                })
                browse.deposit_increment += add
                if product:
                    line_vals = {
                        'product_id': product.id,
                        'price_unit': browse.deposit_amt_interest_percent,
                        'tax_ids': False,
                    }
                else:
                    raise UserError('Please create Product named as Deposit Interest and Check Is Deposit Interest? checkbox')
                if journal:
                    vals = {
                        'invoice_date': fields.datetime.today(),
                        'move_type': 'out_refund',
                        'journal_id': journal.id,
                        'partner_id': browse.partner_id.id,
                        'account_deposit_interest': browse.id,
                        # 'deposit_ref': rec.id,
                        'invoice_line_ids': [(0, 0, line_vals)]
                    }
                else:
                    raise UserError("Please create a Journal named as Deposit Interest and Check Is Deposit Interest? checkbox")
                self.env['account.move'].create(vals).action_post()

            else:
                # if browse.remaining_amount_payment == 0:
                if browse.paid_bool == False:
                    add = browse.deposit_increment.create({
                        'period': str(month_name) + '/' + str(current_year),
                        'interest_amt': browse.deposit_amt_interest_percent,
                        'actual_amt': browse.total_outstanding,
                    })
                    browse.deposit_increment += add
                    if product:
                        line_vals = {
                            'product_id': product.id,
                            'price_unit': browse.deposit_amt_interest_percent,
                            'tax_ids': False,
                        }
                    else:
                        raise UserError('Please create Product named as Deposit Interest and Check Is Deposit Interest? checkbox')
                    if journal:
                        vals = {
                            'invoice_date': fields.datetime.today(),
                            'move_type': 'out_refund',
                            'journal_id': journal.id,
                            'partner_id': browse.partner_id.id,
                            'account_deposit_interest': browse.id,
                            # 'deposit_ref': rec.id,
                            'invoice_line_ids': [(0, 0, line_vals)]
                        }
                    else:
                        raise UserError("Please create a Journal named as Deposit Interest and Check Is Deposit Interest? checkbox")
                    self.env['account.move'].create(vals).action_post()
                else:
                    add = browse.deposit_increment.create({
                        'period': str(month_name) + '/' + str(current_year),
                        'interest_amt': browse.deposit_amt_interest_percent,
                        'actual_amt': browse.remaining_amount_payment,
                    })
                    browse.deposit_increment += add
                    if product:
                        line_vals = {
                            'product_id': product.id,
                            'price_unit': browse.deposit_amt_interest_percent,
                            'tax_ids': False,
                        }
                    else:
                        raise UserError('Please create Product named as Deposit Interest and Check Is Deposit Interest? checkbox')
                    if journal:
                        vals = {
                            'invoice_date': fields.datetime.today(),
                            'move_type': 'out_refund',
                            'journal_id': journal.id,
                            'partner_id': browse.partner_id.id,
                            'account_deposit_interest': browse.id,
                            # 'deposit_ref': rec.id,
                            'invoice_line_ids': [(0, 0, line_vals)]
                        }
                    else:
                        raise UserError("Please create a Journal named as Deposit Interest and Check Is Deposit Interest? checkbox")
                    self.env['account.move'].create(vals).action_post()
                    browse.paid_bool = False
                    browse.total_paid = 0

    @api.model
    def agent_deposits(self):
        # here you can filter you records as you want
        user = self.env.uid
        user_id = self.env['res.users'].browse(user)
        field_segment_incharge = []
        for loop_1 in self.env['res.partner'].search([('hr_employee_id.user_id', '=', user_id.id)]):
            field_segment_incharge.append(loop_1.id)
        publications_incharge = []
        publications_incharge_list = []
        for loop_1 in self.env['hr.employee'].search([('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                for agent in self.env['res.partner'].search([('hr_employee_id', '=', loop_2.id)]):
                    publications_incharge_list.append(agent.id)
                    if agent.id in publications_incharge_list:
                        publications_incharge.append(loop_1.user_partner_id.id)
                        publications_incharge.append(loop_2.user_partner_id.id)
                        publications_incharge.append(agent.id)
        circulation_incharge = []
        circulation_incharge_agent_list = []
        for loop_1 in self.env['hr.employee'].search([('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    for agent in self.env['res.partner'].search([('hr_employee_id', '=', loop_3.id)]):
                        circulation_incharge_agent_list.append(agent.id)
                        if agent.id in circulation_incharge_agent_list:
                            circulation_incharge.append(loop_1.user_partner_id.id)
                            circulation_incharge.append(loop_2.user_partner_id.id)
                            circulation_incharge.append(loop_3.user_partner_id.id)
                            circulation_incharge.append(agent.id)
        unit_incharge = []
        unit_incharge_list = []
        for loop_1 in self.env['hr.employee'].search([('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    for loop_4 in self.env['hr.employee'].search([('parent_id', '=', loop_3.id)]):
                        for agent in self.env['res.partner'].search([('hr_employee_id', '=', loop_4.id)]):
                            unit_incharge_list.append(agent.id)
                            if agent.id in unit_incharge_list:
                                unit_incharge.append(loop_1.user_partner_id.id)
                                unit_incharge.append(loop_2.user_partner_id.id)
                                unit_incharge.append(loop_3.user_partner_id.id)
                                unit_incharge.append(loop_4.user_partner_id.id)
                                unit_incharge.append(agent.id)
        regional_head = []
        regional_head_list = []
        for loop_1 in self.env['hr.employee'].search([('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    for loop_4 in self.env['hr.employee'].search([('parent_id', '=', loop_3.id)]):
                        for loop_5 in self.env['hr.employee'].search([('parent_id', '=', loop_4.id)]):
                            for agent in self.env['res.partner'].search([('hr_employee_id', '=', loop_5.id)]):
                                regional_head_list.append(agent.id)
                                if agent.id in regional_head_list:
                                    regional_head.append(loop_1.user_partner_id.id)
                                    regional_head.append(loop_2.user_partner_id.id)
                                    regional_head.append(loop_3.user_partner_id.id)
                                    regional_head.append(loop_4.user_partner_id.id)
                                    regional_head.append(loop_5.user_partner_id.id)
                                    regional_head.append(agent.id)
        circulation_admin = []
        circulation_admin_list = []
        for loop_1 in self.env['hr.employee'].search([('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    for loop_4 in self.env['hr.employee'].search([('parent_id', '=', loop_3.id)]):
                        for loop_5 in self.env['hr.employee'].search([('parent_id', '=', loop_4.id)]):
                            for loop_6 in self.env['hr.employee'].search([('parent_id', '=', loop_5.id)]):
                                for agent in self.env['res.partner'].search([('hr_employee_id', '=', loop_6.id)]):
                                    circulation_admin_list.append(agent.id)
                                    if agent.id in circulation_admin_list:
                                        circulation_admin.append(loop_1.user_partner_id.id)
                                        circulation_admin.append(loop_2.user_partner_id.id)
                                        circulation_admin.append(loop_3.user_partner_id.id)
                                        circulation_admin.append(loop_4.user_partner_id.id)
                                        circulation_admin.append(loop_5.user_partner_id.id)
                                        circulation_admin.append(loop_6.user_partner_id.id)
                                        circulation_admin.append(agent.id)
        circulation_head = []
        circulation_head_list = []
        for loop_1 in self.env['hr.employee'].search([('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    for loop_4 in self.env['hr.employee'].search([('parent_id', '=', loop_3.id)]):
                        for loop_5 in self.env['hr.employee'].search([('parent_id', '=', loop_4.id)]):
                            for loop_6 in self.env['hr.employee'].search([('parent_id', '=', loop_5.id)]):
                                for loop_7 in self.env['hr.employee'].search([('parent_id', '=', loop_6.id)]):
                                    for agent in self.env['res.partner'].search([('hr_employee_id', '=', loop_7.id)]):
                                        circulation_head_list.append(agent.id)
                                        if agent.id in circulation_head_list:
                                            circulation_head.append(loop_1.user_partner_id.id)
                                            circulation_head.append(loop_2.user_partner_id.id)
                                            circulation_head.append(loop_3.user_partner_id.id)
                                            circulation_head.append(loop_4.user_partner_id.id)
                                            circulation_head.append(loop_5.user_partner_id.id)
                                            circulation_head.append(loop_6.user_partner_id.id)
                                            circulation_head.append(loop_7.user_partner_id.id)
                                            circulation_head.append(agent.id)
        super_admin = []
        super_admin_list = []
        for loop_1 in self.env['hr.employee'].search([('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    for loop_4 in self.env['hr.employee'].search([('parent_id', '=', loop_3.id)]):
                        for loop_5 in self.env['hr.employee'].search([('parent_id', '=', loop_4.id)]):
                            for loop_6 in self.env['hr.employee'].search([('parent_id', '=', loop_5.id)]):
                                for loop_7 in self.env['hr.employee'].search([('parent_id', '=', loop_6.id)]):
                                    for loop_8 in self.env['hr.employee'].search([('parent_id', '=', loop_7.id)]):
                                        for agent in self.env['res.partner'].search(
                                                [('hr_employee_id', '=', loop_8.id)]):
                                            super_admin_list.append(agent.id)
                                            if agent.id in super_admin_list:
                                                super_admin.append(loop_1.user_partner_id.id)
                                                super_admin.append(loop_2.user_partner_id.id)
                                                super_admin.append(loop_3.user_partner_id.id)
                                                super_admin.append(loop_4.user_partner_id.id)
                                                super_admin.append(loop_5.user_partner_id.id)
                                                super_admin.append(loop_6.user_partner_id.id)
                                                super_admin.append(loop_7.user_partner_id.id)
                                                super_admin.append(loop_8.user_partner_id.id)
                                                super_admin.append(agent.id)
        if super_admin:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', super_admin), ('status', '=', 'running')],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if circulation_head:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', circulation_head), ('status', '=', 'running')],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if circulation_admin:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', circulation_admin), ('status', '=', 'running')],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if regional_head:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', regional_head), ('status', '=', 'running')],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if unit_incharge:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', unit_incharge), ('status', '=', 'running')],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if circulation_incharge:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', circulation_incharge), ('status', '=', 'running')],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if publications_incharge:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', publications_incharge), ('status', '=', 'running')],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if field_segment_incharge:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', field_segment_incharge), ('status', '=', 'running')],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }

    @api.model
    def reta_dashboard_deposits(self):
        # here you can filter you records as you want
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
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', reta_super_admin), ('status', '=', 'running'), ("reta", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if reta_head:
            reta_head.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', reta_head), ('status', '=', 'running'), ("reta", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', reg_in_head), ('status', '=', 'running'), ("reta", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', unit_manager), ('status', '=', 'running'), ("reta", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if reta_incharge_head:
            reta_incharge_head.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', reta_incharge_head), ('status', '=', 'running'), ("reta", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if reta_incharge:
            reta_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', reta_incharge), ('status', '=', 'running'), ("reta", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        else:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', '=', user_id.partner_id.id), ('status', '=', 'running'), ("reta", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }

    @api.model
    def classifier_dashboard_deposits(self):
        # here you can filter you records as you want
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
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', classifier_super_admin), ('status', '=', 'running'),
                           ("classifier", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }

        if classifier_head:
            classifier_head.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', classifier_head), ('status', '=', 'running'),
                           ("classifier", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', reg_in_head), ('status', '=', 'running'), ("classifier", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', unit_manager), ('status', '=', 'running'), ("classifier", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', classifier_incharge_head), ('status', '=', 'running'),
                           ("classifier", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        if classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', 'in', classifier_incharge), ('status', '=', 'running'),
                           ("classifier", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }
        else:
            return {
                'name': _('Deposits'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.deposit',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('partner_id', '=', user_id.partner_id.id), ('status', '=', 'running'),
                           ("classifier", "=", True)],
                'views': [(self.env.ref('account_deposit.account_deposit_form_view').id or False, 'form'),
                          (self.env.ref('account_deposit.account_deposit_tree_view').id or False, 'tree')],

            }

    # @api.onchange('deposit_amt')
    # def deposite_history(self):
    #     for record in self:
    #         previous_value = record._origin.deposit_amt if record._origin else False
    #         current_value = record.deposit_amt
    #         add = record.deposit_history_ids.create({
    #             'description': "Deposited Amount",
    #             'from_value': previous_value,
    #             'to_value': current_value,
    #         })
    #         if record.deposit_amt != 0.00:
    #             record.deposit_history_ids += add

    # @api.onchange('interest_percent')
    # def deposite_history_interest(self):
    #     for record in self:
    #         previous_value = record._origin.interest_percent if record._origin else False
    #         current_value = record.interest_percent
    #         add = record.deposit_history_ids.create({
    #             'description': "Interest Percent",
    #             'from_value': previous_value,
    #             'to_value': current_value,
    #         })
    #         if record.interest_percent != 0.00:
    #             record.deposit_history_ids += add


class DepositHitory(models.Model):
    _name = 'account.deposit.history'

    # description = fields.Char('Description')
    # from_value = fields.Float('From Value')
    # to_value = fields.Float('To Value')
    account_m2n_h = fields.Many2one('account.deposit')
    receipt_no = fields.Many2one('account.move', 'Receipt NO')
    receipt_date = fields.Date('Date', related='receipt_no.date')
    partner_id = fields.Many2one('res.partner', 'Partner')
    debit_amt = fields.Float('Debit')
    credit_amt = fields.Float('Credit')
    reta_bool = fields.Boolean('Reta bool')
    classified_bool = fields.Boolean('Classified')
    state = fields.Selection(selection=[('deposit', 'Deposit'),
                                        ('interest', 'Interest'),
                                        ('reconcile', 'Reconciled'), ('unreconcile', 'Unreconciled')], string='State')


class DepositOutstanding(models.Model):
    _name = 'deposit.outstanding'

    period = fields.Char('Period')
    periodd = fields.Integer('Period', default=1)
    actual_amt = fields.Float('Actual Amount')
    interest_amt = fields.Float('Interest Amount')
    outstanding_amt = fields.Float('Outstanding Amount', compute='compute_outstanding')
    account_m2n = fields.Many2one('account.deposit')

    @api.onchange('actual_amt', 'interest_amt')
    def compute_outstanding(self):
        for rec in self:
            # total = (rec.actual_amt * rec.account_m2n.interest_percent / 100)
            # rec.interest_amt = total
            rec.outstanding_amt = rec.actual_amt + rec.interest_amt

    @api.onchange('interest_amt', 'actual_amt')
    def compute_interest(self):
        # self.interest_amt = self.account_m2n.deposit_amt_interest_percent
        if self.account_m2n.total_outstanding == 0.00:
            self.actual_amt = self.account_m2n.deposit_amt
        else:
            self.actual_amt = self.account_m2n.total_outstanding


class AccountPaymentInheritSale(models.Model):
    _inherit = 'account.payment'

    deposit_ref = fields.Many2one('account.deposit', 'Reference')


class DepositAdvancePaymentInv(models.TransientModel):
    _name = 'deposit.payment.wizard'

    @api.model
    def default_get(self, fields_list):
        result = super(DepositAdvancePaymentInv, self).default_get(fields_list)
        active_id = self._context.get('active_id')
        account_deposit = self.env['account.deposit'].browse(active_id)

        if account_deposit.total_outstanding == 0:
            result['amount_payment_full'] = account_deposit.deposit_amt
        elif account_deposit.paid_bool == True:
            result['amount_payment_full'] = account_deposit.remaining_amount_payment
        else:
            result['amount_payment_full'] = account_deposit.total_outstanding

        # if account_deposit.remaining_amount_payment > 0:
        # # if account_deposit.paid_bool == True:
        #     result['amount_payment_full'] = account_deposit.remaining_amount_payment

        result['partner_id'] = account_deposit.partner_id
        result['deposit_id'] = account_deposit.id
        return result

    partner_id = fields.Many2one('res.partner', 'Customer Name')
    deposit_payment_method = fields.Selection(
        selection=[
            ('full', "Complete Payment"),
            ('partial', 'Partial Payment')
        ], default='full')
    deposit_id = fields.Many2one('account.deposit', 'Deposit Ref')

    amount_payment_full = fields.Float('Total Amount')

    amount_payment_partial = fields.Float('Partial Payment Amount')

    amount_remaining = fields.Float('Amount Remaining')

    @api.onchange('amount_payment_partial')
    def payment_remaining(self):

        for rec in self:
            active_id = self._context.get('active_id')
            account_dep = self.env['account.deposit'].browse(active_id)
            if rec.amount_payment_partial:
                rec.amount_remaining = rec.amount_payment_full - rec.amount_payment_partial
                account_dep.remaining_amount_payment = rec.amount_remaining
                account_dep.total_paid = rec.amount_payment_partial
                if account_dep.paid_amt == 0:
                    account_dep.paid_amt = rec.amount_payment_partial
                else:
                    total = account_dep.paid_amt + rec.amount_payment_partial
                    account_dep.paid_amt = total

            else:
                rec.amount_remaining = rec.amount_payment_full
            account_dep.paid_bool = True

    def create_payment(self):
        for rec in self:
            active_id = self._context.get('active_id')
            account_deposit = self.env['account.deposit'].browse(active_id)
            if rec.deposit_payment_method in 'full':
                account_deposit.status = 'completed'
            else:
                account_deposit.status = 'running'

        ctx = dict()

        ctx = ({
            'default_partner_id': self.partner_id.id,
            'default_amount': self.amount_payment_partial if self.deposit_payment_method == 'partial' else self.amount_payment_full,
            'default_deposit_ref': self.deposit_id.id
        })

        form_id = self.env.ref('account.view_account_payment_form').id

        return {
            'name': ('Deposit Payment'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.payment',
            'views_id': False,
            'views': [(form_id or False, 'form')],
            'target': 'current',
            'context': ctx,
        }


class ProductDotProduct(models.Model):
    _inherit = 'product.product'

    is_deposit = fields.Boolean('Is Deposit?')
    is_deposit_interest = fields.Boolean('Is Deposit Interest?')


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    is_deposit = fields.Boolean('Is Deposit?')
    is_deposit_interest = fields.Boolean('Is Deposit interest?')


class AccountMoveDeposit(models.Model):
    _inherit = 'account.move'

    account_deposit = fields.Many2one('account.deposit')
    account_deposit_interest = fields.Many2one('account.deposit')



    def js_assign_outstanding_line(self, line_id):
        res = super(AccountMoveDeposit, self).js_assign_outstanding_line(line_id)
        partial = self.env['account.partial.reconcile'].search([('id', '=', res['partials'].id)])
        lines = self.env['account.move.line'].browse(partial.credit_move_id.id)
        lines_move = self.env['account.move'].search([('id', '=', lines.move_id.id)])

        # updating the values in the account deposit while adding the reconciliation
        account_deposit = self.env['account.deposit'].search(
            [('partner_id', '=', self.partner_id.id), ('status', '=', 'running')])
        vals = {
            'receipt_no': lines_move.id,
            # 'receipt_date': lines_move.date,
            'partner_id': self.partner_id.id,
            'debit_amt': partial.amount,
            'reta_bool': account_deposit.reta,
            'classified_bool': account_deposit.classifier,
            'state': 'reconcile',

        }
        for rec in account_deposit:
            sub_outstanding = rec.total_outstanding - partial.amount
            rec.update({
                'total_outstanding': sub_outstanding,
                'deposit_history_ids': [(0, 0, vals)]
            })
        return res

    def js_remove_outstanding_partial(self, partial_id):
        # res = super(AccountMoveDeposit, self).js_remove_outstanding_partial(partial_id)
        partial = self.env['account.partial.reconcile'].browse(partial_id)
        lines = self.env['account.move.line'].browse(partial.credit_move_id.id)
        lines_move = self.env['account.move'].search([('id', '=', lines.move_id.id)])

        account_deposit = self.env['account.deposit'].search(
            [('partner_id', '=', self.partner_id.id), ('status', '=', 'running')])
        vals = {
            'receipt_no': lines_move.id,
            # 'receipt_date': lines_move.date,
            'partner_id': self.partner_id.id,
            'credit_amt': partial.amount,
            'reta_bool': account_deposit.reta,
            'classified_bool': account_deposit.classifier,
            'state': 'unreconcile',
        }
        for rec in account_deposit:
            sub_outstanding = rec.total_outstanding + partial.amount
            rec.update({
                'total_outstanding': sub_outstanding,
                'deposit_history_ids': [(0, 0, vals)]
            })
        return partial.unlink()

    def action_post(self):
        for rec in self:
            deposit = self.env['account.deposit'].search([('id', '=', rec.account_deposit.id)])
            deposit_interest = self.env['account.deposit'].search([('id', '=', rec.account_deposit_interest.id)])
            lines_vals = {
                'receipt_no': rec.id,
                'partner_id': rec.partner_id.id,
                'credit_amt': rec.amount_total,
                'reta_bool': deposit.reta,
                'classified_bool': deposit.classifier,
                'state': 'deposit'
                # 'receipt_date': rec.invoice_date
            }
            lines_vals_interest = {
                'receipt_no': rec.id,
                'partner_id': rec.partner_id.id,
                'credit_amt': rec.amount_total,
                'reta_bool': deposit_interest.reta,
                'classified_bool': deposit_interest.classifier,
                'state': 'interest',
                # 'receipt_date': rec.invoice_date
            }

            deposit.update({
                'deposit_history_ids': [(0, 0, lines_vals)]
            })
            deposit_interest.update({
                'deposit_history_ids': [(0, 0, lines_vals_interest)]
            })
        return super(AccountMoveDeposit, self).action_post()


class RespartnerDeposit(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals_list):
        self.env['ir.sequence'].create({
            'name': vals_list['name'],
            'code': vals_list['name'] + '.DEP',
            'prefix': '/DEP/',
            'padding': 5

        })
        return super(RespartnerDeposit, self).create(vals_list)
class CirculationPartners(models.Model):
    _inherit = 'res.partner'

    deposit_history_ids = fields.One2many('account.deposit.history', 'partner_id')
