# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#from odoo import models
from odoo import api, fields, models, tools, SUPERUSER_ID, _
import calendar
import random


class ClassifiedDashboard(models.Model):
    _name = 'classified.dashboard.data'

    def get_product_target_vals(self, user_id):
        user_id = self.env['res.users'].search([('id', '=', int(user_id))])
        target_obj = self.env['sales.person.target'].search(
            [('partner_id', '=', user_id.partner_id.id), ('is_classifieds_target', '=', True)])

        background_color1 = []
        border_color1 = []
        background_color2 = []
        border_color2 = []
        period_list = []
        received_payment = []
        target_amount = []

        incentive_obj = self.env['partner.incentive.line'].search([('partner_id', '=', user_id.partner_id.id)])

        for incentive in incentive_obj:
            if incentive.incentive.from_date:
                current_month = incentive.incentive.from_date.month
                month_name = calendar.month_name[current_month]
                current_year = incentive.incentive.from_date.year
            else:
                current_month = current_year = month_name = ''
            period_list.append(str(month_name) + ' ' + str(current_year))
            received_payment.append(round(incentive.recieved_payment, 2))
            target_amount.append(round(incentive.target_amt, 2))
            for i in range(len(incentive_obj)):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                rgb_str = "#{:02X}{:02X}{:02X}".format(r, g, b)
                rgba_str = str(rgb_str) + 'ad'
                background_color1.append(str(rgba_str))
                border_color1.append(str(rgba_str))
            for i in range(len(incentive_obj)):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                rgb_str = "#{:02X}{:02X}{:02X}".format(r, g, b)
                rgba_str = str(rgb_str) + 'ad'
                background_color2.append(str(rgba_str))
                border_color2.append(str(rgba_str))

        return {
            'period_list': period_list,
            'received_payment': received_payment,
            'target_amount': target_amount,
            'background_color1': background_color1,
            'border_color1': border_color1,
            'background_color2': background_color2,
            'border_color2': border_color2,
        }

    def get_display_data(self, user_id):
        user_id = self.env['res.users'].search([('id', '=', int(user_id))])
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

        classifier_order_cio_obj_list = []
        classifier_order_scheduling_obj_list = []
        classifier_order_waiting_for_approval_obj_list = []
        classifier_order_ro_obj_list = []
        invoice_obj_list = []
        deposits_obj_list = []
        target_obj_list = []
        commission_obj_list = []
        incentive_obj_list = []
        if classifier_super_admin:
            classifier_super_admin.append(user_id.partner_id.id)
            classifier_order_cio_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_super_admin),
                                                                ('classified_bool_field', '=', True),
                                                                ('classified_state', '=', 'draft')])
            for cio in classifier_order_cio_obj:
                classifier_order_cio_obj_list.append(cio.id)
            classifier_order_scheduling_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_super_admin), ('classified_bool_field', '=', True), ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_super_admin), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_super_admin), ('classified_bool_field', '=', True), ('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', 'in', classifier_super_admin), ('classified_bool_field_account', '=', True), ('state', '=', 'posted')])
            for invoice in invoice_obj:
                invoice_obj_list.append(invoice.id)
            deposits_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', classifier_super_admin), ('classifier', '=', True), ('status', '=', 'running')])
            for deposits in deposits_obj:
                deposits_obj_list.append(deposits.id)
            target_obj = self.env['sales.person.target'].search(
                [('partner_id', 'in', classifier_super_admin), ('is_classifieds_target', '=', True)])
            for target in target_obj:
                target_obj_list.append(target.id)
            commission_obj = self.env['commission.settlement'].search([
                ('agent_id', 'in', classifier_super_admin),
                ('state', '=', 'settled')])
            for commission in commission_obj:
                commission_obj_list.append(commission.id)
            incentive_obj = self.env['partner.incentive.line'].search([('partner_id', 'in', classifier_super_admin)])
            for incentive in incentive_obj:
                incentive_obj_list.append(incentive.id)
        elif classifier_head:
            classifier_head.append(user_id.partner_id.id)
            classifier_order_cio_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_head),
                                                                ('classified_bool_field', '=', True),
                                                                ('classified_state', '=', 'draft')])
            for cio in classifier_order_cio_obj:
                classifier_order_cio_obj_list.append(cio.id)
            classifier_order_scheduling_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_head), ('classified_bool_field', '=', True), ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_head), ('classified_bool_field', '=', True), ('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', 'in', classifier_head), ('classified_bool_field_account', '=', True), ('state', '=', 'posted')])
            for invoice in invoice_obj:
                invoice_obj_list.append(invoice.id)
            deposits_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', classifier_head), ('classifier', '=', True), ('status', '=', 'running')])
            for deposits in deposits_obj:
                deposits_obj_list.append(deposits.id)
            target_obj = self.env['sales.person.target'].search(
                [('partner_id', 'in', classifier_head), ('is_classifieds_target', '=', True)])
            for target in target_obj:
                target_obj_list.append(target.id)
            commission_obj = self.env['commission.settlement'].search([
                ('agent_id', 'in', classifier_head),
                ('state', '=', 'settled')])
            for commission in commission_obj:
                commission_obj_list.append(commission.id)
            incentive_obj = self.env['partner.incentive.line'].search([('partner_id', 'in', classifier_head)])
            for incentive in incentive_obj:
                incentive_obj_list.append(incentive.id)
        elif reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            classifier_order_cio_obj = self.env['sale.order'].search([('agent_name', 'in', reg_in_head),
                                                                      ('classified_bool_field', '=', True),
                                                                      ('classified_state', '=', 'draft')])
            for cio in classifier_order_cio_obj:
                classifier_order_cio_obj_list.append(cio.id)
            classifier_order_scheduling_obj = self.env['sale.order'].search(
                [('agent_name', 'in', reg_in_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', reg_in_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', 'in', reg_in_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', 'in', reg_in_head), ('classified_bool_field_account', '=', True),
                 ('state', '=', 'posted')])
            for invoice in invoice_obj:
                invoice_obj_list.append(invoice.id)
            deposits_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', reg_in_head), ('classifier', '=', True), ('status', '=', 'running')])
            for deposits in deposits_obj:
                deposits_obj_list.append(deposits.id)
            target_obj = self.env['sales.person.target'].search(
                [('partner_id', 'in', reg_in_head), ('is_classifieds_target', '=', True)])
            for target in target_obj:
                target_obj_list.append(target.id)
            commission_obj = self.env['commission.settlement'].search([
                ('agent_id', 'in', reg_in_head),
                ('state', '=', 'settled')])
            for commission in commission_obj:
                commission_obj_list.append(commission.id)
            incentive_obj = self.env['partner.incentive.line'].search([('partner_id', 'in', reg_in_head)])
            for incentive in incentive_obj:
                incentive_obj_list.append(incentive.id)
        elif unit_manager:
            unit_manager.append(user_id.partner_id.id)
            classifier_order_cio_obj = self.env['sale.order'].search([('agent_name', 'in', unit_manager),
                                                                      ('classified_bool_field', '=', True),
                                                                      ('classified_state', '=', 'draft')])
            for cio in classifier_order_cio_obj:
                classifier_order_cio_obj_list.append(cio.id)
            classifier_order_scheduling_obj = self.env['sale.order'].search(
                [('agent_name', 'in', unit_manager), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', unit_manager), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', 'in', unit_manager), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', 'in', unit_manager), ('classified_bool_field_account', '=', True),
                 ('state', '=', 'posted')])
            for invoice in invoice_obj:
                invoice_obj_list.append(invoice.id)
            deposits_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', unit_manager), ('classifier', '=', True), ('status', '=', 'running')])
            for deposits in deposits_obj:
                deposits_obj_list.append(deposits.id)
            target_obj = self.env['sales.person.target'].search(
                [('partner_id', 'in', unit_manager), ('is_classifieds_target', '=', True)])
            for target in target_obj:
                target_obj_list.append(target.id)
            commission_obj = self.env['commission.settlement'].search([
                ('agent_id', 'in', unit_manager),
                ('state', '=', 'settled')])
            for commission in commission_obj:
                commission_obj_list.append(commission.id)
            incentive_obj = self.env['partner.incentive.line'].search([('partner_id', 'in', unit_manager)])
            for incentive in incentive_obj:
                incentive_obj_list.append(incentive.id)
        elif classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            classifier_order_cio_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge_head),
                                                                      ('classified_bool_field', '=', True),
                                                                      ('classified_state', '=', 'draft')])
            for cio in classifier_order_cio_obj:
                classifier_order_cio_obj_list.append(cio.id)
            classifier_order_scheduling_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_incharge_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_incharge_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_incharge_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', 'in', classifier_incharge_head), ('classified_bool_field_account', '=', True),
                 ('state', '=', 'posted')])
            for invoice in invoice_obj:
                invoice_obj_list.append(invoice.id)
            deposits_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', classifier_incharge_head), ('classifier', '=', True), ('status', '=', 'running')])
            for deposits in deposits_obj:
                deposits_obj_list.append(deposits.id)
            target_obj = self.env['sales.person.target'].search(
                [('partner_id', 'in', classifier_incharge_head), ('is_classifieds_target', '=', True)])
            for target in target_obj:
                target_obj_list.append(target.id)
            commission_obj = self.env['commission.settlement'].search([
                ('agent_id', 'in', classifier_incharge_head),
                ('state', '=', 'settled')])
            for commission in commission_obj:
                commission_obj_list.append(commission.id)
            incentive_obj = self.env['partner.incentive.line'].search([('partner_id', 'in', classifier_incharge_head)])
            for incentive in incentive_obj:
                incentive_obj_list.append(incentive.id)
        elif classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            classifier_order_cio_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge),
                                                                      ('classified_bool_field', '=', True),
                                                                      ('classified_state', '=', 'draft')])
            for cio in classifier_order_cio_obj:
                classifier_order_cio_obj_list.append(cio.id)
            classifier_order_scheduling_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_incharge), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_incharge), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_incharge), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', 'in', classifier_incharge), ('classified_bool_field_account', '=', True),
                 ('state', '=', 'posted')])
            for invoice in invoice_obj:
                invoice_obj_list.append(invoice.id)
            deposits_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', classifier_incharge), ('classifier', '=', True), ('status', '=', 'running')])
            for deposits in deposits_obj:
                deposits_obj_list.append(deposits.id)
            target_obj = self.env['sales.person.target'].search(
                [('partner_id', 'in', classifier_incharge), ('is_classifieds_target', '=', True)])
            for target in target_obj:
                target_obj_list.append(target.id)
            commission_obj = self.env['commission.settlement'].search([
                ('agent_id', 'in', classifier_incharge),
                ('state', '=', 'settled')])
            for commission in commission_obj:
                commission_obj_list.append(commission.id)
            incentive_obj = self.env['partner.incentive.line'].search([('partner_id', 'in', classifier_incharge)])
            for incentive in incentive_obj:
                incentive_obj_list.append(incentive.id)
        else:
            classifier_incharge.append(user_id.partner_id.id)
            classifier_order_cio_obj = self.env['sale.order'].search([('agent_name', '=', user_id.partner_id.id),
                                                                      ('classified_bool_field', '=', True),
                                                                      ('classified_state', '=', 'draft')])
            for cio in classifier_order_cio_obj:
                classifier_order_cio_obj_list.append(cio.id)
            classifier_order_scheduling_obj = self.env['sale.order'].search(
                [('agent_name', '=', user_id.partner_id.id), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', '=', user_id.partner_id.id), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', '=', user_id.partner_id.id), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', '=', user_id.partner_id.id), ('classified_bool_field_account', '=', True),
                 ('state', '=', 'posted')])
            for invoice in invoice_obj:
                invoice_obj_list.append(invoice.id)
            deposits_obj = self.env['account.deposit'].search(
                [('partner_id', '=', user_id.partner_id.id), ('classifier', '=', True), ('status', '=', 'running')])
            for deposits in deposits_obj:
                deposits_obj_list.append(deposits.id)
            target_obj = self.env['sales.person.target'].search(
                [('partner_id', '=', user_id.partner_id.id), ('is_classifieds_target', '=', True)])
            for target in target_obj:
                target_obj_list.append(target.id)
            commission_obj = self.env['commission.settlement'].search([
                ('agent_id', '=', user_id.partner_id.id),
                ('state', '=', 'settled')])
            for commission in commission_obj:
                commission_obj_list.append(commission.id)
            incentive_obj = self.env['partner.incentive.line'].search([('partner_id', '=', user_id.partner_id.id)])
            for incentive in incentive_obj:
                incentive_obj_list.append(incentive.id)

        deposit_amt = 0.00
        outstanding_amt = 0.00
        for deposits in deposits_obj_list:
            deposits = self.env['account.deposit'].browse(deposits)
            deposit_amt += deposits.deposit_amt
            outstanding_amt += deposits.total_outstanding

        invoice_amount = 0.00
        invoice_due = 0.00
        for invoice in invoice_obj_list:
            invoices = self.env['account.move'].browse(invoice)
            invoice_amount += invoices.amount_total
            invoice_due += invoices.amount_residual

        target_lines = []
        so_target_lines = []
        for target in target_obj_list:
            target = self.env['sales.person.target'].browse(target)
            for target_line in target.product_target_line_ids:
                if target_line.product_id.product_template_attribute_value_ids:
                    product_name = str(target_line.product_id.name) + ' (' + str(
                        target_line.product_id.product_template_attribute_value_ids.name) + ')'
                else:
                    product_name = str(target_line.product_id.name)
                target_lines.append({
                    'product_id': product_name,
                    'target_amount': target_line.target_amount,
                    'achieved_amount': target_line.achieved_amount,
                    'to_be_achieved': target_line.to_be_achieved
                })
            for so_target_line in target.so_targer_line_ids:
                so_target_lines.append({
                    'target_amount': so_target_line.target_amount,
                    'so_total_amount': so_target_line.so_total_amount,
                    'achieved_amount': so_target_line.achieved_amount,
                    'to_be_achieved': so_target_line.to_be_achieved
                })

        total_payment_received = 0.00
        total_commission_received = 0.00
        for commission in commission_obj_list:
            commission = self.env['commission.settlement'].browse(commission)
            for line in commission.reta_order:
                total_payment_received += line.amount_paid
                total_commission_received += line.commission
        incentive_lines = []
        total_incentive_payment_received = 0.00
        total_incentive_amount = 0.00
        for incentive in incentive_obj_list:
            incentive = self.env['partner.incentive.line'].browse(incentive)
            total_incentive_payment_received += incentive.recieved_payment
            total_incentive_amount += incentive.incentive_amt
            if incentive.incentive.from_date:
                current_month = incentive.incentive.from_date.month
                month_name = calendar.month_name[current_month]
                current_year = incentive.incentive.from_date.year
            else:
                current_month = current_year = month_name = ''

            incentive_lines.append({
                'employee_name': incentive.employee_id.name,
                'target_period': str(month_name) + ' ' + str(current_year),
                # 'target_period':str(incentive.incentive.from_date)+' - '+str(incentive.incentive.to_date),
                'target_amt': incentive.target_amt,
                'so_total_amt': incentive.so_total_amt,
                'recieved_payment': incentive.recieved_payment,
                'progress': incentive.progress
            })

        dashboard_display_vals = {
            'user': user_id.name,
            'cio': len(classifier_order_cio_obj_list),
            'scheduling': len(classifier_order_scheduling_obj_list),
            'waiting_for_approval': len(classifier_order_waiting_for_approval_obj_list),
            'release_orders': len(classifier_order_ro_obj_list),
            'invoices': len(invoice_obj_list),
            'invoice_amount': round(invoice_amount, 2),
            'invoice_due': round(invoice_due, 2),
            'deposit_amt': round(deposit_amt, 2),
            'outstanding_amt': round(outstanding_amt, 2),
            'total_payment_received': round(total_payment_received, 2),
            'total_commission_received': round(total_commission_received, 2),
            'total_incentive_payment_received': round(total_incentive_payment_received, 2),
            'total_incentive_amount': round(total_incentive_amount, 2),
            'target_lines': target_lines,
            'so_target_lines': so_target_lines,
            'incentive_lines': incentive_lines
        }

        return dashboard_display_vals


