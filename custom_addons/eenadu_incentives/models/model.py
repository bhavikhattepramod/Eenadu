from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _rec_name = 'name'

    # fields of employee table
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    incentive_type = fields.Selection([('fixed_amt', 'Fixed Amount'), ('percentage', 'Percentage')])
    incentive_amt = fields.Monetary('Incentive Amount', currency_field='currency_id')
    incentive_percent = fields.Integer('Incentive')


class IncentiveClass(models.Model):
    _name = 'partner.incentive'
    _rec_name = 'unit_name'

    # fields of partner incentive table
    reta = fields.Boolean('Is Reta Deposit')  # for reta module
    classified = fields.Boolean('Is Classified Deposit')  # for Classified module
    classified_line = fields.One2many('partner.incentive.line.classified',
                                      'incentive_classified')  # for Classified module
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.company.currency_id)  # link to monetary field
    partner_id = fields.Many2one('res.partner', string='Partners')
    target_amt = fields.Monetary(string='Target Amount', currency_field='currency_id')
    so_total = fields.Monetary(string='Sale Total', currency_field='currency_id')
    payment_total = fields.Monetary(string='Payment Total', currency_field='currency_id')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')
    unit_name = fields.Many2one('unit.master', "Unit Name")
    achieved_amt = fields.Monetary(string='Achieved Amount', compute='_compute_amount_sum')
    incentive_line = fields.One2many('partner.incentive.line', 'incentive', string='Incentive Lines')
    incentive_state = fields.Selection(
        [('draft', 'New'), ('running', 'Running'), ('disperse', 'Disperse'), ('paid', 'Paid')], default='draft')

    def action_running(self):  # button for validation and state change button name = 'Process'
        if not self.target_amt:
            raise ValidationError('Please Enter the Targe Amount')
        if self.reta:
            print(self.incentive_line, 'running incentive')
            for rec in self.incentive_line:
                if not rec.target_amt:
                    raise ValidationError('Please Enter the Target Amount')
            self.incentive_state = 'running'
        elif self.classified:
            # for Classified module
            print(self.classified_line, 'clasiified running')
            for classified in self.classified_line:
                if not classified.target_amt:
                    raise ValidationError('Please Enter the Target Amount')
            self.incentive_state = 'running'

    # method to compute achieved amount
    def _compute_amount_sum(self):
        sum_amt = 0.0
        if self.reta:
            print(self.incentive_line, 'incentive')
            for record in self.incentive_line:
                if record.recieved_payment:
                    sum_amt += record.recieved_payment
                    self.achieved_amt = sum_amt
        elif self.classified:
            # for Classified module
            print('clasiified incentive', self.classified_line)
            for classified in self.classified_line:
                if classified.recieved_payment:
                    sum_amt += classified.recieved_payment
                    self.achieved_amt = sum_amt
        return self.achieved_amt

    # method to create order lines
    # for classified module
    @api.constrains('unit_name', 'from_date', 'to_date')
    def create_order_lines(self):
        employee_obj = self.env['hr.employee'].search([('unit_name_hr', '=', self.unit_name.id)])
        # creation of partner in lines
        if self.reta == True:
            print('reta', self.reta)
            if employee_obj:
                for employee in employee_obj:
                    incentive_emp = self.incentive_line.create({
                        'employee_id': employee.id,
                        'partner_id': employee.user_partner_id.id,
                        'incentive': self.id,
                    })
                    # child_emp_obj = self.env['hr.employee'].search([('id', 'child_of', employee.id)])
                    # print('-3-',child_emp_obj,'-3-')
                    sale_obj = self.env['sale.order'].search([('agent_name', '=', employee.user_partner_id.id),
                                                              ('date_order', '>=', self.from_date),
                                                              ('date_order', '<=', self.to_date),
                                                              ('reta_bool_field', '=', True),
                                                              ('reta_state', 'in', ('sale', 'print', 'done'))])

                    # print(child_emp_obj,'-child_emp_obj-')
                    so_total = 0.0
                    so_paid_total = 0.0
                    for so in sale_obj:
                        so_total += so.amount_total
                        so_paid_total += so.cio_paid_amount

                    # for child_emp in child_emp_obj:
                    #     if child_emp.id != employee.id:
                    #         child_so_obj = self.env['sale.order'].search([('agent_name','=',child_emp.user_partner_id.id),
                    #                                                   ('date_order', '>=',self.from_date),
                    #                                                   ('date_order', '<=', self.to_date),
                    #                                                   ('reta_bool_field', '=', True),
                    #                                                   ('reta_state', 'in', ('sale','print','done'))])
                    #         for child_so in child_so_obj:
                    #             so_total += child_so.amount_total
                    #             so_paid_total += child_so.cio_paid_amount

                    # update incentive lines based on partner which was added in create method
                    incentive_emp.update({
                        'so_total_amt': so_total,
                        'recieved_payment': so_paid_total
                    })

                    if incentive_emp.employee_id.incentive_type:
                        if incentive_emp.employee_id.incentive_type == 'fixed_amt':
                            incentive_emp.update({
                                'incentive_amt': incentive_emp.employee_id.incentive_amt
                            })
        # for Classified module
        elif self.classified == True:
            print('classifie', self.classified)
            if employee_obj:
                for employee in employee_obj:
                    incentive_emp = self.classified_line.create({
                        'employee_id': employee.id,
                        'partner_id': employee.user_partner_id.id,
                        'incentive_classified': self.id,
                    })
                    # child_emp_obj = self.env['hr.employee'].search([('id', 'child_of', employee.id)])
                    # print('-3-',child_emp_obj,'-3-')
                    sale_obj = self.env['sale.order'].search([('agent_name', '=', employee.user_partner_id.id),
                                                              ('date_order', '>=', self.from_date),
                                                              ('date_order', '<=', self.to_date),
                                                              ('classified_bool_field', '=', True),
                                                              ('classified_state', 'in', ('sale', 'print', 'done'))])

                    # print(sale_obj.cio_paid_amount, '-child_emp_obj-')
                    so_total = 0.0
                    so_paid_total = 0.0
                    for so in sale_obj:
                        so_total += so.amount_total
                        so_paid_total += so.cio_paid_amount

                    # update incentive lines based on partner which was added in create method
                    incentive_emp.update({
                        'so_total_amt': so_total,
                        'recieved_payment': so_paid_total
                    })

                    if incentive_emp.employee_id.incentive_type:
                        if incentive_emp.employee_id.incentive_type == 'fixed_amt':
                            incentive_emp.update({
                                'incentive_amt': incentive_emp.employee_id.incentive_amt
                            })

    def action_make_payment(self):
        for incentive in self:
            if incentive.achieved_amt < incentive.target_amt:
                raise ValidationError('Target Not Reached')

            else:
                return {
                    "type": "ir.actions.act_window",
                    "name": _("Create Vendor Bills"),
                    "res_model": "incentive.wizard",
                    "target": "new",
                    "view_mode": "form",
                }

    def action_view_payment(self):
        return {
            'name': ('Incentive Payment Details'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('incentive_ref', '=', self[0].id)],
            'views_id': False,
            'views': [(self.env.ref('account.view_in_invoice_bill_tree').id or False, 'tree'),
                      (self.env.ref('account.view_move_form').id or False, 'form')]
        }


