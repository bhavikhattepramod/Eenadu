from odoo.http import request, root
from odoo.service import security
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
import calendar

def _rotate_session(httprequest):
    if httprequest.session.rotate:
        root.session_store.delete(httprequest.session)
        httprequest.session.sid = root.session_store.generate_key()
        if httprequest.session.uid:
            httprequest.session.session_token = security.compute_session_token(
                httprequest.session, request.env
            )
        httprequest.session.modified = True

class PartnerNewApiService(Component):
    _inherit = "base.rest.service"
    _name = "partner.new_api.service.classified"
    _usage = "classified"
    _collection = "base_rest_auth_user_service.services"
    _description = """ """

    @restapi.method([(["/dashboard_details"], "GET")], auth="public")
    def dashboard_details(self):
        user = self.env.user
        user_id = self.env['res.users'].search([('id', '=', int(user))])
        classifier_incharge = [agent.id for agent in self.env['res.partner'].search([
            ('hr_employee_id.user_id', '=', user_id.id)])]

        reg_incharge_list = []
        for agent in self.env['res.partner'].search([('id', '=', user_id.partner_id.id)]):
            for incharge in self.env['hr.employee'].search([('id', '=', agent.hr_employee_id.id)]):
                for reta_incharge_obj in self.env['hr.employee'].search([('id', '=', incharge.parent_id.id)]):
                    for unit_incharge in self.env['hr.employee'].search([('id', '=', reta_incharge_obj.parent_id.id)]):
                        for reg_incharge in self.env['hr.employee'].search([('id', '=', unit_incharge.parent_id.id)]):
                            reg_incharge_list.append({
                                'id': reg_incharge.id if reg_incharge.id else 0,
                                'name': reg_incharge.name if reg_incharge.name else '',
                                'job_position': reg_incharge.job_id.name if reg_incharge.job_id.name else '',
                                'mobile': reg_incharge.mobile_phone if reg_incharge.mobile_phone else '',
                                'work_phone': reg_incharge.work_phone if reg_incharge.work_phone else '',
                            })

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
                [('agent_name', 'in', classifier_super_admin), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_super_admin), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_super_admin), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', 'in', classifier_super_admin), ('classified_bool_field_account', '=', True),
                 ('state', '=', 'posted')])
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
            commission_obj = self.env['commission.settlement'].search([('agent_id', 'in', classifier_super_admin),
                                                                       ('state', '=', 'settled')
                                                                       ])
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
                [('agent_name', 'in', classifier_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', 'in', classifier_head), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', 'in', classifier_head), ('classified_bool_field_account', '=', True),
                 ('state', '=', 'posted')])
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
            commission_obj = self.env['commission.settlement'].search([('agent_id', 'in', classifier_head),
                                                                       ('state', '=', 'settled')])
            for commission in commission_obj:
                commission_obj_list.append(commission.id)
            incentive_obj = self.env['partner.incentive.line'].search([('partner_id', 'in', classifier_head)])
            for incentive in incentive_obj:
                incentive_obj_list.append(incentive.id)
        elif reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            classifier_order_cio_obj = self.env['sale.order'].search([('agent_name', 'in', reg_in_head),('classified_bool_field', '=', True),('classified_state', '=', 'draft')])
            for cio in classifier_order_cio_obj:
                classifier_order_cio_obj_list.append(cio.id)
            classifier_order_scheduling_obj = self.env['sale.order'].search(
                [('agent_name', 'in', reg_in_head), ('classified_bool_field', '=', True),('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', reg_in_head), ('classified_bool_field', '=', True),('reta_state', '=', 'waiting_for_approval')])
            for waiting_for_approval in classifier_order_waiting_for_approval_obj:
                classifier_order_waiting_for_approval_obj_list.append(waiting_for_approval.id)
            classifier_order_ro_obj = self.env['sale.order'].search(
                [('agent_name', 'in', reg_in_head), ('classified_bool_field', '=', True),('classified_state', '=', 'sale')])
            for ro in classifier_order_ro_obj:
                classifier_order_ro_obj_list.append(ro.id)
            invoice_obj = self.env['account.move'].search(
                [('agent_name', 'in', reg_in_head), ('classified_bool_field_account', '=', True),('state', '=', 'posted')])
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
            commission_obj = self.env['commission.settlement'].search([('agent_id', 'in', reg_in_head),('state', '=', 'settled')])
            for commission in commission_obj:
                commission_obj_list.append(commission.id)
            incentive_obj = self.env['partner.incentive.line'].search([('partner_id', 'in', reg_in_head)])
            for incentive in incentive_obj:
                incentive_obj_list.append(incentive.id)
        elif unit_manager:
            unit_manager.append(user_id.partner_id.id)
            classifier_order_cio_obj = self.env['sale.order'].search([('agent_name', 'in', unit_manager),('classified_bool_field', '=', True),('classified_state', '=', 'draft')])
            for cio in classifier_order_cio_obj:
                classifier_order_cio_obj_list.append(cio.id)
            classifier_order_scheduling_obj = self.env['sale.order'].search(
                [('agent_name', 'in', unit_manager), ('classified_bool_field', '=', True),
                 ('classified_state', '=', 'sent')])
            for scheduling in classifier_order_scheduling_obj:
                classifier_order_scheduling_obj_list.append(scheduling.id)
            classifier_order_waiting_for_approval_obj = self.env['sale.order'].search(
                [('agent_name', 'in', unit_manager), ('classified_bool_field', '=', True),
                 ('reta_state', '=', 'waiting_for_approval')])
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
            commission_obj = self.env['commission.settlement'].search([('agent_id', 'in', unit_manager),('state', '=', 'settled')])
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
                 ('reta_state', '=', 'waiting_for_approval')])
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
            commission_obj = self.env['commission.settlement'].search([('agent_id', 'in', classifier_incharge_head),
                                                                       ('state', '=', 'settled')
                                                                       ])
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
                 ('reta_state', '=', 'waiting_for_approval')])
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
            commission_obj = self.env['commission.settlement'].search([('agent_id', 'in', classifier_incharge),('state', '=', 'settled')])
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
                 ('reta_state', '=', 'waiting_for_approval')])
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
            commission_obj = self.env['commission.settlement'].search([('agent_id', '=', user_id.partner_id.id),
                                                                       ('state', '=', 'settled')
                                                                       ])
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

        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)], limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])
        target_obj = self.env['partner.incentive.line'].sudo().search(
            [('employee_id', '=', employee_obj.id)])

        commission_obj = self.env['commission.settlement'].sudo().search([
            ('agent_id', '=', user_id.partner_id.id),
            ('state', '=', 'settled')])

        reta_cio_name = str(user_id.partner_id.name) + '.CIO'
        reta_ro_name = str(user_id.partner_id.name) + '.RO'
        customer_seq_name = str(user_id.partner_id.agent_code) + '.agent_code'

        reta_cio_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', reta_cio_name)], limit=1)
        reta_ro_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', reta_ro_name)], limit=1)
        customer_sequence_obj = self.env['ir.sequence'].search([('code', '=', customer_seq_name)], limit=1)

        reta_default_cio_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', 'reta.quotation.sequence')])
        reta_default_ro_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', 'reta.sale.sequence')])
        default_customer_sequence_obj = self.env['ir.sequence'].search([('code', '=', 'customer.sequence.code')])

        if reta_cio_next_sequence_obj:
            reta_cio_next_sequence_number = str(user_id.partner_id.agent_code) + '/CIOM/' + str(
                f"{reta_cio_next_sequence_obj.number_next_actual:05}")
        else:
            reta_cio_next_sequence_number = 'CIOM/' + str(f"{reta_default_cio_next_sequence_obj.number_next_actual:05}")

        if reta_ro_next_sequence_obj:
            reta_ro_next_sequence_number = str(user_id.partner_id.agent_code) + '/ROM/' + str(
                f"{reta_ro_next_sequence_obj.number_next_actual:05}")
        else:
            reta_ro_next_sequence_number = 'ROM/' + str(f"{reta_default_ro_next_sequence_obj.number_next_actual:05}")

        if customer_sequence_obj:
            customer_next_seq_number = str(user_id.partner_id.agent_code) + '/CUST/' + str(
                f"{customer_sequence_obj.number_next_actual:05}")
        else:
            customer_next_seq_number = 'CUST/' + str(f"{default_customer_sequence_obj.number_next_actual:05}")

        classifieds_cio_name = str(user_id.partner_id.name) + ' Classifieds.CIO'
        classifieds_ro_name = str(user_id.partner_id.name) + ' Classifieds.RO'

        classifieds_cio_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', classifieds_cio_name)],
                                                                           limit=1)
        classifieds_ro_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', classifieds_ro_name)], limit=1)

        classifieds_default_cio_next_sequence_obj = self.env['ir.sequence'].search(
            [('code', '=', 'reta.quotation.sequence')])
        classifieds_default_ro_next_sequence_obj = self.env['ir.sequence'].search([('code', '=', 'reta.sale.sequence')])

        if classifieds_cio_next_sequence_obj:
            classifieds_cio_next_sequence_number = str(user_id.partner_id.agent_code) + '/CIOM/' + str(
                f"{classifieds_cio_next_sequence_obj.number_next_actual:05}")
        else:
            classifieds_cio_next_sequence_number = 'CIOM/' + str(
                f"{classifieds_default_cio_next_sequence_obj.number_next_actual:05}")

        if classifieds_ro_next_sequence_obj:
            classifieds_ro_next_sequence_number = str(user_id.partner_id.agent_code) + '/ROM/' + str(
                f"{classifieds_ro_next_sequence_obj.number_next_actual:05}")
        else:
            classifieds_ro_next_sequence_number = 'ROM/' + str(
                f"{classifieds_default_ro_next_sequence_obj.number_next_actual:05}")

        deposit_amt = 0.00
        outstanding_amt = 0.00
        for deposits in deposits_obj:
            deposit_amt += deposits.deposit_amt
            outstanding_amt += deposits.total_outstanding

        target_lines = []

        for target in target_obj:
            if target.incentive.from_date:
                current_month = target.incentive.from_date.month
                month_name = calendar.month_name[current_month]
                current_year = target.incentive.from_date.year
            else:
                current_month = current_year = month_name = ''
            target_lines.append({
                'employee_name': target.employee_id.name,
                'period': str(month_name) + ' ' + str(current_year),
                'target_amount': target.target_amt,
                'ro_total_amount': target.so_total_amt,
                'recieved_payment': target.recieved_payment,
                'progress': str(target.progress) + ' %',
            })

        total_payment_received = 0.00
        total_commission_received = 0.00
        for commission in commission_obj:
            for line in commission.reta_order:
                total_payment_received += line.amount_paid
                total_commission_received += line.commission

        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id,
                'name': child_emp.name
            })

        if user_id.partner_id.mobile:
            mobile = user_id.partner_id.mobile.replace('+91', '').replace(' ', '')
        else:
            mobile = ''

        dashboard_display_vals = {
            'cio': len(classifier_order_cio_obj_list),
            'user_role': employee_obj.job_id.name if employee_obj.job_id.name else '',
            'scheduling': len(classifier_order_scheduling_obj_list),
            'waiting_for_approval': len(classifier_order_waiting_for_approval_obj_list),
            'release_orders': len(classifier_order_ro_obj_list),
            'invoices': len(invoice_obj),
            'deposit_amt': round(deposit_amt, 2),
            'outstanding_amt': round(outstanding_amt, 2),
            'total_payment_received': round(total_payment_received, 2),
            'total_commission_received': round(total_commission_received, 2),
            'target_lines': [{
                'id': user.id if user.id else 0,
                'name': user.name if user.name else '',
                'target': target_lines
            }],
            'user_list_role': user_list_role,
            'user_list': user_list,
            'reta_cio_next_sequence_number': reta_cio_next_sequence_number,
            'reta_ro_next_sequence_number': reta_ro_next_sequence_number,
            'classifieds_cio_next_sequence_number': classifieds_cio_next_sequence_number,
            'classifieds_ro_next_sequence_number': classifieds_ro_next_sequence_number,
            'customer_next_seq_number': customer_next_seq_number,
            'mobile_number': mobile,
            'reg_incharge_details': reg_incharge_list
        }

        return dashboard_display_vals

    @restapi.method([(["/dashboard_cio"], "GET")], auth="public")
    def dashboard_cio(self):
        user = self.env.user
        user_id = self.env['res.users'].search([('id', '=', int(user))])
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
        classified_agent = []
        if classifier_super_admin:
            classifier_super_admin.append(user_id.partner_id.id)
            cio_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_super_admin),
                                                     ('classified_bool_field', '=', True),
                                                     ('classified_state', '=', 'draft')])
        elif classifier_head:
            classifier_head.append(user_id.partner_id.id)
            cio_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_head),
                                                     ('classified_bool_field', '=', True),
                                                     ('classified_state', '=', 'draft')])
        elif reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            cio_obj = self.env['sale.order'].search([('agent_name', 'in', reg_in_head),
                                                     ('classified_bool_field', '=', True),
                                                     ('classified_state', '=', 'draft')])
        elif unit_manager:
            unit_manager.append(user_id.partner_id.id)
            cio_obj = self.env['sale.order'].search([('agent_name', 'in', unit_manager),
                                                     ('classified_bool_field', '=', True),
                                                     ('classified_state', '=', 'draft')])
        elif classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            cio_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge_head),
                                                     ('classified_bool_field', '=', True),
                                                     ('classified_state', '=', 'draft')])
        elif classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            cio_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge),
                                                     ('classified_bool_field', '=', True),
                                                     ('classified_state', '=', 'draft')])
        else:
            classified_agent.append(user_id.partner_id.id)
            cio_obj = self.env['sale.order'].search([('agent_name', '=', user_id.partner_id.id),
                                                     ('classified_bool_field', '=', True),
                                                     ('classified_state', '=', 'draft')])
        cio_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])

        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name
            })

        for sale in cio_obj:
            invoice_status = ''
            if sale.classified_state == 'draft':
                invoice_status = "CIO"
            elif sale.classified_state == 'sent':
                invoice_status = "Scheduling"
            elif sale.classified_state == 'waiting_for_approval':
                invoice_status = "Waiting for Approval"
            elif sale.classified_state == 'sale':
                invoice_status = "Release Order"
            elif sale.classified_state == 'print':
                invoice_status = "Published"
            elif sale.classified_state == 'cancel':
                invoice_status = "Rejected"
            cio_det.append({
                'id': sale.id if sale.id else 0,
                'number': sale.name if sale.name else '',
                'cio_reference': sale.custom_seq if sale.custom_seq else 0,
                'ro_sequence': sale.custom_sale_seq if sale.custom_sale_seq else 0,
                'order_date': sale.date_order if sale.date_order else '',
                'customer': sale.partner_id.name if sale.partner_id else '',
                'sales_person': sale.user_id.name if sale.user_id.name else '',
                'total': sale.amount_total if sale.amount_total else 0.0,
                'invoice_status': invoice_status,
                'is_online': sale.is_online
            })
        cio_details = [{
            'dashboard_details': cio_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }]
        return cio_details

    @restapi.method([(["/dashboard_scheduling"], "GET")], auth="public")
    def dashboard_scheduling(self):
        user = self.env.user
        user_id = self.env['res.users'].search([('id', '=', int(user))])
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

        classified_agent = []
        if classifier_super_admin:
            classifier_super_admin.append(user_id.partner_id.id)
            sched_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_super_admin),
                                                       ('classified_bool_field', '=', True),
                                                       ('classified_state', '=', 'sent')])
        elif classifier_head:
            classifier_head.append(user_id.partner_id.id)
            sched_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_head),
                                                       ('classified_bool_field', '=', True),
                                                       ('classified_state', '=', 'sent')])
        elif reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            sched_obj = self.env['sale.order'].search([('agent_name', 'in', reg_in_head),
                                                       ('classified_bool_field', '=', True),
                                                       ('classified_state', '=', 'sent')])
        elif unit_manager:
            unit_manager.append(user_id.partner_id.id)
            sched_obj = self.env['sale.order'].search([('agent_name', 'in', unit_manager),
                                                       ('classified_bool_field', '=', True),
                                                       ('classified_state', '=', 'sent')])
        elif classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            sched_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge_head),
                                                       ('classified_bool_field', '=', True),
                                                       ('classified_state', '=', 'sent')])
        elif classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            sched_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge),
                                                       ('classified_bool_field', '=', True),
                                                       ('classified_state', '=', 'sent')])
        else:
            classified_agent.append(user_id.partner_id.id)
            sched_obj = self.env['sale.order'].search([('agent_name', '=', user_id.partner_id.id),
                                                       ('classified_bool_field', '=', True),
                                                       ('classified_state', '=', 'sent')])
        sched_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])

        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })

        for sale in sched_obj:
            invoice_status = ''
            if sale.classified_state == 'draft':
                invoice_status = "CIO"
            elif sale.classified_state == 'sent':
                invoice_status = "Scheduling"
            elif sale.classified_state == 'waiting_for_approval':
                invoice_status = "Waiting for Approval"
            elif sale.classified_state == 'sale':
                invoice_status = "Release Order"
            elif sale.classified_state == 'print':
                invoice_status = "Published"
            elif sale.classified_state == 'cancel':
                invoice_status = "Rejected"
            sched_det.append({
                'id': sale.id if sale.id else 0,
                'number': sale.name if sale.name else '',
                'cio_reference': sale.custom_seq if sale.custom_seq else 0,
                'ro_sequence': sale.custom_sale_seq if sale.custom_sale_seq else 0,
                'order_date': sale.date_order if sale.date_order else '',
                'customer': sale.partner_id.name if sale.partner_id else '',
                'sales_person': sale.user_id.name if sale.user_id.name else '',
                'total': sale.amount_total if sale.amount_total else 0.0,
                'invoice_status': invoice_status,
                'is_online': sale.is_online
            })
        sched_det = [{
            'dashboard_details': sched_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }]
        return sched_det

    @restapi.method([(["/dashboard_waiting_for_approval"], "GET")], auth="public")
    def dashboard_waiting_for_approval(self):
        user = self.env.user
        user_id = self.env['res.users'].search([('id', '=', int(user))])
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

        classified_agent = []
        if classifier_super_admin:
            classifier_super_admin.append(user_id.partner_id.id)
            waiting_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_super_admin),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'waiting_for_approval')])
        elif classifier_head:
            classifier_head.append(user_id.partner_id.id)
            waiting_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_head),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'waiting_for_approval')])
        elif reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            waiting_obj = self.env['sale.order'].search([('agent_name', 'in', reg_in_head),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'waiting_for_approval')])
        elif unit_manager:
            unit_manager.append(user_id.partner_id.id)
            waiting_obj = self.env['sale.order'].search([('agent_name', 'in', unit_manager),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'waiting_for_approval')])
        elif classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            waiting_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge_head),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'waiting_for_approval')])
        elif classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            waiting_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'waiting_for_approval')])
        else:
            classified_agent.append(user_id.partner_id.id)
            waiting_obj = self.env['sale.order'].search([('agent_name', '=', user_id.partner_id.id),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'waiting_for_approval')])
        approval_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])

        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })

        for sale in waiting_obj:
            invoice_status = ''
            if sale.classified_state == 'draft':
                invoice_status = "CIO"
            elif sale.classified_state == 'sent':
                invoice_status = "Scheduling"
            elif sale.classified_state == 'waiting_for_approval':
                invoice_status = "Waiting for Approval"
            elif sale.classified_state == 'sale':
                invoice_status = "Release Order"
            elif sale.classified_state == 'print':
                invoice_status = "Published"
            elif sale.classified_state == 'cancel':
                invoice_status = "Rejected"
            approval_det.append({
                'id': sale.id if sale.id else 0,
                'number': sale.name if sale.name else '',
                'cio_reference': sale.custom_seq if sale.custom_seq else 0,
                'ro_sequence': sale.custom_sale_seq if sale.custom_sale_seq else 0,
                'order_date': sale.date_order if sale.date_order else '',
                'customer': sale.partner_id.name if sale.partner_id else '',
                'sales_person': sale.user_id.name if sale.user_id.name else '',
                'total': sale.amount_total if sale.amount_total else 0.0,
                'invoice_status': invoice_status,
                'is_online': sale.is_online
            })
        approval_det = [{
            'dashboard_details': approval_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }]
        return approval_det

    @restapi.method([(["/dashboard_release_orders"], "GET")], auth="public")
    def dashboard_release_orders(self):
        user = self.env.user
        user_id = self.env['res.users'].search([('id', '=', int(user))])
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

        classified_agent = []
        if classifier_super_admin:
            classifier_super_admin.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_super_admin),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'sale')])
        elif classifier_head:
            classifier_head.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_head),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'sale')])
        elif reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', reg_in_head),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'sale')])
        elif unit_manager:
            unit_manager.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', unit_manager),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'sale')])
        elif classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge_head),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'sale')])
        elif classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'sale')])
        else:
            classified_agent.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', '=', user_id.partner_id.id),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'sale')])
        release_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])

        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })

        for sale in release_obj:
            invoice_status = ''
            if sale.classified_state == 'draft':
                invoice_status = "CIO"
            elif sale.classified_state == 'sent':
                invoice_status = "Scheduling"
            elif sale.classified_state == 'waiting_for_approval':
                invoice_status = "Waiting for Approval"
            elif sale.classified_state == 'sale':
                invoice_status = "Release Order"
            elif sale.classified_state == 'print':
                invoice_status = "Published"
            elif sale.classified_state == 'cancel':
                invoice_status = "Rejected"
            release_det.append({
                'id': sale.id if sale.id else 0,
                'number': sale.name if sale.name else '',
                'cio_reference': sale.custom_seq if sale.custom_seq else 0,
                'ro_sequence': sale.custom_sale_seq if sale.custom_sale_seq else 0,
                'order_date': sale.date_order if sale.date_order else '',
                'customer': sale.partner_id.name if sale.partner_id else '',
                'sales_person': sale.user_id.name if sale.user_id.name else '',
                'total': sale.amount_total if sale.amount_total else 0.0,
                'invoice_status': invoice_status,
                'is_online': sale.is_online
            })
        release_det = [{
            'dashboard_details': release_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }]

        return release_det

    @restapi.method([(["/dashboard_published"], "GET")], auth="public")
    def dashboard_published(self):
        user = self.env.user
        user_id = self.env['res.users'].search([('id', '=', int(user))])
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

        classified_agent = []
        if classifier_super_admin:
            classifier_super_admin.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_super_admin),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'print')])
        elif classifier_head:
            classifier_head.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_head),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'print')])
        elif reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', reg_in_head),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'print')])
        elif unit_manager:
            unit_manager.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', unit_manager),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'print')])
        elif classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge_head),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'print')])
        elif classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'print')])
        else:
            classified_agent.append(user_id.partner_id.id)
            release_obj = self.env['sale.order'].search([('agent_name', '=', user_id.partner_id.id),
                                                         ('classified_bool_field', '=', True),
                                                         ('classified_state', '=', 'print')])
        release_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])

        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })

        for sale in release_obj:
            invoice_status = ''
            if sale.classified_state == 'draft':
                invoice_status = "CIO"
            elif sale.classified_state == 'sent':
                invoice_status = "Scheduling"
            elif sale.classified_state == 'waiting_for_approval':
                invoice_status = "Waiting for Approval"
            elif sale.classified_state == 'sale':
                invoice_status = "Release Order"
            elif sale.classified_state == 'print':
                invoice_status = "Published"
            elif sale.classified_state == 'cancel':
                invoice_status = "Rejected"
            release_det.append({
                'id': sale.id if sale.id else 0,
                'number': sale.name if sale.name else '',
                'cio_reference': sale.custom_seq if sale.custom_seq else 0,
                'ro_sequence': sale.custom_sale_seq if sale.custom_sale_seq else 0,
                'order_date': sale.date_order if sale.date_order else '',
                'customer': sale.partner_id.name if sale.partner_id else '',
                'sales_person': sale.user_id.name if sale.user_id.name else '',
                'total': sale.amount_total if sale.amount_total else 0.0,
                'invoice_status': invoice_status,
                'is_online': sale.is_online
            })
        release_det = [{
            'dashboard_details': release_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }]

        return release_det

    @restapi.method([(["/dashboard_rejected"], "GET")], auth="public")
    def dashboard_rejected(self):
        user = self.env.user
        user_id = self.env['res.users'].search([('id', '=', int(user))])
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

        classified_agent = []
        if classifier_super_admin:
            classifier_super_admin.append(user_id.partner_id.id)
            rejected_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_super_admin),
                                                          ('classified_bool_field', '=', True),
                                                          ('classified_state', '=', 'cancel')])
        elif classifier_head:
            classifier_head.append(user_id.partner_id.id)
            rejected_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_head),
                                                          ('classified_bool_field', '=', True),
                                                          ('classified_state', '=', 'cancel')])
        elif reg_in_head:
            reg_in_head.append(user_id.partner_id.id)
            rejected_obj = self.env['sale.order'].search([('agent_name', 'in', reg_in_head),
                                                          ('classified_bool_field', '=', True),
                                                          ('classified_state', '=', 'cancel')])
        elif unit_manager:
            unit_manager.append(user_id.partner_id.id)
            rejected_obj = self.env['sale.order'].search([('agent_name', 'in', unit_manager),
                                                          ('classified_bool_field', '=', True),
                                                          ('classified_state', '=', 'cancel')])
        elif classifier_incharge_head:
            classifier_incharge_head.append(user_id.partner_id.id)
            rejected_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge_head),
                                                          ('classified_bool_field', '=', True),
                                                          ('classified_state', '=', 'cancel')])
        elif classifier_incharge:
            classifier_incharge.append(user_id.partner_id.id)
            rejected_obj = self.env['sale.order'].search([('agent_name', 'in', classifier_incharge),
                                                          ('classified_bool_field', '=', True),
                                                          ('classified_state', '=', 'cancel')])
        else:
            classified_agent.append(user_id.partner_id.id)
            rejected_obj = self.env['sale.order'].search([('agent_name', '=', user_id.partner_id.id),
                                                          ('classified_bool_field', '=', True),
                                                          ('classified_state', '=', 'cancel')])
        release_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])

        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })

        for sale in rejected_obj:
            invoice_status = ''
            if sale.classified_state == 'draft':
                invoice_status = "CIO"
            elif sale.classified_state == 'sent':
                invoice_status = "Scheduling"
            elif sale.classified_state == 'waiting_for_approval':
                invoice_status = "Waiting for Approval"
            elif sale.classified_state == 'sale':
                invoice_status = "Release Order"
            elif sale.classified_state == 'print':
                invoice_status = "Published"
            elif sale.classified_state == 'cancel':
                invoice_status = "Rejected"
            release_det.append({
                'id': sale.id if sale.id else 0,
                'number': sale.name if sale.name else '',
                'cio_reference': sale.custom_seq if sale.custom_seq else 0,
                'ro_sequence': sale.custom_sale_seq if sale.custom_sale_seq else 0,
                'order_date': sale.date_order if sale.date_order else '',
                'customer': sale.partner_id.name if sale.partner_id else '',
                'sales_person': sale.user_id.name if sale.user_id.name else '',
                'total': sale.amount_total if sale.amount_total else 0.0,
                'invoice_status': invoice_status,
                'is_online': sale.is_online
            })
        release_det = [{
            'dashboard_details': release_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }]

        return release_det

    @restapi.method([(["/dashboard_employee_incentive"], "GET")], auth="public")
    def dashboard_employee_incentive(self):
        user_id = self.env.user
        incentive_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])
        incentive_obj = self.env['partner.incentive.line'].search([('partner_id', '=', user_id.partner_id.id)])
        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id,
                'name': child_emp.name
            })

        for inc in incentive_obj:
            incentive_det.append({
                'id': inc.id,
                'target_amt': inc.target_amt,
                'so_total_amt': inc.so_total_amt,
                'recieved_payment': inc.recieved_payment,
                'incentive_amt': inc.incentive_amt
            })
        incentive_details = {
            'employee_incentive': incentive_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }

        return incentive_details

    @restapi.method([(["/dashboard_invoices"], "GET")], auth="public")
    def dashboard_invoices(self):
        user_id = self.env.user
        invoice_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])
        invoice_obj = self.env['account.move'].search(
            [('agent_name', '=', user_id.partner_id.id)])
        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })

        for invoice in invoice_obj:
            invoice_status = ''
            payment_state = ''
            if invoice.state == 'draft':
                invoice_status += "Draft"
            elif invoice.state == 'posted':
                invoice_status += "Posted"
            elif invoice.state == 'cancel':
                invoice_status += "Cancelled"

            if invoice.payment_state == 'not_paid':
                payment_state += "Not Paid"
            elif invoice.payment_state == 'in_payment':
                payment_state += "In Payment"
            elif invoice.payment_state == 'partial':
                payment_state += "Partially Paid"
            elif invoice.payment_state == 'paid':
                payment_state += "Paid"
            elif invoice.payment_state == 'reversed':
                payment_state += "Reversed"
            elif invoice.payment_state == 'invoicing_legacy':
                payment_state += "Invoicing App Legacy"

            invoice_det.append({
                'id': invoice.id if invoice.id else 0,
                'number': invoice.name if invoice.name else '',
                'due_date': invoice.invoice_date_due if invoice.invoice_date_due else '',
                'tax_excluded': invoice.amount_untaxed_signed if invoice.amount_untaxed_signed else 0.0,
                'total_amount': invoice.amount_total_signed if invoice.amount_total_signed else 0.0,
                'payment_status': payment_state,
                'status': invoice_status
            })

        invoices_details = {
            'invoice_det': invoice_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }

        return invoices_details

    @restapi.method([(["/dashboard_deposits"], "GET")], auth="public")
    def dashboard_deposits(self):
        user_id = self.env.user
        deposit_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])
        deposits_obj = self.env['account.deposit'].search(
            [('partner_id', '=', user_id.partner_id.id), ('status', '=', 'running')])
        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })

        for deposit in deposits_obj:
            deposit_det.append({
                'id': deposit.id if deposit.id else 0,
                'partner_id': deposit.partner_id.name if deposit.partner_id.name else '',
                'deposit_amt': deposit.deposit_amt if deposit.deposit_amt else 0.0,
                'interest_percent': deposit.interest_percent if deposit.interest_percent else 0.0
            })

        deposit_details = {
            'deposit_det': deposit_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }
        return deposit_details

    @restapi.method([(["/dashboard_commissions"], "GET")], auth="public")
    def dashboard_commissions(self):
        user_id = self.env.user
        commission_det = []
        employee_obj = self.env['hr.employee'].sudo().search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)
        emp_child_obj = self.env['hr.employee'].sudo().search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])
        commission_obj = self.env['commission.settlement'].search([
            ('agent_id', '=', user_id.partner_id.id),
            ('state', '=', 'settled')])
        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if child_emp.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })

        for commission in commission_obj:
            comm_state = ''
            if commission.state == 'settled':
                comm_state += "Settled"
            elif commission.state == 'cancel':
                comm_state += "Cancelled"
            elif commission.state == 'invoiced':
                comm_state += "Invoiced"
            elif commission.state == 'except_invoice':
                comm_state += "Invoice Exception"

            if commission.commission_type == 'fixed_amount':
                comm_type = "Fixed Amount"
            elif commission.commission_type == 'percent':
                comm_type = "Commission Percentage"

            commission_det.append({
                'id': commission.id if commission.id else 0,
                'agent_id': commission.agent_id.name if commission.agent_id.name else '',
                'date_from': commission.date_from if commission.date_from else '',
                'date_to': commission.date_to if commission.date_to else '',
                'total': round(commission.total_commission, 2) if round(commission.total_commission, 2) else 0.00,
                'fixed_amount': commission.fixed_amt if commission.fixed_amt else 0.00,
                'commission_percentage': commission.commission_per if commission.commission_per else 0,
                'commission_type': comm_type if comm_type else '',
                'state': comm_state
            })
        commission_details = {
            'commission_det': commission_det,
            'user_list_role': user_list_role,
            'user_list': user_list,
        }
        return commission_details

    @restapi.method([(["/cio/<int:rec_id>"], "GET")], auth="public")
    def cio(self, rec_id):
        cio_dict = {}
        cio_details_obj = self.env['sale.order'].search(
            [('id', '=', rec_id), ('classified_bool_field', '=', True), ('classified_state', '=', 'draft')])

        if cio_details_obj.partner_id.mobile:
            mobile = cio_details_obj.partner_id.mobile.replace('+91', '').replace(' ', '')
        else:
            mobile = ''

        for cio in cio_details_obj:
            adv_lines_dict = []
            advertisement_language = ''
            if cio.advertisement_language == 'telugu':
                advertisement_language = 'Telugu'
            elif cio.advertisement_language == 'english':
                advertisement_language = 'English'
            elif cio.advertisement_language == 'both':
                advertisement_language == 'Both'

            if cio.scheduling_date == 'specific_date':
                scheduling_date = 'Specific Date'
            else:
                scheduling_date = 'Multiple Date'

            l10n_in_gst_treatment = ''
            if cio.l10n_in_gst_treatment == 'regular':
                l10n_in_gst_treatment = 'Registered Business - Regular'
            elif cio.l10n_in_gst_treatment == 'composition':
                l10n_in_gst_treatment = 'Registered Business - Composition'
            elif cio.l10n_in_gst_treatment == 'unregistered':
                l10n_in_gst_treatment = 'Unregistered Business'
            elif cio.l10n_in_gst_treatment == 'consumer':
                l10n_in_gst_treatment = 'Consumer'
            elif cio.l10n_in_gst_treatment == 'overseas':
                l10n_in_gst_treatment = 'Overseas'
            elif cio.l10n_in_gst_treatment == 'special_economic_zone':
                l10n_in_gst_treatment = 'Special Economic Zone'
            elif cio.l10n_in_gst_treatment == 'deemed_export':
                l10n_in_gst_treatment = 'Deemed Export'
            elif cio.l10n_in_gst_treatment == 'uin_holders':
                l10n_in_gst_treatment = 'UIN Holders'

            for adv_lines in cio.advertisement_line_ids:
                adv_lines_dict.append({
                    "id": adv_lines.id if adv_lines.id else 0,
                    "product_id": adv_lines.product_id.id if adv_lines.product_id.id else 0,
                    "product_name": adv_lines.product_id.name if adv_lines.product_id.name else '',
                    'advertisement_description': adv_lines.advertisement_description if adv_lines.advertisement_description else '',
                    'no_of_characters': adv_lines.no_of_characters if adv_lines.no_of_characters else 0,
                    'no_of_lines': adv_lines.no_of_lines if adv_lines.no_of_lines else 0,
                })

            line_order = []
            related_documents_list = []
            for rel_docs in cio.sale_related_document_ids:
                related_documents_list.append(
                    {
                        'id': rel_docs.id if rel_docs.id else 0,
                        'doc_name': rel_docs.name.name if rel_docs.name else '',
                        'doc_id': rel_docs.name.id if rel_docs.id else 0,
                        'related_document': rel_docs.related_document if rel_docs.related_document else '',
                    })
            for line in cio.order_line:
                publication_line_list = []
                for publication_line in line.publication_line_ids:
                    region_list = []
                    for regions in publication_line.publication_region_ids:
                        region_list.append({
                            'id': regions.id if regions.id else 0,
                            'region_name': regions.name if regions.name else ''
                        })
                    publication_line_list.append({
                        'id': publication_line.id if publication_line.id else 0,
                        'publication_id': publication_line.publication_id.id if publication_line.publication_id.id else 0,
                        'publication_name': publication_line.publication_id.name if publication_line.publication_id.name else '',
                        'region_ids': region_list
                    })
                tax_name_list = []
                tax_id_list = []

                for tax in line.tax_id:
                    tax_name_list.append(tax.name)
                    tax_id_list.append(tax.id)

                if line.sale_type == 'main':
                    sale_type = "Main"
                else:
                    sale_type = "Mini"

                line_order.append({
                    'id': line.id if line.id else 0,
                    'product_id': line.product_template_id.id if line.product_template_id.id else 0,
                    'product_name': line.product_template_id.name if line.product_template_id.name else '',
                    'product_varients_id': line.product_id.id if line.product_id.id else 0,
                    'product_varients_name': line.product_id.product_template_attribute_value_ids.name if line.product_id.product_template_attribute_value_ids else line.product_id.name,
                    'description': line.name if line.name else '',
                    'size': line.size if line.size else '',
                    'product_uom_qty': line.product_uom_qty if line.product_uom_qty else 0.00,
                    'product_uom_id': line.product_uom.id if line.product_uom.id else 0,
                    'product_uom': line.product_uom.name if line.product_uom.name else '',
                    'page_id': line.page.id if line.page.id else 0,
                    'page_name': str(line.page.name) + ' - ' + str(line.page.page_name) if line.page else '',
                    'pricelist_id': line.product_pricelist_id.id if line.product_pricelist_id else 0,
                    'pricelist_name': line.product_pricelist_id.name if line.product_pricelist_id else '',
                    'tax_id': line.tax_id.ids,
                    'tax_name': tax_name_list,
                    'ad_position_id': line.ad_position.id if line.ad_position.id else 0,
                    'ad_position': line.ad_position.name if line.ad_position else '',
                    'price_unit': line.price_unit if line.price_unit else 0.00,
                    'discount': line.discount if line.discount else 0,
                    'price_subtotal': line.price_subtotal if line.price_subtotal else 0.00,
                    'main_category_id': line.main_category.id if line.main_category.id else 0,
                    'main_category_name': line.main_category.name if line.main_category.name else '',
                    'sub_category_id': line.sub_category.id if line.sub_category.id else 0,
                    'sub_category_name': line.sub_category.name if line.sub_category.name else '',
                    'sale_type': sale_type,
                    'main_area_id': line.main_area.id if line.main_area.id else 0,
                    'main_area_name': line.main_area.name if line.main_area.name else '',
                    'sub_area_id': line.sub_area.id if line.sub_area.id else 0,
                    'sub_area_name': line.sub_area.name if line.sub_area.name else '',
                    'package_id': line.packages.id if line.packages.id else 0,
                    'package_name': line.packages.name if line.packages.name else '',
                    'publication_line_list': publication_line_list,
                })

            payment_information_list = []

            for payment_line in cio.payment_information_ids:

                if payment_line.payment_type == 0.00:
                    payment_type = 'Full Payment'
                else:
                    payment_type = 'Partial Payment'

                payment_mode = ''

                if payment_line.payment_mode == 'cash':
                    payment_mode = 'Cash'
                elif payment_line.payment_mode == 'upi':
                    payment_mode = 'UPI/QR'
                elif payment_line.payment_mode == 'bank':
                    payment_mode = 'Bank - NEFT'
                elif payment_line.payment_mode == 'pdc':
                    payment_mode = 'Cheque'

                if payment_line.payment_media == 'gpay':
                    payment_media = 'Google Pay'
                elif payment_line.payment_media == 'phonepe':
                    payment_media = 'Phonepe'
                elif payment_line.payment_media == 'paytm':
                    payment_media = 'Paytm'
                elif payment_line.payment_media == 'upi':
                    payment_media = 'UPI'
                else:
                    payment_media = ''


                payment_information_list.append({
                    'payment_type': payment_type,
                    'payment_mode': payment_mode,
                    'agent_name': payment_line.agent_id.name if payment_line.agent_id else '',
                    'payee_name': payment_line.payee_name if payment_line.payee_name else '',
                    'payee_mobile': payment_line.payee_mobile if payment_line.payee_mobile else '',
                    'payment_datetime': payment_line.payment_datetime if payment_line.payment_datetime else '',
                    'payment_amount': payment_line.payment_amount if payment_line.payment_amount else 0.00,
                    'payment_location': payment_line.payment_location if payment_line.payment_location else '',
                    'sender_acc_no': payment_line.sender_acc_no if payment_line.sender_acc_no else '',
                    'tnx_id': payment_line.tnx_id if payment_line.tnx_id else '',
                    'payment_media': payment_media,
                    'utr_no': payment_line.utr_no if payment_line.utr_no else '',
                    'payment_confirmation_file': payment_line.payment_confirmation_file if payment_line.payment_confirmation_file else '',
                    'acc_branch_name': payment_line.acc_branch_name if payment_line.acc_branch_name else '',
                    'cheque_no': payment_line.cheque_no if payment_line.cheque_no else '',
                    'cheque_date': payment_line.cheque_date if payment_line.cheque_date else '',
                    'siginig_authority': payment_line.siginig_authority if payment_line.siginig_authority else '',
                    'micr_no': payment_line.micr_no if payment_line.micr_no else '',
                    'ifsc': payment_line.ifsc if payment_line.ifsc else '',
                    'bank_name': payment_line.bank_name if payment_line.bank_name else '',
                    'cheque_expiry_date': payment_line.cheque_expiry_date if payment_line.cheque_expiry_date else '',
                })

            cio_dict.update({
                'id': cio.id if cio.id else 0,
                'cio_ref_num': cio.custom_seq if cio.custom_seq else '',
                'ro_ref_num': cio.custom_sale_seq if cio.custom_sale_seq else '',
                'reta_state': cio.reta_state,
                'is_schedule_done': cio.is_schedule_done,
                'partner_id': cio.partner_id.id if cio.partner_id.id else 0,
                'partner_code': cio.partner_id.cust_seq if cio.partner_id.cust_seq else '',
                'partner_name': cio.partner_id.name if cio.partner_id.name else '',
                'mobile_number': mobile,
                'is_sthirasthi': cio.is_sthirasthi,
                'agent_id': cio.agent_name.id if cio.agent_name.id else 0,
                'agent_name': cio.agent_name.name if cio.agent_name.name else '',
                'scheduling_date': scheduling_date if scheduling_date else '',
                'specific_date': cio.specific_date if cio.specific_date else '',
                'from_date': cio.from_date if cio.from_date else '',
                'to_date': cio.to_date if cio.to_date else '',
                'publish_start_date': cio.publish_start_date if cio.publish_start_date else '',
                'no_of_occurence': cio.no_of_occurence if cio.no_of_occurence else 0,
                'time_interval': cio.time_interval if cio.time_interval else 0,
                'l10n_in_gst_treatment': l10n_in_gst_treatment,
                'quotation_date': cio.date_order if cio.date_order else '',
                'pricelist_id': cio.pricelist_id.id if cio.pricelist_id.id else 0,
                'pricelist_name': cio.pricelist_id.name if cio.pricelist_id.name else '',
                'package_id': cio.packages.id if cio.packages.id else 0,
                'package_name': cio.packages.name if cio.packages.name else '',
                'cio_paid_amount': cio.cio_paid_amount if cio.cio_paid_amount else 0.00,
                'cio_amount_due': cio.cio_amount_due if cio.cio_amount_due else 0.00,
                'publication_id': cio.publication_id.id if cio.publication_id.id else 0,
                'publication_name': cio.publication_id.name if cio.publication_id.name else '',
                'amount_untaxed': round(cio.amount_untaxed, 2) if cio.amount_untaxed else 0.00,
                'amount_tax': round(cio.amount_tax, 2) if cio.amount_tax else 0.00,
                'amount_total': round(cio.amount_total, 2) if cio.amount_total else 0.00,
                'is_online': cio.is_online,
                'line_orders': line_order,
                'related_documents_list': related_documents_list,
                'advertisement_language': advertisement_language,
                'advertisement_lines': adv_lines_dict,
                'payment_information_list': payment_information_list
            })
        return cio_dict

    @restapi.method([(["/scheduling/<int:rec_id>"], "GET")], auth="user")
    def scheduling(self, rec_id):
        sched_dict = {}
        sched_details_obj = self.env['sale.order'].search(
            [('id', '=', rec_id), ('classified_bool_field', '=', True), ('classified_state', '=', 'sent')])

        if sched_details_obj.partner_id.mobile:
            mobile = sched_details_obj.partner_id.mobile.replace('+91', '').replace(' ', '')
        else:
            mobile = ''

        for sched in sched_details_obj:
            adv_lines_dict = []
            advertisement_language = ''
            if sched.advertisement_language == 'telugu':
                advertisement_language = 'Telugu'
            elif sched.advertisement_language == 'english':
                advertisement_language = 'English'
            elif sched.advertisement_language == 'both':
                advertisement_language == 'Both'

            if sched.scheduling_date == 'specific_date':
                scheduling_date = 'Specific Date'
            else:
                scheduling_date = 'Multiple Date'

            l10n_in_gst_treatment = ''
            if sched.l10n_in_gst_treatment == 'regular':
                l10n_in_gst_treatment = 'Registered Business - Regular'
            elif sched.l10n_in_gst_treatment == 'composition':
                l10n_in_gst_treatment = 'Registered Business - Composition'
            elif sched.l10n_in_gst_treatment == 'unregistered':
                l10n_in_gst_treatment = 'Unregistered Business'
            elif sched.l10n_in_gst_treatment == 'consumer':
                l10n_in_gst_treatment = 'Consumer'
            elif sched.l10n_in_gst_treatment == 'overseas':
                l10n_in_gst_treatment = 'Overseas'
            elif sched.l10n_in_gst_treatment == 'special_economic_zone':
                l10n_in_gst_treatment = 'Special Economic Zone'
            elif sched.l10n_in_gst_treatment == 'deemed_export':
                l10n_in_gst_treatment = 'Deemed Export'
            elif sched.l10n_in_gst_treatment == 'uin_holders':
                l10n_in_gst_treatment = 'UIN Holders'

            for adv_lines in sched.advertisement_line_ids:
                adv_lines_dict.append({
                    "id": adv_lines.id if adv_lines.id else 0,
                    "product_id": adv_lines.product_id.id if adv_lines.product_id.id else 0,
                    "product_name": adv_lines.product_id.name if adv_lines.product_id.name else '',
                    'advertisement_description': adv_lines.advertisement_description if adv_lines.advertisement_description else '',
                    'no_of_characters': adv_lines.no_of_characters if adv_lines.no_of_characters else 0,
                    'no_of_lines': adv_lines.no_of_lines if adv_lines.no_of_lines else 0,
                })

            line_order = []
            related_documents_list = []
            for rel_docs in sched.sale_related_document_ids:
                related_documents_list.append(
                    {
                        'id': rel_docs.id if rel_docs.id else 0,
                        'doc_name': rel_docs.name.name if rel_docs.name else '',
                        'doc_id': rel_docs.name.id if rel_docs.id else 0,
                        'related_document': rel_docs.related_document if rel_docs.related_document else '',
                    })
            for line in sched.order_line:
                publication_line_list = []
                for publication_line in line.publication_line_ids:
                    region_list = []
                    for regions in publication_line.publication_region_ids:
                        region_list.append({
                            'id': regions.id if regions.id else 0,
                            'region_name': regions.name if regions.name else ''
                        })
                    publication_line_list.append({
                        'id': publication_line.id if publication_line.id else 0,
                        'publication_id': publication_line.publication_id.id if publication_line.publication_id.id else 0,
                        'publication_name': publication_line.publication_id.name if publication_line.publication_id.name else '',
                        'region_ids': region_list
                    })
                tax_name_list = []
                tax_id_list = []

                for tax in line.tax_id:
                    tax_name_list.append(tax.name)
                    tax_id_list.append(tax.id)

                if line.sale_type == 'main':
                    sale_type = "Main"
                else:
                    sale_type = "Mini"

                line_order.append({
                    'id': line.id if line.id else 0,
                    'product_id': line.product_template_id.id if line.product_template_id.id else 0,
                    'product_name': line.product_template_id.name if line.product_template_id.name else '',
                    'product_varients_id': line.product_id.id if line.product_id.id else 0,
                    'product_varients_name': line.product_id.product_template_attribute_value_ids.name if line.product_id.product_template_attribute_value_ids else line.product_id.name,
                    'description': line.name if line.name else '',
                    'size': line.size if line.size else '',
                    'product_uom_qty': line.product_uom_qty if line.product_uom_qty else 0.00,
                    'product_uom_id': line.product_uom.id if line.product_uom.id else 0,
                    'product_uom': line.product_uom.name if line.product_uom.name else '',
                    'page_id': line.page.id if line.page.id else 0,
                    'page_name': str(line.page.name) + ' - ' + str(line.page.page_name) if line.page else '',
                    'pricelist_id': line.product_pricelist_id.id if line.product_pricelist_id else 0,
                    'pricelist_name': line.product_pricelist_id.name if line.product_pricelist_id.name else '',
                    'tax_id': line.tax_id.ids,
                    'tax_name': tax_name_list,
                    'ad_position_id': line.ad_position.id if line.ad_position.id else 0,
                    'ad_position': line.ad_position.name if line.ad_position else '',
                    'price_unit': line.price_unit if line.price_unit else 0.00,
                    'discount': line.discount if line.discount else 0,
                    'price_subtotal': line.price_subtotal if line.price_subtotal else 0.00,
                    'main_category_id': line.main_category.id if line.main_category.id else 0,
                    'main_category_name': line.main_category.name if line.main_category.name else '',
                    'sub_category_id': line.sub_category.id if line.sub_category.id else 0,
                    'sub_category_name': line.sub_category.name if line.sub_category.name else '',
                    'sale_type': sale_type,
                    'main_area_id': line.main_area.id if line.main_area.id else 0,
                    'main_area_name': line.main_area.name if line.main_area.name else '',
                    'sub_area_id': line.sub_area.id if line.sub_area.id else 0,
                    'sub_area_name': line.sub_area.name if line.sub_area.name else '',
                    'package_id': line.packages.id if line.packages.id else 0,
                    'package_name': line.packages.name if line.packages.name else '',
                    'publication_line_list': publication_line_list,
                })

            payment_information_list = []

            for payment_line in sched.payment_information_ids:
                if payment_line.payment_type == 0.00:
                    payment_type = 'Full Payment'
                else:
                    payment_type = 'Partial Payment'

                if payment_line.payment_mode == 'cash':
                    payment_mode = 'Cash'
                elif payment_line.payment_mode == 'upi':
                    payment_mode = 'UPI/QR'
                elif payment_line.payment_mode == 'bank':
                    payment_mode = 'Bank - NEFT'
                elif payment_line.payment_mode == 'pdc':
                    payment_mode = 'Cheque'


                if payment_line.payment_media == 'gpay':
                    payment_media = 'Google Pay'
                elif payment_line.payment_media == 'phonepe':
                    payment_media = 'Phonepe'
                elif payment_line.payment_media == 'paytm':
                    payment_media = 'Paytm'
                elif payment_line.payment_media == 'upi':
                    payment_media = 'UPI'
                else:
                    payment_media = ''

                payment_information_list.append({
                    'payment_type': payment_type,
                    'payment_mode': payment_mode,
                    'agent_name': payment_line.agent_id.name if payment_line.agent_id else '',
                    'payee_name': payment_line.payee_name if payment_line.payee_name else '',
                    'payee_mobile': payment_line.payee_mobile if payment_line.payee_mobile else '',
                    'payment_datetime': payment_line.payment_datetime if payment_line.payment_datetime else '',
                    'payment_amount': payment_line.payment_amount if payment_line.payment_amount else 0.00,
                    'payment_location': payment_line.payment_location if payment_line.payment_location else '',
                    'sender_acc_no': payment_line.sender_acc_no if payment_line.sender_acc_no else '',
                    'tnx_id': payment_line.tnx_id if payment_line.tnx_id else '',
                    'payment_media': payment_media,
                    'utr_no': payment_line.utr_no if payment_line.utr_no else '',
                    'payment_confirmation_file': payment_line.payment_confirmation_file if payment_line.payment_confirmation_file else '',
                    'acc_branch_name': payment_line.acc_branch_name if payment_line.acc_branch_name else '',
                    'cheque_no': payment_line.cheque_no if payment_line.cheque_no else '',
                    'cheque_date': payment_line.cheque_date if payment_line.cheque_date else '',
                    'siginig_authority': payment_line.siginig_authority if payment_line.siginig_authority else '',
                    'micr_no': payment_line.micr_no if payment_line.micr_no else '',
                    'ifsc': payment_line.ifsc if payment_line.ifsc else '',
                    'bank_name': payment_line.bank_name if payment_line.bank_name else '',
                    'cheque_expiry_date': payment_line.cheque_expiry_date if payment_line.cheque_expiry_date else '',
                })

            sched_dict.update({
                'id': sched.id if sched.id else 0,
                'cio_ref_num': sched.custom_seq if sched.custom_seq else '',
                'ro_ref_num': sched.custom_sale_seq if sched.custom_sale_seq else '',
                'reta_state': sched.reta_state,
                'is_schedule_done': sched.is_schedule_done,
                'partner_id': sched.partner_id.id if sched.partner_id.id else 0,
                'partner_code': sched.partner_id.cust_seq if sched.partner_id.cust_seq else '',
                'partner_name': sched.partner_id.name if sched.partner_id.name else '',
                'mobile_number': mobile,
                'is_sthirasthi': sched.is_sthirasthi,
                'agent_id': sched.agent_name.id if sched.agent_name.id else 0,
                'agent_name': sched.agent_name.name if sched.agent_name.name else '',
                'scheduling_date': scheduling_date if scheduling_date else '',
                'specific_date': sched.specific_date if sched.specific_date else '',
                'from_date': sched.from_date if sched.from_date else '',
                'to_date': sched.to_date if sched.to_date else '',
                'publish_start_date': sched.publish_start_date if sched.publish_start_date else '',
                'no_of_occurence': sched.no_of_occurence if sched.no_of_occurence else 0,
                'time_interval': sched.time_interval if sched.time_interval else 0,
                'l10n_in_gst_treatment': l10n_in_gst_treatment,
                'quotation_date': sched.date_order if sched.date_order else '',
                'pricelist_id': sched.pricelist_id.id if sched.pricelist_id.id else 0,
                'pricelist_name': sched.pricelist_id.name if sched.pricelist_id.name else '',
                'package_id': sched.packages.id if sched.packages.id else 0,
                'package_name': sched.packages.name if sched.packages.name else '',
                'cio_paid_amount': sched.cio_paid_amount if sched.cio_paid_amount else 0.00,
                'cio_amount_due': sched.cio_amount_due if sched.cio_amount_due else 0.00,
                'publication_id': sched.publication_id.id if sched.publication_id.id else 0,
                'publication_name': sched.publication_id.name if sched.publication_id.name else '',
                'amount_untaxed': round(sched.amount_untaxed, 2) if sched.amount_untaxed else 0.00,
                'amount_tax': round(sched.amount_tax, 2) if sched.amount_tax else 0.00,
                'amount_total': round(sched.amount_total, 2) if sched.amount_total else 0.00,
                'is_online': sched.is_online,
                'line_orders': line_order,
                'related_documents_list': related_documents_list,
                'advertisement_language': advertisement_language,
                'advertisement_lines': adv_lines_dict,
                'payment_information_list': payment_information_list
            })

        return sched_dict

    @restapi.method([(["/waiting_for_approval/<int:rec_id>"], "GET")], auth="user")
    def waiting_for_approval(self, rec_id):
        waiting_details_dict = {}
        waiting_details_obj = self.env['sale.order'].search(
            [('id', '=', rec_id), ('classified_bool_field', '=', True),
             ('reta_state', '=', 'waiting_for_approval')])

        if waiting_details_obj.partner_id.mobile:
            mobile = waiting_details_obj.partner_id.mobile.replace('+91', '').replace(' ', '')
        else:
            mobile = ''

        for waiting in waiting_details_obj:
            adv_lines_dict = []
            advertisement_language = ''

            if waiting.advertisement_language == 'telugu':
                advertisement_language = 'Telugu'
            elif waiting.advertisement_language == 'english':
                advertisement_language = 'English'
            elif waiting.advertisement_language == 'both':
                advertisement_language == 'Both'

            if waiting.scheduling_date == 'specific_date':
                scheduling_date = 'Specific Date'
            else:
                scheduling_date = 'Multiple Date'

            l10n_in_gst_treatment = ''
            if waiting.l10n_in_gst_treatment == 'regular':
                l10n_in_gst_treatment = 'Registered Business - Regular'
            elif waiting.l10n_in_gst_treatment == 'composition':
                l10n_in_gst_treatment = 'Registered Business - Composition'
            elif waiting.l10n_in_gst_treatment == 'unregistered':
                l10n_in_gst_treatment = 'Unregistered Business'
            elif waiting.l10n_in_gst_treatment == 'consumer':
                l10n_in_gst_treatment = 'Consumer'
            elif waiting.l10n_in_gst_treatment == 'overseas':
                l10n_in_gst_treatment = 'Overseas'
            elif waiting.l10n_in_gst_treatment == 'special_economic_zone':
                l10n_in_gst_treatment = 'Special Economic Zone'
            elif waiting.l10n_in_gst_treatment == 'deemed_export':
                l10n_in_gst_treatment = 'Deemed Export'
            elif waiting.l10n_in_gst_treatment == 'uin_holders':
                l10n_in_gst_treatment = 'UIN Holders'

            for adv_lines in waiting.advertisement_line_ids:
                adv_lines_dict.append({
                    "id": adv_lines.id if adv_lines.id else 0,
                    "product_id": adv_lines.product_id.id if adv_lines.product_id.id else 0,
                    "product_name": adv_lines.product_id.name if adv_lines.product_id.name else '',
                    'advertisement_description': adv_lines.advertisement_description if adv_lines.advertisement_description else '',
                    'no_of_characters': adv_lines.no_of_characters if adv_lines.no_of_characters else 0,
                    'no_of_lines': adv_lines.no_of_lines if adv_lines.no_of_lines else 0,
                })

            line_order = []
            related_documents_list = []
            for rel_docs in waiting.sale_related_document_ids:
                related_documents_list.append(
                    {
                        'id': rel_docs.id if rel_docs.id else 0,
                        'doc_name': rel_docs.name.name if rel_docs.name else '',
                        'doc_id': rel_docs.name.id if rel_docs.id else 0,
                        'related_document': rel_docs.related_document if rel_docs.related_document else '',
                    })
            for line in waiting.order_line:
                publication_line_list = []
                for publication_line in line.publication_line_ids:
                    region_list = []
                    for regions in publication_line.publication_region_ids:
                        region_list.append({
                            'id': regions.id if regions.id else 0,
                            'region_name': regions.name if regions.name else ''
                        })
                    publication_line_list.append({
                        'id': publication_line.id if publication_line.id else 0,
                        'publication_id': publication_line.publication_id.id if publication_line.publication_id.id else 0,
                        'publication_name': publication_line.publication_id.name if publication_line.publication_id.name else '',
                        'region_ids': region_list
                    })
                tax_name_list = []
                tax_id_list = []

                for tax in line.tax_id:
                    tax_name_list.append(tax.name)
                    tax_id_list.append(tax.id)

                if line.sale_type == 'main':
                    sale_type = "Main"
                else:
                    sale_type = "Mini"

                line_order.append({
                    'id': line.id if line.id else 0,
                    'product_id': line.product_template_id.id if line.product_template_id.id else 0,
                    'product_name': line.product_template_id.name if line.product_template_id.name else '',
                    'product_varients_id': line.product_id.id if line.product_id.id else 0,
                    'product_varients_name': line.product_id.product_template_attribute_value_ids.name if line.product_id.product_template_attribute_value_ids else line.product_id.name,
                    'description': line.name if line.name else '',
                    'size': line.size if line.size else '',
                    'product_uom_qty': line.product_uom_qty if line.product_uom_qty else 0.00,
                    'product_uom_id': line.product_uom.id if line.product_uom.id else 0,
                    'product_uom': line.product_uom.name if line.product_uom.name else '',
                    'page_id': line.page.id if line.page.id else 0,
                    'page_name': str(line.page.name) + ' - ' + str(line.page.page_name) if line.page else '',
                    'pricelist_id': line.product_pricelist_id.id if line.product_pricelist_id else 0,
                    'pricelist_name': line.product_pricelist_id.name if line.product_pricelist_id.name else '',
                    'tax_id': line.tax_id.ids,
                    'tax_name': tax_name_list,
                    'ad_position_id': line.ad_position.id if line.ad_position.id else 0,
                    'ad_position': line.ad_position.name if line.ad_position else '',
                    'price_unit': line.price_unit if line.price_unit else 0.00,
                    'discount': line.discount if line.discount else 0,
                    'price_subtotal': line.price_subtotal if line.price_subtotal else 0.00,
                    'main_category_id': line.main_category.id if line.main_category.id else 0,
                    'main_category_name': line.main_category.name if line.main_category.name else '',
                    'sub_category_id': line.sub_category.id if line.sub_category.id else 0,
                    'sub_category_name': line.sub_category.name if line.sub_category.name else '',
                    'sale_type': sale_type,
                    'main_area_id': line.main_area.id if line.main_area.id else 0,
                    'main_area_name': line.main_area.name if line.main_area.name else '',
                    'sub_area_id': line.sub_area.id if line.sub_area.id else 0,
                    'sub_area_name': line.sub_area.name if line.sub_area.name else '',
                    'package_id': line.packages.id if line.packages.id else 0,
                    'package_name': line.packages.name if line.packages.name else '',
                    'publication_line_list': publication_line_list,
                })

            payment_information_list = []

            for payment_line in waiting.payment_information_ids:

                if payment_line.payment_type == 0.00:
                    payment_type = 'Full Payment'
                else:
                    payment_type = 'Partial Payment'

                if payment_line.payment_mode == 'cash':
                    payment_mode = 'Cash'
                elif payment_line.payment_mode == 'upi':
                    payment_mode = 'UPI/QR'
                elif payment_line.payment_mode == 'bank':
                    payment_mode = 'Bank - NEFT'
                elif payment_line.payment_mode == 'pdc':
                    payment_mode = 'Cheque'

                if payment_line.payment_media == 'gpay':
                    payment_media = 'Google Pay'
                elif payment_line.payment_media == 'phonepe':
                    payment_media = 'Phonepe'
                elif payment_line.payment_media == 'paytm':
                    payment_media = 'Paytm'
                elif payment_line.payment_media == 'upi':
                    payment_media = 'UPI'
                else:
                    payment_media = ''

                payment_information_list.append({
                    'payment_type': payment_type,
                    'payment_mode': payment_mode,
                    'agent_name': payment_line.agent_id.name if payment_line.agent_id else '',
                    'payee_name': payment_line.payee_name if payment_line.payee_name else '',
                    'payee_mobile': payment_line.payee_mobile if payment_line.payee_mobile else '',
                    'payment_datetime': payment_line.payment_datetime if payment_line.payment_datetime else '',
                    'payment_amount': payment_line.payment_amount if payment_line.payment_amount else 0.00,
                    'payment_location': payment_line.payment_location if payment_line.payment_location else '',
                    'sender_acc_no': payment_line.sender_acc_no if payment_line.sender_acc_no else '',
                    'tnx_id': payment_line.tnx_id if payment_line.tnx_id else '',
                    'payment_media': payment_media,
                    'utr_no': payment_line.utr_no if payment_line.utr_no else '',
                    'payment_confirmation_file': payment_line.payment_confirmation_file if payment_line.payment_confirmation_file else '',
                    'acc_branch_name': payment_line.acc_branch_name if payment_line.acc_branch_name else '',
                    'cheque_no': payment_line.cheque_no if payment_line.cheque_no else '',
                    'cheque_date': payment_line.cheque_date if payment_line.cheque_date else '',
                    'siginig_authority': payment_line.siginig_authority if payment_line.siginig_authority else '',
                    'micr_no': payment_line.micr_no if payment_line.micr_no else '',
                    'ifsc': payment_line.ifsc if payment_line.ifsc else '',
                    'bank_name': payment_line.bank_name if payment_line.bank_name else '',
                    'cheque_expiry_date': payment_line.cheque_expiry_date if payment_line.cheque_expiry_date else '',
                })

            waiting_details_dict.update({
                'id': waiting.id if waiting.id else 0,
                'cio_ref_num': waiting.custom_seq if waiting.custom_seq else '',
                'ro_ref_num': waiting.custom_sale_seq if waiting.custom_sale_seq else '',
                'reta_state': waiting.reta_state,
                'is_schedule_done': waiting.is_schedule_done,
                'partner_id': waiting.partner_id.id if waiting.partner_id.id else 0,
                'partner_code': waiting.partner_id.cust_seq if waiting.partner_id.cust_seq else '',
                'partner_name': waiting.partner_id.name if waiting.partner_id.name else '',
                'mobile_number': mobile,
                'is_sthirasthi': waiting.is_sthirasthi,
                'agent_id': waiting.agent_name.id if waiting.agent_name.id else 0,
                'agent_name': waiting.agent_name.name if waiting.agent_name.name else '',
                'scheduling_date': scheduling_date if scheduling_date else '',
                'specific_date': waiting.specific_date if waiting.specific_date else '',
                'from_date': waiting.from_date if waiting.from_date else '',
                'to_date': waiting.to_date if waiting.to_date else '',
                'publish_start_date': waiting.publish_start_date if waiting.publish_start_date else '',
                'no_of_occurence': waiting.no_of_occurence if waiting.no_of_occurence else 0,
                'time_interval': waiting.time_interval if waiting.time_interval else 0,
                'l10n_in_gst_treatment': l10n_in_gst_treatment,
                'quotation_date': waiting.date_order if waiting.date_order else '',
                'pricelist_id': waiting.pricelist_id.id if waiting.pricelist_id.id else 0,
                'pricelist_name': waiting.pricelist_id.name if waiting.pricelist_id.name else '',
                'package_id': waiting.packages.id if waiting.packages.id else 0,
                'package_name': waiting.packages.name if waiting.packages.name else '',
                'cio_paid_amount': waiting.cio_paid_amount if waiting.cio_paid_amount else 0.00,
                'cio_amount_due': waiting.cio_amount_due if waiting.cio_amount_due else 0.00,
                'publication_id': waiting.publication_id.id if waiting.publication_id.id else 0,
                'publication_name': waiting.publication_id.name if waiting.publication_id.name else '',
                'amount_untaxed': round(waiting.amount_untaxed, 2) if waiting.amount_untaxed else 0.00,
                'amount_tax': round(waiting.amount_tax, 2) if waiting.amount_tax else 0.00,
                'amount_total': round(waiting.amount_total, 2) if waiting.amount_total else 0.00,
                'is_online': waiting.is_online,
                'line_orders': line_order,
                'related_documents_list': related_documents_list,
                'advertisement_language': advertisement_language,
                'advertisement_lines': adv_lines_dict,
                'payment_information_list': payment_information_list
            })
        return waiting_details_dict

    @restapi.method([(["/release_order/<int:rec_id>"], "GET")], auth="user")
    def release_order(self, rec_id):
        release_order_dict = {}
        release_obj = self.env['sale.order'].search(
            [('id', '=', rec_id), ('classified_bool_field', '=', True), ('classified_state', '=', 'sale')])

        if release_obj.partner_id.mobile:
            mobile = release_obj.partner_id.mobile.replace('+91', '').replace(' ', '')
        else:
            mobile = ''

        for release in release_obj:
            adv_lines_dict = []
            advertisement_language = ''

            if release.advertisement_language == 'telugu':
                advertisement_language = 'Telugu'
            elif release.advertisement_language == 'english':
                advertisement_language = 'English'
            elif release.advertisement_language == 'both':
                advertisement_language == 'Both'

            if release.scheduling_date == 'specific_date':
                scheduling_date = 'Specific Date'
            else:
                scheduling_date = 'Multiple Date'

            l10n_in_gst_treatment = ''
            if release.l10n_in_gst_treatment == 'regular':
                l10n_in_gst_treatment = 'Registered Business - Regular'
            elif release.l10n_in_gst_treatment == 'composition':
                l10n_in_gst_treatment = 'Registered Business - Composition'
            elif release.l10n_in_gst_treatment == 'unregistered':
                l10n_in_gst_treatment = 'Unregistered Business'
            elif release.l10n_in_gst_treatment == 'consumer':
                l10n_in_gst_treatment = 'Consumer'
            elif release.l10n_in_gst_treatment == 'overseas':
                l10n_in_gst_treatment = 'Overseas'
            elif release.l10n_in_gst_treatment == 'special_economic_zone':
                l10n_in_gst_treatment = 'Special Economic Zone'
            elif release.l10n_in_gst_treatment == 'deemed_export':
                l10n_in_gst_treatment = 'Deemed Export'
            elif release.l10n_in_gst_treatment == 'uin_holders':
                l10n_in_gst_treatment = 'UIN Holders'

            for adv_lines in release.advertisement_line_ids:
                adv_lines_dict.append({
                    "id": adv_lines.id if adv_lines.id else 0,
                    "product_id": adv_lines.product_id.id if adv_lines.product_id.id else 0,
                    "product_name": adv_lines.product_id.name if adv_lines.product_id.name else '',
                    'advertisement_description': adv_lines.advertisement_description if adv_lines.advertisement_description else '',
                    'no_of_characters': adv_lines.no_of_characters if adv_lines.no_of_characters else 0,
                    'no_of_lines': adv_lines.no_of_lines if adv_lines.no_of_lines else 0,
                })
            line_order = []
            related_documents_list = []
            for rel_docs in release.sale_related_document_ids:
                related_documents_list.append(
                    {
                        'id': rel_docs.id if rel_docs.id else 0,
                        'doc_name': rel_docs.name.name if rel_docs.name else '',
                        'doc_id': rel_docs.name.id if rel_docs.id else 0,
                        'related_document': rel_docs.related_document if rel_docs.related_document else '',
                    })
            for line in release.order_line:
                publication_line_list = []
                for publication_line in line.publication_line_ids:
                    region_list = []
                    for regions in publication_line.publication_region_ids:
                        region_list.append({
                            'id': regions.id if regions.id else 0,
                            'region_name': regions.name if regions.name else ''
                        })
                    publication_line_list.append({
                        'id': publication_line.id if publication_line.id else 0,
                        'publication_id': publication_line.publication_id.id if publication_line.publication_id.id else 0,
                        'publication_name': publication_line.publication_id.name if publication_line.publication_id.name else '',
                        'region_ids': region_list
                    })
                tax_name_list = []
                tax_id_list = []

                for tax in line.tax_id:
                    tax_name_list.append(tax.name)
                    tax_id_list.append(tax.id)

                if line.sale_type == 'main':
                    sale_type = "Main"
                else:
                    sale_type = "Mini"

                line_order.append({
                    'id': line.id if line.id else 0,
                    'product_id': line.product_template_id.id if line.product_template_id.id else 0,
                    'product_name': line.product_template_id.name if line.product_template_id.name else '',
                    'product_varients_id': line.product_id.id if line.product_id.id else 0,
                    'product_varients_name': line.product_id.product_template_attribute_value_ids.name if line.product_id.product_template_attribute_value_ids else line.product_id.name,
                    'description': line.name if line.name else '',
                    'size': line.size if line.size else '',
                    'product_uom_qty': line.product_uom_qty if line.product_uom_qty else 0.00,
                    'product_uom_id': line.product_uom.id if line.product_uom.id else 0,
                    'product_uom': line.product_uom.name if line.product_uom.name else '',
                    'page_id': line.page.id if line.page.id else 0,
                    'page_name': str(line.page.name) + ' - ' + str(line.page.page_name) if line.page else '',
                    'pricelist_id': line.product_pricelist_id.id if line.product_pricelist_id else 0,
                    'pricelist_name': line.product_pricelist_id.name if line.product_pricelist_id.name else '',
                    'tax_id': line.tax_id.ids,
                    'tax_name': tax_name_list,
                    'ad_position_id': line.ad_position.id if line.ad_position.id else 0,
                    'ad_position': line.ad_position.name if line.ad_position else '',
                    'price_unit': line.price_unit if line.price_unit else 0.00,
                    'discount': line.discount if line.discount else 0,
                    'price_subtotal': line.price_subtotal if line.price_subtotal else 0.00,
                    'main_category_id': line.main_category.id if line.main_category.id else 0,
                    'main_category_name': line.main_category.name if line.main_category.name else '',
                    'sub_category_id': line.sub_category.id if line.sub_category.id else 0,
                    'sub_category_name': line.sub_category.name if line.sub_category.name else '',
                    'sale_type': sale_type,
                    'main_area_id': line.main_area.id if line.main_area.id else 0,
                    'main_area_name': line.main_area.name if line.main_area.name else '',
                    'sub_area_id': line.sub_area.id if line.sub_area.id else 0,
                    'sub_area_name': line.sub_area.name if line.sub_area.name else '',
                    'package_id': line.packages.id if line.packages.id else 0,
                    'package_name': line.packages.name if line.packages.name else '',
                    'publication_line_list': publication_line_list,
                })

            payment_information_list = []

            for payment_line in release.payment_information_ids:
                if payment_line.payment_type == 0.00:
                    payment_type = 'Full Payment'
                else:
                    payment_type = 'Partial Payment'


                if payment_line.payment_mode == 'cash':
                    payment_mode = 'Cash'
                elif payment_line.payment_mode == 'upi':
                    payment_mode = 'UPI/QR'
                elif payment_line.payment_mode == 'bank':
                    payment_mode = 'Bank - NEFT'
                elif payment_line.payment_mode == 'pdc':
                    payment_mode = 'Cheque'


                if payment_line.payment_media == 'gpay':
                    payment_media = 'Google Pay'
                elif payment_line.payment_media == 'phonepe':
                    payment_media = 'Phonepe'
                elif payment_line.payment_media == 'paytm':
                    payment_media = 'Paytm'
                elif payment_line.payment_media == 'upi':
                    payment_media = 'UPI'
                else:
                    payment_media = ''

                payment_information_list.append({
                    'payment_type': payment_type,
                    'payment_mode': payment_mode,
                    'agent_name': payment_line.agent_id.name if payment_line.agent_id else '',
                    'payee_name': payment_line.payee_name if payment_line.payee_name else '',
                    'payee_mobile': payment_line.payee_mobile if payment_line.payee_mobile else '',
                    'payment_datetime': payment_line.payment_datetime if payment_line.payment_datetime else '',
                    'payment_amount': payment_line.payment_amount if payment_line.payment_amount else 0.00,
                    'payment_location': payment_line.payment_location if payment_line.payment_location else '',
                    'sender_acc_no': payment_line.sender_acc_no if payment_line.sender_acc_no else '',
                    'tnx_id': payment_line.tnx_id if payment_line.tnx_id else '',
                    'payment_media': payment_media,
                    'utr_no': payment_line.utr_no if payment_line.utr_no else '',
                    'payment_confirmation_file': payment_line.payment_confirmation_file if payment_line.payment_confirmation_file else '',
                    'acc_branch_name': payment_line.acc_branch_name if payment_line.acc_branch_name else '',
                    'cheque_no': payment_line.cheque_no if payment_line.cheque_no else '',
                    'cheque_date': payment_line.cheque_date if payment_line.cheque_date else '',
                    'siginig_authority': payment_line.siginig_authority if payment_line.siginig_authority else '',
                    'micr_no': payment_line.micr_no if payment_line.micr_no else '',
                    'ifsc': payment_line.ifsc if payment_line.ifsc else '',
                    'bank_name': payment_line.bank_name if payment_line.bank_name else '',
                    'cheque_expiry_date': payment_line.cheque_expiry_date if payment_line.cheque_expiry_date else '',
                })

            release_order_dict.update({
                'id': release.id if release.id else 0,
                'cio_ref_num': release.custom_seq if release.custom_seq else '',
                'ro_ref_num': release.custom_sale_seq if release.custom_sale_seq else '',
                'reta_state': release.reta_state,
                'is_schedule_done': release.is_schedule_done,
                'partner_id': release.partner_id.id if release.partner_id.id else 0,
                'partner_code': release.partner_id.cust_seq if release.partner_id.cust_seq else '',
                'partner_name': release.partner_id.name if release.partner_id.name else '',
                'mobile_number': mobile,
                'is_sthirasthi': release.is_sthirasthi,
                'agent_id': release.agent_name.id if release.agent_name.id else 0,
                'agent_name': release.agent_name.name if release.agent_name.name else '',
                'scheduling_date': scheduling_date if scheduling_date else '',
                'specific_date': release.specific_date if release.specific_date else '',
                'from_date': release.from_date if release.from_date else '',
                'to_date': release.to_date if release.to_date else '',
                'publish_start_date': release.publish_start_date if release.publish_start_date else '',
                'no_of_occurence': release.no_of_occurence if release.no_of_occurence else 0,
                'time_interval': release.time_interval if release.time_interval else 0,
                'l10n_in_gst_treatment': l10n_in_gst_treatment,
                'quotation_date': release.date_order if release.date_order else '',
                'pricelist_id': release.pricelist_id.id if release.pricelist_id.id else 0,
                'pricelist_name': release.pricelist_id.name if release.pricelist_id.name else '',
                'package_id': release.packages.id if release.packages.id else 0,
                'package_name': release.packages.name if release.packages.name else '',
                'cio_paid_amount': release.cio_paid_amount if release.cio_paid_amount else 0.00,
                'cio_amount_due': release.cio_amount_due if release.cio_amount_due else 0.00,
                'publication_id': release.publication_id.id if release.publication_id.id else 0,
                'publication_name': release.publication_id.name if release.publication_id.name else '',
                'amount_untaxed': round(release.amount_untaxed, 2) if release.amount_untaxed else 0.00,
                'amount_tax': round(release.amount_tax, 2) if release.amount_tax else 0.00,
                'amount_total': round(release.amount_total, 2) if release.amount_total else 0.00,
                'is_online': release.is_online,
                'line_orders': line_order,
                'related_documents_list': related_documents_list,
                'advertisement_language': advertisement_language,
                'advertisement_lines': adv_lines_dict,
                'payment_information_list': payment_information_list
            })
        return release_order_dict

    @restapi.method([(["/rejected/<int:rec_id>"], "GET")], auth="public")
    def rejected(self, rec_id):
        rejected_dict = {}
        rejected_obj = self.env['sale.order'].search(
            [('id', '=', rec_id), ('classified_bool_field', '=', True), ('classified_state', '=', 'cancel')])

        if rejected_obj.partner_id.mobile:
            mobile = rejected_obj.partner_id.mobile.replace('+91', '').replace(' ', '')
        else:
            mobile = ''

        for rejected in rejected_obj:
            adv_lines_dict = []
            advertisement_language = ''

            if rejected.advertisement_language == 'telugu':
                advertisement_language = 'Telugu'
            elif rejected.advertisement_language == 'english':
                advertisement_language = 'English'
            elif rejected.advertisement_language == 'both':
                advertisement_language == 'Both'

            if rejected.scheduling_date == 'specific_date':
                scheduling_date = 'Specific Date'
            else:
                scheduling_date = 'Multiple Date'

            l10n_in_gst_treatment = ''
            if rejected.l10n_in_gst_treatment == 'regular':
                l10n_in_gst_treatment = 'Registered Business - Regular'
            elif rejected.l10n_in_gst_treatment == 'composition':
                l10n_in_gst_treatment = 'Registered Business - Composition'
            elif rejected.l10n_in_gst_treatment == 'unregistered':
                l10n_in_gst_treatment = 'Unregistered Business'
            elif rejected.l10n_in_gst_treatment == 'consumer':
                l10n_in_gst_treatment = 'Consumer'
            elif rejected.l10n_in_gst_treatment == 'overseas':
                l10n_in_gst_treatment = 'Overseas'
            elif rejected.l10n_in_gst_treatment == 'special_economic_zone':
                l10n_in_gst_treatment = 'Special Economic Zone'
            elif rejected.l10n_in_gst_treatment == 'deemed_export':
                l10n_in_gst_treatment = 'Deemed Export'
            elif rejected.l10n_in_gst_treatment == 'uin_holders':
                l10n_in_gst_treatment = 'UIN Holders'

            for adv_lines in rejected.advertisement_line_ids:
                adv_lines_dict.append({
                    "id": adv_lines.id if adv_lines.id else 0,
                    "product_id": adv_lines.product_id.id if adv_lines.product_id.id else 0,
                    "product_name": adv_lines.product_id.name if adv_lines.product_id.name else '',
                    'advertisement_description': adv_lines.advertisement_description if adv_lines.advertisement_description else '',
                    'no_of_characters': adv_lines.no_of_characters if adv_lines.no_of_characters else 0,
                    'no_of_lines': adv_lines.no_of_lines if adv_lines.no_of_lines else 0,
                })
            line_order = []
            related_documents_list = []
            for rel_docs in rejected.sale_related_document_ids:
                related_documents_list.append(
                    {
                        'id': rel_docs.id if rel_docs.id else 0,
                        'doc_name': rel_docs.name.name if rel_docs.name else '',
                        'doc_id': rel_docs.name.id if rel_docs.id else 0,
                        'related_document': rel_docs.related_document if rel_docs.related_document else '',
                    })
            for line in rejected.order_line:
                publication_line_list = []
                for publication_line in line.publication_line_ids:
                    region_list = []
                    for regions in publication_line.publication_region_ids:
                        region_list.append({
                            'id': regions.id if regions.id else 0,
                            'region_name': regions.name if regions.name else ''
                        })
                    publication_line_list.append({
                        'id': publication_line.id if publication_line.id else 0,
                        'publication_id': publication_line.publication_id.id if publication_line.publication_id.id else 0,
                        'publication_name': publication_line.publication_id.name if publication_line.publication_id.name else '',
                        'region_ids': region_list
                    })
                tax_name_list = []
                tax_id_list = []

                for tax in line.tax_id:
                    tax_name_list.append(tax.name)
                    tax_id_list.append(tax.id)

                if line.sale_type == 'main':
                    sale_type = "Main"
                else:
                    sale_type = "Mini"

                line_order.append({
                    'id': line.id if line.id else 0,
                    'product_id': line.product_template_id.id if line.product_template_id.id else 0,
                    'product_name': line.product_template_id.name if line.product_template_id.name else '',
                    'product_varients_id': line.product_id.id if line.product_id.id else 0,
                    'product_varients_name': line.product_id.product_template_attribute_value_ids.name if line.product_id.product_template_attribute_value_ids else line.product_id.name,
                    'description': line.name if line.name else '',
                    'size': line.size if line.size else '',
                    'product_uom_qty': line.product_uom_qty if line.product_uom_qty else 0.00,
                    'product_uom_id': line.product_uom.id if line.product_uom.id else 0,
                    'product_uom': line.product_uom.name if line.product_uom.name else '',
                    'page_id': line.page.id if line.page.id else 0,
                    'page_name': str(line.page.name) + ' - ' + str(line.page.page_name) if line.page else '',
                    'pricelist_id': line.product_pricelist_id.id if line.product_pricelist_id else 0,
                    'pricelist_name': line.product_pricelist_id.name if line.product_pricelist_id.name else '',
                    'tax_id': line.tax_id.ids,
                    'tax_name': tax_name_list,
                    'ad_position_id': line.ad_position.id if line.ad_position.id else 0,
                    'ad_position': line.ad_position.name if line.ad_position else '',
                    'price_unit': line.price_unit if line.price_unit else 0.00,
                    'discount': line.discount if line.discount else 0,
                    'price_subtotal': line.price_subtotal if line.price_subtotal else 0.00,
                    'main_category_id': line.main_category.id if line.main_category.id else 0,
                    'main_category_name': line.main_category.name if line.main_category.name else '',
                    'sub_category_id': line.sub_category.id if line.sub_category.id else 0,
                    'sub_category_name': line.sub_category.name if line.sub_category.name else '',
                    'sale_type': sale_type,
                    'main_area_id': line.main_area.id if line.main_area.id else 0,
                    'main_area_name': line.main_area.name if line.main_area.name else '',
                    'sub_area_id': line.sub_area.id if line.sub_area.id else 0,
                    'sub_area_name': line.sub_area.name if line.sub_area.name else '',
                    'package_id': line.packages.id if line.packages.id else 0,
                    'package_name': line.packages.name if line.packages.name else '',
                    'publication_line_list': publication_line_list,
                })

            payment_information_list = []

            for payment_line in rejected.payment_information_ids:
                if payment_line.payment_type == 0.00:
                    payment_type = 'Full Payment'
                else:
                    payment_type = 'Partial Payment'


                if payment_line.payment_mode == 'cash':
                    payment_mode = 'Cash'
                elif payment_line.payment_mode == 'upi':
                    payment_mode = 'UPI/QR'
                elif payment_line.payment_mode == 'bank':
                    payment_mode = 'Bank - NEFT'
                elif payment_line.payment_mode == 'pdc':
                    payment_mode = 'Cheque'

                if payment_line.payment_media == 'gpay':
                    payment_media = 'Google Pay'
                elif payment_line.payment_media == 'phonepe':
                    payment_media = 'Phonepe'
                elif payment_line.payment_media == 'paytm':
                    payment_media = 'Paytm'
                elif payment_line.payment_media == 'upi':
                    payment_media = 'UPI'
                else:
                    payment_media = ''

                payment_information_list.append({
                    'payment_type': payment_type,
                    'payment_mode': payment_mode,
                    'agent_name': payment_line.agent_id.name if payment_line.agent_id else '',
                    'payee_name': payment_line.payee_name if payment_line.payee_name else '',
                    'payee_mobile': payment_line.payee_mobile if payment_line.payee_mobile else '',
                    'payment_datetime': payment_line.payment_datetime if payment_line.payment_datetime else '',
                    'payment_amount': payment_line.payment_amount if payment_line.payment_amount else 0.00,
                    'payment_location': payment_line.payment_location if payment_line.payment_location else '',
                    'sender_acc_no': payment_line.sender_acc_no if payment_line.sender_acc_no else '',
                    'tnx_id': payment_line.tnx_id if payment_line.tnx_id else '',
                    'payment_media': payment_media,
                    'utr_no': payment_line.utr_no if payment_line.utr_no else '',
                    'payment_confirmation_file': payment_line.payment_confirmation_file if payment_line.payment_confirmation_file else '',
                    'acc_branch_name': payment_line.acc_branch_name if payment_line.acc_branch_name else '',
                    'cheque_no': payment_line.cheque_no if payment_line.cheque_no else '',
                    'cheque_date': payment_line.cheque_date if payment_line.cheque_date else '',
                    'siginig_authority': payment_line.siginig_authority if payment_line.siginig_authority else '',
                    'micr_no': payment_line.micr_no if payment_line.micr_no else '',
                    'ifsc': payment_line.ifsc if payment_line.ifsc else '',
                    'bank_name': payment_line.bank_name if payment_line.bank_name else '',
                    'cheque_expiry_date': payment_line.cheque_expiry_date if payment_line.cheque_expiry_date else '',
                })

            rejected_dict.update({
                'id': rejected.id if rejected.id else 0,
                'cio_ref_num': rejected.custom_seq if rejected.custom_seq else '',
                'ro_ref_num': rejected.custom_sale_seq if rejected.custom_sale_seq else '',
                'reta_state': rejected.reta_state,
                'is_schedule_done': rejected.is_schedule_done,
                'partner_id': rejected.partner_id.id if rejected.partner_id.id else 0,
                'partner_code': rejected.partner_id.cust_seq if rejected.partner_id.cust_seq else '',
                'partner_name': rejected.partner_id.name if rejected.partner_id.name else '',
                'mobile_number': mobile,
                'is_sthirasthi': rejected.is_sthirasthi,
                'agent_id': rejected.agent_name.id if rejected.agent_name.id else 0,
                'agent_name': rejected.agent_name.name if rejected.agent_name.name else '',
                'scheduling_date': scheduling_date if scheduling_date else '',
                'specific_date': rejected.specific_date if rejected.specific_date else '',
                'from_date': rejected.from_date if rejected.from_date else '',
                'to_date': rejected.to_date if rejected.to_date else '',
                'publish_start_date': rejected.publish_start_date if rejected.publish_start_date else '',
                'no_of_occurence': rejected.no_of_occurence if rejected.no_of_occurence else 0,
                'time_interval': rejected.time_interval if rejected.time_interval else 0,
                'l10n_in_gst_treatment': l10n_in_gst_treatment,
                'quotation_date': rejected.date_order if rejected.date_order else '',
                'pricelist_id': rejected.pricelist_id.id if rejected.pricelist_id.id else 0,
                'pricelist_name': rejected.pricelist_id.name if rejected.pricelist_id.name else '',
                'package_id': rejected.packages.id if rejected.packages.id else 0,
                'package_name': rejected.packages.name if rejected.packages.name else '',
                'cio_paid_amount': rejected.cio_paid_amount if rejected.cio_paid_amount else 0.00,
                'cio_amount_due': rejected.cio_amount_due if rejected.cio_amount_due else 0.00,
                'publication_id': rejected.publication_id.id if rejected.publication_id.id else 0,
                'publication_name': rejected.publication_id.name if rejected.publication_id.name else '',
                'amount_untaxed': round(rejected.amount_untaxed, 2) if rejected.amount_untaxed else 0.00,
                'amount_tax': round(rejected.amount_tax, 2) if rejected.amount_tax else 0.00,
                'amount_total': round(rejected.amount_total, 2) if rejected.amount_total else 0.00,
                'is_online': rejected.is_online,
                'line_orders': line_order,
                'related_documents_list': related_documents_list,
                'advertisement_language': advertisement_language,
                'advertisement_lines': adv_lines_dict,
                'payment_information_list': payment_information_list,
            })
        return rejected_dict

    @restapi.method([(["/published/<int:rec_id>"], "GET")], auth="public")
    def published(self, rec_id):
        published_dict = {}
        published_obj = self.env['sale.order'].search(
            [('id', '=', rec_id), ('classified_bool_field', '=', True), ('classified_state', '=', 'print')])

        if published_obj.partner_id.mobile:
            mobile = published_obj.partner_id.mobile.replace('+91', '').replace(' ', '')
        else:
            mobile = ''

        for published in published_obj:
            adv_lines_dict = []
            advertisement_language = ''

            if published.advertisement_language == 'telugu':
                advertisement_language = 'Telugu'
            elif published.advertisement_language == 'english':
                advertisement_language = 'English'
            elif published.advertisement_language == 'both':
                advertisement_language == 'Both'

            if published.scheduling_date == 'specific_date':
                scheduling_date = 'Specific Date'
            else:
                scheduling_date = 'Multiple Date'

            l10n_in_gst_treatment = ''
            if published.l10n_in_gst_treatment == 'regular':
                l10n_in_gst_treatment = 'Registered Business - Regular'
            elif published.l10n_in_gst_treatment == 'composition':
                l10n_in_gst_treatment = 'Registered Business - Composition'
            elif published.l10n_in_gst_treatment == 'unregistered':
                l10n_in_gst_treatment = 'Unregistered Business'
            elif published.l10n_in_gst_treatment == 'consumer':
                l10n_in_gst_treatment = 'Consumer'
            elif published.l10n_in_gst_treatment == 'overseas':
                l10n_in_gst_treatment = 'Overseas'
            elif published.l10n_in_gst_treatment == 'special_economic_zone':
                l10n_in_gst_treatment = 'Special Economic Zone'
            elif published.l10n_in_gst_treatment == 'deemed_export':
                l10n_in_gst_treatment = 'Deemed Export'
            elif published.l10n_in_gst_treatment == 'uin_holders':
                l10n_in_gst_treatment = 'UIN Holders'

            for adv_lines in published.advertisement_line_ids:
                adv_lines_dict.append({
                    "id": adv_lines.id if adv_lines.id else 0,
                    "product_id": adv_lines.product_id.id if adv_lines.product_id.id else 0,
                    "product_name": adv_lines.product_id.name if adv_lines.product_id.name else '',
                    'advertisement_description': adv_lines.advertisement_description if adv_lines.advertisement_description else '',
                    'no_of_characters': adv_lines.no_of_characters if adv_lines.no_of_characters else 0,
                    'no_of_lines': adv_lines.no_of_lines if adv_lines.no_of_lines else 0,
                })
            line_order = []
            related_documents_list = []
            for rel_docs in published.sale_related_document_ids:
                related_documents_list.append(
                    {
                        'id': rel_docs.id if rel_docs.id else 0,
                        'doc_name': rel_docs.name.name if rel_docs.name else '',
                        'doc_id': rel_docs.name.id if rel_docs.id else 0,
                        'related_document': rel_docs.related_document if rel_docs.related_document else '',
                    })
            for line in published.order_line:
                publication_line_list = []
                for publication_line in line.publication_line_ids:
                    region_list = []
                    for regions in publication_line.publication_region_ids:
                        region_list.append({
                            'id': regions.id if regions.id else 0,
                            'region_name': regions.name if regions.name else ''
                        })
                    publication_line_list.append({
                        'id': publication_line.id if publication_line.id else 0,
                        'publication_id': publication_line.publication_id.id if publication_line.publication_id.id else 0,
                        'publication_name': publication_line.publication_id.name if publication_line.publication_id.name else '',
                        'region_ids': region_list
                    })
                tax_name_list = []
                tax_id_list = []

                for tax in line.tax_id:
                    tax_name_list.append(tax.name)
                    tax_id_list.append(tax.id)

                if line.sale_type == 'main':
                    sale_type = "Main"
                else:
                    sale_type = "Mini"

                line_order.append({
                    'id': line.id if line.id else 0,
                    'product_id': line.product_template_id.id if line.product_template_id.id else 0,
                    'product_name': line.product_template_id.name if line.product_template_id.name else '',
                    'product_varients_id': line.product_id.id if line.product_id.id else 0,
                    'product_varients_name': line.product_id.product_template_attribute_value_ids.name if line.product_id.product_template_attribute_value_ids else line.product_id.name,
                    'description': line.name if line.name else '',
                    'size': line.size if line.size else '',
                    'product_uom_qty': line.product_uom_qty if line.product_uom_qty else 0.00,
                    'product_uom_id': line.product_uom.id if line.product_uom.id else 0,
                    'product_uom': line.product_uom.name if line.product_uom.name else '',
                    'page_id': line.page.id if line.page.id else 0,
                    'page_name': str(line.page.name) + ' - ' + str(line.page.page_name) if line.page else '',
                    'pricelist_id': line.product_pricelist_id.id if line.product_pricelist_id else 0,
                    'pricelist_name': line.product_pricelist_id.name if line.product_pricelist_id.name else '',
                    'tax_id': line.tax_id.ids,
                    'tax_name': tax_name_list,
                    'ad_position_id': line.ad_position.id if line.ad_position.id else 0,
                    'ad_position': line.ad_position.name if line.ad_position else '',
                    'price_unit': line.price_unit if line.price_unit else 0.00,
                    'discount': line.discount if line.discount else 0,
                    'price_subtotal': line.price_subtotal if line.price_subtotal else 0.00,
                    'main_category_id': line.main_category.id if line.main_category.id else 0,
                    'main_category_name': line.main_category.name if line.main_category.name else '',
                    'sub_category_id': line.sub_category.id if line.sub_category.id else 0,
                    'sub_category_name': line.sub_category.name if line.sub_category.name else '',
                    'sale_type': sale_type,
                    'main_area_id': line.main_area.id if line.main_area.id else 0,
                    'main_area_name': line.main_area.name if line.main_area.name else '',
                    'sub_area_id': line.sub_area.id if line.sub_area.id else 0,
                    'sub_area_name': line.sub_area.name if line.sub_area.name else '',
                    'package_id': line.packages.id if line.packages.id else 0,
                    'package_name': line.packages.name if line.packages.name else '',
                    'publication_line_list': publication_line_list,
                })

            payment_information_list = []

            for payment_line in published.payment_information_ids:

                if payment_line.payment_type == 0.00:
                    payment_type = 'Full Payment'
                else:
                    payment_type = 'Partial Payment'

                if payment_line.payment_mode == 'cash':
                    payment_mode = 'Cash'
                elif payment_line.payment_mode == 'upi':
                    payment_mode = 'UPI/QR'
                elif payment_line.payment_mode == 'bank':
                    payment_mode = 'Bank - NEFT'
                elif payment_line.payment_mode == 'pdc':
                    payment_mode = 'Cheque'

                if payment_line.payment_media == 'gpay':
                    payment_media = 'Google Pay'
                elif payment_line.payment_media == 'phonepe':
                    payment_media = 'Phonepe'
                elif payment_line.payment_media == 'paytm':
                    payment_media = 'Paytm'
                elif payment_line.payment_media == 'upi':
                    payment_media = 'UPI'
                else:
                    payment_media = ''

                payment_information_list.append({
                    'payment_type': payment_type,
                    'payment_mode': payment_mode,
                    'agent_name': payment_line.agent_id.name if payment_line.agent_id else '',
                    'payee_name': payment_line.payee_name if payment_line.payee_name else '',
                    'payee_mobile': payment_line.payee_mobile if payment_line.payee_mobile else '',
                    'payment_datetime': payment_line.payment_datetime if payment_line.payment_datetime else '',
                    'payment_amount': payment_line.payment_amount if payment_line.payment_amount else 0.00,
                    'payment_location': payment_line.payment_location if payment_line.payment_location else '',
                    'sender_acc_no': payment_line.sender_acc_no if payment_line.sender_acc_no else '',
                    'tnx_id': payment_line.tnx_id if payment_line.tnx_id else '',
                    'payment_media': payment_media,
                    'utr_no': payment_line.utr_no if payment_line.utr_no else '',
                    'payment_confirmation_file': payment_line.payment_confirmation_file if payment_line.payment_confirmation_file else '',
                    'acc_branch_name': payment_line.acc_branch_name if payment_line.acc_branch_name else '',
                    'cheque_no': payment_line.cheque_no if payment_line.cheque_no else '',
                    'cheque_date': payment_line.cheque_date if payment_line.cheque_date else '',
                    'siginig_authority': payment_line.siginig_authority if payment_line.siginig_authority else '',
                    'micr_no': payment_line.micr_no if payment_line.micr_no else '',
                    'ifsc': payment_line.ifsc if payment_line.ifsc else '',
                    'bank_name': payment_line.bank_name if payment_line.bank_name else '',
                    'cheque_expiry_date': payment_line.cheque_expiry_date if payment_line.cheque_expiry_date else '',
                })

            published_dict.update({
                'id': published.id if published.id else 0,
                'cio_ref_num': published.custom_seq if published.custom_seq else '',
                'ro_ref_num': published.custom_sale_seq if published.custom_sale_seq else '',
                'reta_state': published.reta_state,
                'is_schedule_done': published.is_schedule_done,
                'partner_id': published.partner_id.id if published.partner_id.id else 0,
                'partner_code': published.partner_id.cust_seq if published.partner_id.cust_seq else '',
                'partner_name': published.partner_id.name if published.partner_id.name else '',
                'mobile_number': mobile,
                'is_sthirasthi': published.is_sthirasthi,
                'agent_id': published.agent_name.id if published.agent_name.id else 0,
                'agent_name': published.agent_name.name if published.agent_name.name else '',
                'scheduling_date': scheduling_date if scheduling_date else '',
                'specific_date': published.specific_date if published.specific_date else '',
                'from_date': published.from_date if published.from_date else '',
                'to_date': published.to_date if published.to_date else '',
                'publish_start_date': published.publish_start_date if published.publish_start_date else '',
                'no_of_occurence': published.no_of_occurence if published.no_of_occurence else 0,
                'time_interval': published.time_interval if published.time_interval else 0,
                'l10n_in_gst_treatment': l10n_in_gst_treatment,
                'quotation_date': published.date_order if published.date_order else '',
                'pricelist_id': published.pricelist_id.id if published.pricelist_id.id else 0,
                'pricelist_name': published.pricelist_id.name if published.pricelist_id.name else '',
                'package_id': published.packages.id if published.packages.id else 0,
                'package_name': published.packages.name if published.packages.name else '',
                'cio_paid_amount': published.cio_paid_amount if published.cio_paid_amount else 0.00,
                'cio_amount_due': published.cio_amount_due if published.cio_amount_due else 0.00,
                'publication_id': published.publication_id.id if published.publication_id.id else 0,
                'publication_name': published.publication_id.name if published.publication_id.name else '',
                'amount_untaxed': round(published.amount_untaxed, 2) if published.amount_untaxed else 0.00,
                'amount_tax': round(published.amount_tax, 2) if published.amount_tax else 0.00,
                'amount_total': round(published.amount_total, 2) if published.amount_total else 0.00,
                'is_online': published.is_online,
                'line_orders': line_order,
                'related_documents_list': related_documents_list,
                'advertisement_language': advertisement_language,
                'advertisement_lines': adv_lines_dict,
                'payment_information_list': payment_information_list,
            })

        return published_dict

    @restapi.method([(["/create_cio"], "POST")], auth="user")
    def create_cio(self):
        params = request.params
        l10n_in_gst_treatment = ""
        if params.get('scheduling_date') == 'Specific Date':
            scheduling_date = 'specific_date'
        elif params.get('scheduling_date') == 'Multiple Date':
            scheduling_date = 'multiple_date'
        if params.get('l10n_in_gst_treatment') == 'Registered Business - Regular':
            l10n_in_gst_treatment = 'regular'

        if params.get('l10n_in_gst_treatment') == 'Registered Business - Composition':
            l10n_in_gst_treatment = 'composition'
        elif params.get('l10n_in_gst_treatment') == 'Unregistered Business':
            l10n_in_gst_treatment = 'unregistered'
        elif params.get('l10n_in_gst_treatment') == 'Consumer':
            l10n_in_gst_treatment = 'consumer'
        elif params.get('l10n_in_gst_treatment') == 'Overseas':
            l10n_in_gst_treatment = 'overseas'
        elif params.get('l10n_in_gst_treatment') == 'Special Economic Zone':
            l10n_in_gst_treatment = 'special_economic_zone'
        elif params.get('l10n_in_gst_treatment') == 'Deemed Export':
            l10n_in_gst_treatment = 'deemed_export'
        elif params.get('l10n_in_gst_treatment') == 'UIN Holders':
            l10n_in_gst_treatment = 'uin_holders'

        advertisement_language = ""
        if params.get('advertisement_language') == 'Telugu':
            advertisement_language = 'telugu'
        elif params.get('advertisement_language') == 'English':
            advertisement_language = 'english'
        elif params.get('advertisement_language') == 'Both':
            advertisement_language = 'both'

        cust_order_line = []
        related_order_lines = []
        advertisement_order_line = []
        order_line_vals = params.get('line_orders')
        related_docs = params.get('related_documents_list')
        advertisement_line = params.get('advertisement_line_ids')

        for advertisement in advertisement_line:
            advertisement_order_line.append((0, 0, {
                'advertisement_description': str(advertisement['advertisement_description']),
                'no_of_characters': int(advertisement['no_of_characters']),
                'no_of_lines': int(advertisement['no_of_lines'])
            }))

        for docs in related_docs:
            related_order_lines.append((0, 0, {
                'name': docs['doc_id'],
                'related_document': docs['related_document']
            }))

        if params.get('is_online') == False:
            if params.get('partner_id') == 0:
                res_partner_obj = self.env['res.partner'].search([('cust_seq', '=', str(params.get('partner_code')))],
                                                                 limit=1)
                partner_obj = res_partner_obj.id
            else:
                partner_obj = params.get('partner_id')
        else:
            partner_obj = params.get('partner_id')

        phone_number = self.env['res.partner'].browse(params.get('partner_id'))

        for products in order_line_vals:
            publication_lines = []
            order_publication_lines = products['publication_line_list']
            for pub_line in order_publication_lines:
                publication_lines.append((0, 0, {
                    'publication_id': pub_line['publication_id'],
                    'publication_region_ids': pub_line['region_ids']
                }))

            cust_order_line.append((0, 0, {
                'product_template_id': products['product_id'],
                'product_id': products['product_varients_id'],
                'name': advertisement['advertisement_description'],
                'size': products['size'],
                'page': products['page_id'],
                'ad_position': products['ad_position_id'],
                'product_pricelist_id': products['pricelist_id'],
                'product_uom_qty': products['product_uom_qty'],
                "price_unit": products['price_unit'],
                'tax_id': products['tax_id'],
                'discount': products['discount'],
                'product_uom': products['product_uom_id'],
                'main_category': products['main_category_id'],
                'sub_category': products['sub_category_id'],
                'main_area': products['main_area_id'],
                'sub_area': products['sub_area_id'],
                'packages': products['package_id'],
                'publication_line_ids': publication_lines
            }))

        if scheduling_date == 'specific_date':
            customer_val = {
                'classified_bool_field': True,
                'l10n_in_gst_treatment': l10n_in_gst_treatment,
                'cio_paid_amount': params.get('cio_paid_amount'),
                'cio_amount_due': params.get('cio_amount_due'),
                'amount_untaxed': params.get('amount_untaxed'),
                'amount_tax': params.get('amount_tax'),
                'amount_total': params.get('amount_total'),
                'is_online': params.get('is_online'),
                'partner_id': partner_obj,
                'phone_number': phone_number.mobile,
                # 'packages': params.get('package_id'),
                'agent_name': params.get('agent_id'),
                'publication_id': params.get('publication_id'),
                # 'reta_order_line': cust_order_line,
                'scheduling_date': scheduling_date,
                'specific_date': params.get('specific_date'),
                'mob_seq_number': params.get('mob_seq_number'),
                'mob_seq_id': params.get('mob_seq_id'),
                'sale_related_document_ids': related_order_lines,
                'advertisement_language': advertisement_language,
                'advertisement_line_ids': advertisement_order_line,
                'is_sthirasthi': params.get('is_sthirasthi'),
                'is_created_from_app': True
            }
        else:
            customer_val = {
                'classified_bool_field': True,
                'agent_name': params.get('agent_id'),
                'l10n_in_gst_treatment': l10n_in_gst_treatment,
                'cio_paid_amount': params.get('cio_paid_amount'),
                'cio_amount_due': params.get('cio_amount_due'),
                'amount_untaxed': params.get('amount_untaxed'),
                'amount_tax': params.get('amount_tax'),
                'amount_total': params.get('amount_total'),
                'is_online': params.get('is_online'),
                'partner_id': partner_obj,
                'phone_number': phone_number.mobile,
                # 'packages': params.get('package_id'),
                # 'reta_order_line': cust_order_line,
                'scheduling_date': scheduling_date,
                'from_date': params.get('from_date'),
                'to_date': params.get('to_date'),
                'publish_start_date': params.get('publish_start_date'),
                'no_of_occurence': params.get('no_of_occurence'),
                'time_interval': params.get('time_interval'),
                'mob_seq_number': params.get('mob_seq_number'),
                'publication_id': params.get('publication_id'),
                'mob_seq_id': params.get('mob_seq_id'),
                'sale_related_document_ids': related_order_lines,
                'advertisement_language': advertisement_language,
                'advertisement_line_ids': advertisement_order_line,
                'is_sthirasthi': params.get('is_sthirasthi'),
                'is_created_from_app': True
            }

        quotation_obj = self.env['sale.order'].search(
            [('mob_seq_number', '=', params.get('mob_seq_number'))])
        if quotation_obj:
            return {
                'Status': "Record already Created!",
                'CIO Reference': quotation_obj.custom_seq,
                'id': quotation_obj.id
            }
        else:
            quotation = self.env['sale.order'].create(customer_val)
            quotation.reta_order_line = cust_order_line
            return {"id": quotation.id, "Status": "Success", "CIO Reference": quotation.custom_seq,
                    "Number": quotation.name}

    @restapi.method([(["/cio_to_scheduling"], "POST")], auth="user")
    def cio_to_scheduling(self):
        params = request.params
        sale_order_obj = self.env['sale.order'].sudo().browse(int(params.get('id')))
        sale_order_obj.sudo().send_for_scheduling()

        return "Success"

    @restapi.method([(["/scheduling_to_confirm"], "POST")], auth="user")
    def scheduling_to_confirm(self):
        params = request.params
        sale_order_obj = self.env['sale.order'].sudo().browse(int(params.get('id')))
        if params.get('is_terms_and_conditions') == True:
            sale_order_obj.is_terms_and_conditions = True
        if params.get('is_consent_form') == True:
            sale_order_obj.is_consent_form = True
        sale_order_obj.sudo().action_confirm()

        return "Success"

    @restapi.method([(["/update_cio"], "POST")], auth="user")
    def update_cio(self):
        params = request.params
        so_order_obj = self.env['sale.order'].browse(params.get('id'))
        order_line_vals = params.get('line_orders')
        advertisement_line_vals = params.get('advertisement_line_ids')
        related_docs = params.get('related_documents_list')

        for docs in related_docs:
            docs_line_obj = self.env['sale.related.documents'].browse(docs['id'])
            if docs['id'] != 0:
                docs_line_obj.name = docs['doc_id']
                docs_line_obj.related_document = docs['related_document']
            elif docs['id'] == 0:
                create_docs_line_obj = self.env['sale.related.documents'].sudo().create({
                    'sale_related_document_id': params.get('id'),
                    'name': docs['doc_id'],
                    'related_document': docs['related_document']
                })

        for advertisement_line in advertisement_line_vals:
            adv_line_obj = self.env['advertisement.content.line'].browse(advertisement_line['id'])
            if advertisement_line['id'] != 0:
                adv_line_obj.advertisement_description = advertisement_line['advertisement_description']
                adv_line_obj.no_of_characters = advertisement_line['no_of_characters']
                adv_line_obj.no_of_lines = advertisement_line['no_of_lines']
            elif advertisement_line['id'] == 0:
                create_advertisement_line_obj = self.env['advertisement.content.line'].create({
                    'advertisement_line_id': params.get('id'),
                    'advertisement_description': str(advertisement_line['advertisement_description']),
                    'no_of_characters': int(advertisement_line['no_of_characters']),
                    'no_of_lines': int(advertisement_line['no_of_lines'])
                })



        for order_line in order_line_vals:

            sale_type = ''
            if order_line['sale_type'] == 'Main':
                sale_type += 'main'
            elif order_line['sale_type'] == 'Mini':
                sale_type += 'mini'

            order_line_obj = self.env['sale.order.line'].browse(order_line['id'])
            if order_line['id'] != 0:
                order_line_obj.product_id = order_line['product_varients_id']
                order_line_obj.product_template_id = order_line['product_id']
                order_line_obj.name = order_line['description']
                order_line_obj.size = order_line['size']
                order_line_obj.page = order_line['page_id']
                order_line_obj.ad_position = order_line['ad_position_id']
                order_line_obj.product_pricelist_id = order_line['pricelist_id']
                order_line_obj.product_uom_qty = order_line['product_uom_qty']
                order_line_obj.product_uom = order_line['product_uom_id']
                order_line_obj.price_unit = order_line['price_unit']
                order_line_obj.tax_id = order_line['tax_id']
                order_line_obj.discount = order_line['discount']
                order_line_obj.main_category = order_line['main_category_id']
                order_line_obj.sub_category = order_line['sub_category_id']
                order_line_obj.main_area = order_line['main_area_id']
                order_line_obj.sub_area = order_line['sub_area_id']
                order_line_obj.packages = order_line['package_id']
                order_line_obj.sale_type = order_line['sale_type']

                if order_line['publication_line_list']:
                    for publication_line in order_line['publication_line_list']:
                        publication_line_obj = self.env['publication.line'].browse(publication_line['id'])
                        if publication_line['id'] != 0:
                            publication_line_obj.publication_id = publication_line['publication_id']
                            publication_line_obj.publication_region_ids = publication_line['region_ids']
                        else:
                            create_publication_line_obj = self.env['publication.line'].create({
                                'publication_id': publication_line['publication_id'],
                                'publication_region_ids': publication_line['region_ids'],
                                'publication_line_id': order_line['id']
                            })

            elif order_line['id'] == 0:
                publication_lines_list = []
                if order_line['publication_line_list']:
                    for publication_line in order_line['publication_line_list']:
                        publication_lines_list.append((0, 0, {
                            'publication_id': publication_line['publication_id'],
                            'publication_region_ids': publication_line['region_ids']
                        }))


                cust_order_line = []
                cust_order_line.append({
                    'order_id': so_order_obj.id,
                    'product_template_id': order_line['product_id'],
                    'product_id': order_line['product_varients_id'],
                    'name': order_line['description'],
                    'size': order_line['size'],
                    'page': order_line['page_id'],
                    'ad_position': order_line['ad_position_id'],
                    'product_pricelist_id': order_line['pricelist_id'],
                    'product_uom_qty': order_line['product_uom_qty'],
                    "price_unit": order_line['price_unit'],
                    'tax_id': order_line['tax_id'],
                    'discount': order_line['discount'],
                    'product_uom': order_line['product_uom_id'],
                    'main_category': order_line['main_category_id'],
                    'sub_category': order_line['sub_category_id'],
                    'main_area': order_line['main_area_id'],
                    'sub_area': order_line['sub_area_id'],
                    'packages': order_line['package_id'],
                    'sale_type': sale_type,
                    'publication_line_ids': publication_lines_list
                })
                order_line_create_obj = self.env['sale.order.line'].create(cust_order_line)

        if params.get('scheduling_date') == 'Specific Date':
            scheduling_date = 'specific_date'
        else:
            scheduling_date = 'multiple_date'

        if params.get('l10n_in_gst_treatment') == 'Registered Business - Regular':
            l10n_in_gst_treatment = 'regular'
        elif params.get('l10n_in_gst_treatment') == 'Registered Business - Composition':
            l10n_in_gst_treatment = 'composition'
        elif params.get('l10n_in_gst_treatment') == 'Unregistered Business':
            l10n_in_gst_treatment = 'unregistered'
        elif params.get('l10n_in_gst_treatment') == 'Consumer':
            l10n_in_gst_treatment = 'consumer'
        elif params.get('l10n_in_gst_treatment') == 'Overseas':
            l10n_in_gst_treatment = 'overseas'
        elif params.get('l10n_in_gst_treatment') == 'Special Economic Zone':
            l10n_in_gst_treatment = 'special_economic_zone'
        elif params.get('l10n_in_gst_treatment') == 'Deemed Export':
            l10n_in_gst_treatment = 'deemed_export'
        elif params.get('l10n_in_gst_treatment') == 'UIN Holders':
            l10n_in_gst_treatment = 'uin_holders'
        else:
            l10n_in_gst_treatment = ''

        if params.get('advertisement_language') == 'Telugu':
            advertisement_language = 'telugu'
        elif params.get('advertisement_language') == 'English':
            advertisement_language = 'english'
        elif params.get('advertisement_language') == 'Both':
            advertisement_language = 'english_telugu'
        else:
            advertisement_language = ''

        so_order_obj.partner_id = params.get('partner_id')
        so_order_obj.agent_name = params.get('agent_id')
        so_order_obj.scheduling_date = scheduling_date
        so_order_obj.specific_date = params.get('specific_date')
        so_order_obj.from_date = params.get('from_date')
        so_order_obj.to_date = params.get('to_date')
        so_order_obj.publication_id = params.get('publication_id')
        so_order_obj.l10n_in_gst_treatment = l10n_in_gst_treatment
        so_order_obj.publish_start_date = params.get('publish_start_date')
        so_order_obj.no_of_occurence = params.get('no_of_occurence')
        so_order_obj.time_interval = params.get('time_interval')
        so_order_obj.packages = params.get('package_id')
        so_order_obj.phone_number = params.get('mobile_number')
        so_order_obj.is_sthirasthi = params.get('is_sthirasthi')
        so_order_obj.advertisement_language = advertisement_language

        if params.get('id'):
            return {"Status": "Success"}

    @restapi.method([(["/classified_management"], "GET")], auth="user")
    def classified_management(self):
        total_value = 0.0
        classified_order_cio_obj = self.env['sale.order'].search([('classified_bool_field', '=', True),
                                                                  ('classified_state', '=', 'draft')])
        for cio in classified_order_cio_obj:
            total_value += cio.amount_total
        total_value_ro = 0.0
        classified_order_ro_obj = self.env['sale.order'].search(
            [('classified_bool_field', '=', True), ('classified_state', '=', 'sale')])
        for ro in classified_order_ro_obj:
            total_value_ro += ro.amount_total

        pending_payment = 0.0
        payment_collected = 0.0
        classified_payment_obj = self.env['sale.order'].search(
            [('classified_bool_field', '=', True), ('classified_state', '!=', 'cancel')])
        for payment in classified_payment_obj:
            pending_payment += payment.cio_paid_amount
            payment_collected += payment.cio_amount_due

        unit_target_incentive_lines = []
        unit_master_obj = self.env['unit.master'].search([])
        for unit in unit_master_obj:
            target_amount = 0.0
            ro_value = 0.0
            collections = 0.0
            partner_incentive_obj = self.env['partner.incentive'].search([('unit_name', '=', unit.id),
                                                                          ('classified', '=', True)])
            for incentive in partner_incentive_obj:
                for line in incentive.incentive_line:
                    target_amount += line.target_amt
                    ro_value += line.so_total_amt
                    collections += line.recieved_payment
            if target_amount != 0.00:
                progress = round(collections / target_amount * 100)
            else:
                progress = 0

            unit_target_incentive_lines.append({
                'unit_name': unit.name,
                'target_amount': target_amount,
                'ro_value': ro_value,
                'collections': collections,
                'progress': progress
            })

        unit_top_cio_lines = []
        unit_master_obj = self.env['unit.master'].search([])
        for unit in unit_master_obj:
            cio_value = 0.0
            ro_value = 0.0
            top_cio_collections = 0.0
            partner_incentive_obj = self.env['sale.order'].search([('classified_bool_field', '=', True),
                                                                   ('classified_state', '=', 'draft'),
                                                                   ('agent_name.unit', '=', unit.id)])
            for incentive in partner_incentive_obj:
                cio_value += incentive.amount_total
                top_cio_collections += incentive.cio_paid_amount
            if cio_value != 0.00:
                top_cio_progress = round(top_cio_collections / cio_value * 100)
            else:
                top_cio_progress = 0

            unit_top_cio_lines.append({
                'unit_name': unit.name,
                'cio_value': cio_value,
                'top_cio_collections': top_cio_collections,
                'progress': top_cio_progress
            })

        return {
            'issued_cio': len(classified_order_cio_obj),
            'total_value_cio': "{0:.2f}".format(total_value),
            'received_ro': len(classified_order_ro_obj),
            'total_value_ro': "{0:.2f}".format(total_value_ro),
            'pending_payment': "{0:.2f}".format(pending_payment),
            'payment_collected': "{0:.2f}".format(payment_collected),
            'unit_target_incentive_lines': unit_target_incentive_lines,
            'unit_top_cio_lines': unit_top_cio_lines
        }