class ClassifierDashBoardRedirect(models.Model):
    _inherit = 'sale.order'

    def classifier_dashboard_cio(self):
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
                'name': _('CIO'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_super_admin),
                           ('classified_state', '=', 'draft')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        if classifier_head:
            classifier_head.append(user_id.partner_id.id)
            return {
                'name': _('CIO'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_head),
                           ('classified_state', '=', 'draft')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            return {
                'name': _('CIO'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', reg_in_head),
                           ('classified_state', '=', 'draft')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.partner_id.id)
            return {
                'name': _('CIO'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', unit_manager),
                           ('classified_state', '=', 'draft')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        if classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            return {
                'name': _('CIO'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_incharge_head),
                           ('classified_state', '=', 'draft')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        if classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Classified CIO'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_incharge),
                           ('classified_state', '=', 'draft')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        else:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Classified CIO'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', '=', user_id.partner_id.id),
                           ('classified_state', '=', 'draft')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }

    def classifier_dashboard_scheduling(self):
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
                'name': _('Scheduling'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_super_admin),
                           ('classified_state', '=', 'sent')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        if classifier_head:
            classifier_head.append(user_id.partner_id.id)
            return {
                'name': _('Scheduling'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_head),
                           ('classified_state', '=', 'sent')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            return {
                'name': _('Scheduling'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', reg_in_head),
                           ('classified_state', '=', 'sent')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.partner_id.id)
            return {
                'name': _('Scheduling'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', unit_manager),
                           ('classified_state', '=', 'sent')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        if classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            return {
                'name': _('Scheduling'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_incharge_head),
                           ('classified_state', '=', 'sent')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }

        if classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Scheduling'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_incharge),
                           ('classified_state', '=', 'sent')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        else:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Scheduling'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', '=', user_id.partner_id.id),
                           ('classified_state', '=', 'sent')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }

    def classifier_dashboard_waiting_for_approval(self):
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
                'name': _('Waiting For Approval'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_super_admin),
                           ('classified_state', '=', 'waiting_for_approval')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        if classifier_head:
            classifier_head.append(user_id.partner_id.id)
            return {
                'name': _('Waiting For Approval'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_head),
                           ('classified_state', '=', 'waiting_for_approval')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            return {
                'name': _('Waiting For Approval'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', reg_in_head),
                           ('classified_state', '=', 'waiting_for_approval')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.partner_id.id)
            return {
                'name': _('Waiting For Approval'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', unit_manager),
                           ('classified_state', '=', 'waiting_for_approval')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        if classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            return {
                'name': _('Classified Waiting For Approval'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_incharge_head),
                           ('classified_state', '=', 'waiting_for_approval')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }

        if classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Waiting For Approval'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_incharge),
                           ('classified_state', '=', 'waiting_for_approval')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }
        else:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Waiting For Approval'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', '=', user_id.partner_id.id),
                           ('classified_state', '=', 'waiting_for_approval')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

            }

    def classifier_dashboard_release_orders(self):
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
                'name': _('Release Orders'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_super_admin),
                           ('classified_state', '=', 'sale')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        if classifier_head:
            classifier_head.append(user_id.partner_id.id)
            return {
                'name': _('Release Orders'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_head),
                           ('classified_state', '=', 'sale')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            return {
                'name': _('Release Orders'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', reg_in_head),
                           ('classified_state', '=', 'sale')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.partner_id.id)
            return {
                'name': _('Release Orders'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', unit_manager),
                           ('classified_state', '=', 'sale')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        if classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            return {
                'name': _('Release Orders'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_incharge_head),
                           ('classified_state', '=', 'sale')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }

        if classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Release Orders'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', 'in', classifier_incharge),
                           ('classified_state', '=', 'sale')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }
        else:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Release Orders'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'sale.order',
                'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
                'domain': [('classified_bool_field', '=', True), ('agent_name', '=', user_id.partner_id.id),
                           ('classified_state', '=', 'sale')],
                'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                          (self.env.ref('sale.view_order_tree').id or False, 'tree')],

            }


class ClassifierDashBoardAccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def classifier_dashboard_invoices(self):
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
                'name': _('Invoices'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'move_type': 'out_invoice',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('agent_name', 'in', classifier_super_admin), ('state', '=', 'posted'),
                           ('classified_bool_field_account', '=', True)],
                'views': [(self.env.ref('account.view_move_form').id or False, 'form'),
                          (self.env.ref('account.view_invoice_tree').id or False, 'tree')],

            }
        if classifier_head:
            classifier_head.append(user_id.partner_id.id)
            return {
                'name': _('Invoices'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'move_type': 'out_invoice',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('agent_name', 'in', classifier_head), ('state', '=', 'posted'),
                           ('classified_bool_field_account', '=', True)],
                'views': [(self.env.ref('account.view_move_form').id or False, 'form'),
                          (self.env.ref('account.view_invoice_tree').id or False, 'tree')],

            }
        if reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            return {
                'name': _('Invoices'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'move_type': 'out_invoice',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('agent_name', 'in', reg_in_head), ('state', '=', 'posted'),
                           ('classified_bool_field_account', '=', True)],
                'views': [(self.env.ref('account.view_move_form').id or False, 'form'),
                          (self.env.ref('account.view_invoice_tree').id or False, 'tree')],

            }
        if unit_manager:
            unit_manager.append(user_id.partner_id.id)
            return {
                'name': _('Invoices'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'move_type': 'out_invoice',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('agent_name', 'in', unit_manager), ('state', '=', 'posted'),
                           ('classified_bool_field_account', '=', True)],
                'views': [(self.env.ref('account.view_move_form').id or False, 'form'),
                          (self.env.ref('account.view_invoice_tree').id or False, 'tree')],

            }
        if classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            return {
                'name': _('Invoices'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'move_type': 'out_invoice',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('agent_name', 'in', classifier_incharge_head), ('state', '=', 'posted'),
                           ('classified_bool_field_account', '=', True)],
                'views': [(self.env.ref('account.view_move_form').id or False, 'form'),
                          (self.env.ref('account.view_invoice_tree').id or False, 'tree')],

            }

        if classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Invoices'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'move_type': 'out_invoice',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('agent_name', 'in', classifier_incharge), ('state', '=', 'posted'),
                           ('classified_bool_field_account', '=', True)],
                'views': [(self.env.ref('account.view_move_form').id or False, 'form'),
                          (self.env.ref('account.view_invoice_tree').id or False, 'tree')],

            }
        else:
            classifier_incharge.append(user_id.partner_id.id)
            return {
                'name': _('Invoices'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'account.move',
                'move_type': 'out_invoice',
                'context': {'readonly_by_pass': True, 'check_domain': True},
                'domain': [('agent_name', '=', user_id.partner_id.id), ('state', '=', 'posted'),
                           ('classified_bool_field_account', '=', True)],
                'views': [(self.env.ref('account.view_move_form').id or False, 'form'),
                          (self.env.ref('account.view_invoice_tree').id or False, 'tree')],

            }