class IncentiveLines(models.Model):
    _name = 'partner.incentive.line'

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    incentive = fields.Many2one('partner.incentive')
    partner_id = fields.Many2one('res.partner', string='Partners')
    target_amt = fields.Monetary(string='Target Amount', currency_field='currency_id')
    so_total_amt = fields.Monetary(string='SO Total Value', currency_field='currency_id')
    incentive_amt = fields.Monetary(string='Incentive Amount', currency_field='currency_id',
                                    compute='_compute_incentive_amount')
    recieved_payment = fields.Monetary(string='Recieved Payment', currency_field='currency_id')
    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    progress = fields.Integer('Progress', compute="_compute_progress")

    @api.depends('target_amt', 'recieved_payment')
    def _compute_progress(self):
        for rec in self:
            if rec.target_amt != 0.00:
                percentage = abs((rec.recieved_payment / rec.target_amt) * 100)
            else:
                percentage = 0
            if percentage <= 100:
                rec.progress = percentage
            else:
                rec.progress = 100

    @api.depends('target_amt', 'employee_id')
    def _compute_incentive_amount(self):
        for rec in self:
            if rec.target_amt < rec.recieved_payment:
                if rec.employee_id and rec.target_amt:
                    if rec.employee_id.incentive_type == 'percentage':
                        rec.incentive_amt = rec.target_amt * (rec.employee_id.incentive_percent / 100)
                    else:
                        rec.incentive_amt = rec.employee_id.incentive_amt
                else:
                    rec.incentive_amt = 0.00
            else:
                rec.incentive_amt = 0.00

    def reta_dashboard_incentive(self):
        user = self.env.uid
        user_id = self.env['res.users'].browse(user)
        reta_incharge = [agent.id for agent in self.env['hr.employee'].search([
            ('parent_id.user_id', '=', user_id.id)])]
        reta_incharge_head = []
        for incharge_head in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for incharge in self.env['hr.employee'].search([('parent_id', '=', incharge_head.id)]):
                reta_incharge_head.append(incharge.id)
                for agent in self.env['hr.employee'].search([('parent_id', '=', incharge.id)]):
                    reta_incharge_head.append(agent.id)
        unit_manager = []
        for loop_1 in self.env['hr.employee'].search([('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                unit_manager.append(loop_2.id)
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    unit_manager.append(loop_3.id)
                    for agent in self.env['hr.employee'].search([('parent_id', '=', loop_3.id)]):
                        unit_manager.append(agent.id)

        reg_in_head = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                reg_in_head.append(loop_2.id)
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    reg_in_head.append(loop_3.id)
                    for loop_4 in self.env['hr.employee'].search([('parent_id', '=', loop_3.id)]):
                        reg_in_head.append(loop_4.id)
                        for agent in self.env['hr.employee'].search([('parent_id', '=', loop_4.id)]):
                            reg_in_head.append(agent.id)

        reta_head = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                reta_head.append(loop_2.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    reta_head.append(loop_3.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        reta_head.append(loop_4.id)
                        for loop_5 in self.env['hr.employee'].search([
                            ('parent_id', '=', loop_4.id)]):
                            reta_head.append(loop_5.id)
                            for agent in self.env['hr.employee'].search([
                                ('parent_id', '=', loop_5.id)]):
                                reta_head.append(agent.id)

        reta_super_admin = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                reta_super_admin.append(loop_2.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    reta_super_admin.append(loop_3.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        reta_super_admin.append(loop_4.id)
                        for loop_5 in self.env['hr.employee'].search([
                            ('parent_id', '=', loop_4.id)]):
                            reta_super_admin.append(loop_5.id)
                            for loop_6 in self.env['hr.employee'].search([
                                ('parent_id', '=', loop_5.id)]):
                                reta_super_admin.append(loop_6.id)
                                for agent in self.env['hr.employee'].search([
                                    ('parent_id', '=', loop_6.id)]):
                                    reta_super_admin.append(agent.id)
        # reta_super_admin.append(user_id.partner_id.id)
        if reta_super_admin:
            reta_super_admin.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reta_super_admin),
                           ('incentive.reta', '=', True),],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if reta_head:
            reta_head.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reta_head),
                           ('incentive.reta', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reg_in_head),
                           ('incentive.reta', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', unit_manager),
                           ('incentive.reta', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if reta_incharge_head:
            reta_incharge_head.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reta_incharge_head),
                           ('incentive.reta', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if reta_incharge:
            reta_incharge.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reta_incharge),
                           ('incentive.reta', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        else:
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id.user_id', '=', user_id.id),
                           ('incentive.reta', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }

    def classifier_dashboard_incentive(self):
        user = self.env.uid
        user_id = self.env['res.users'].browse(user)
        reta_incharge = [agent.id for agent in self.env['hr.employee'].search([
            ('parent_id.user_id', '=', user_id.id)])]
        reta_incharge_head = []
        for incharge_head in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for incharge in self.env['hr.employee'].search([('parent_id', '=', incharge_head.id)]):
                reta_incharge_head.append(incharge.id)
                for agent in self.env['hr.employee'].search([('parent_id', '=', incharge.id)]):
                    reta_incharge_head.append(agent.id)
        unit_manager = []
        for loop_1 in self.env['hr.employee'].search([('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                unit_manager.append(loop_2.id)
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    unit_manager.append(loop_3.id)
                    for agent in self.env['hr.employee'].search([('parent_id', '=', loop_3.id)]):
                        unit_manager.append(agent.id)

        reg_in_head = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                reg_in_head.append(loop_2.id)
                for loop_3 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                    reg_in_head.append(loop_3.id)
                    for loop_4 in self.env['hr.employee'].search([('parent_id', '=', loop_3.id)]):
                        reg_in_head.append(loop_4.id)
                        for agent in self.env['hr.employee'].search([('parent_id', '=', loop_4.id)]):
                            reg_in_head.append(agent.id)

        reta_head = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_2.id)]):
                reta_head.append(loop_2.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    reta_head.append(loop_3.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        reta_head.append(loop_4.id)
                        for loop_5 in self.env['hr.employee'].search([
                            ('parent_id', '=', loop_4.id)]):
                            reta_head.append(loop_5.id)
                            for agent in self.env['hr.employee'].search([
                                ('parent_id', '=', loop_5.id)]):
                                reta_head.append(agent.id)

        reta_super_admin = []
        for loop_1 in self.env['hr.employee'].search([
            ('user_id', '=', user_id.id)]):
            for loop_2 in self.env['hr.employee'].search([('parent_id', '=', loop_1.id)]):
                reta_super_admin.append(loop_2.id)
                for loop_3 in self.env['hr.employee'].search([
                    ('parent_id', '=', loop_2.id)]):
                    reta_super_admin.append(loop_3.id)
                    for loop_4 in self.env['hr.employee'].search([
                        ('parent_id', '=', loop_3.id)]):
                        reta_super_admin.append(loop_4.id)
                        for loop_5 in self.env['hr.employee'].search([
                            ('parent_id', '=', loop_4.id)]):
                            reta_super_admin.append(loop_5.id)
                            for loop_6 in self.env['hr.employee'].search([
                                ('parent_id', '=', loop_5.id)]):
                                reta_super_admin.append(loop_6.id)
                                for agent in self.env['hr.employee'].search([
                                    ('parent_id', '=', loop_6.id)]):
                                    reta_super_admin.append(agent.id)
        # reta_super_admin.append(user_id.partner_id.id)
        if reta_super_admin:
            reta_super_admin.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reta_super_admin),
                           ('incentive.classified', '=', True),],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if reta_head:
            reta_head.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reta_head),
                           ('incentive.classified', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reg_in_head),
                           ('incentive.classified', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', unit_manager),
                           ('incentive.classified', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if reta_incharge_head:
            reta_incharge_head.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reta_incharge_head),
                           ('incentive.classified', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        if reta_incharge:
            reta_incharge.append(user_id.employee_id.id)
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id', 'in', reta_incharge),
                           ('incentive.classified', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }
        else:
            return {
                'name': _('Incentives'),
                'type': 'ir.actions.act_window',
                'view_type': 'tree',
                'view_mode': 'tree',
                'res_model': 'partner.incentive.line',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('employee_id.user_id', '=', user_id.id),
                           ('incentive.classified', '=', True),
                           ],
                'views': [(self.env.ref('eenadu_incentives.employee_incentives_tree_view').id or False, 'tree')],

            }


class AccountMoveVendor(models.Model):
    _inherit = 'account.move'
    _description = 'vendor bill value pass'

    incentive_ref = fields.Many2one('partner.incentive',
                                    'Incentive Ref')  # to pass domain for particular vendor bills for particular incentive form


class IncentiveLinesClassified(models.Model):
    _name = 'partner.incentive.line.classified'

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    incentive_classified = fields.Many2one('partner.incentive')
    partner_id = fields.Many2one('res.partner', string='Partners')
    target_amt = fields.Monetary(string='Target Amount', currency_field='currency_id')
    so_total_amt = fields.Monetary(string='SO Total Value', currency_field='currency_id')
    incentive_amt = fields.Monetary(string='Incentive Amount', currency_field='currency_id',
                                    compute='_compute_incentive_amount')
    recieved_payment = fields.Monetary(string='Recieved Payment', currency_field='currency_id')
    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    progress = fields.Integer('Progress', compute="_compute_progress")

    @api.depends('target_amt', 'recieved_payment')
    def _compute_progress(self):
        for rec in self:
            if rec.target_amt != 0.00:
                percentage = abs((rec.recieved_payment / rec.target_amt) * 100)
            else:
                percentage = 0
            if percentage <= 100:
                rec.progress = percentage
            else:
                rec.progress = 100

    @api.depends('target_amt', 'employee_id')
    def _compute_incentive_amount(self):
        for rec in self:
            if rec.target_amt < rec.recieved_payment:
                if rec.employee_id and rec.target_amt:
                    if rec.employee_id.incentive_type == 'percentage':
                        rec.incentive_amt = rec.target_amt * (rec.employee_id.incentive_percent / 100)
                    else:
                        rec.incentive_amt = rec.employee_id.incentive_amt
                else:
                    rec.incentive_amt = 0.00
            else:
                rec.incentive_amt = 0.00
