from odoo import api, fields, models, _
from operator import itemgetter
import random
# from datetime import datetime
import calendar


class RetaManagementDashboard(models.Model):
    _name = 'classified.management.dashboard.data'

    def get_management_product_values(self, user_id):
        user_id = self.env['res.users'].search([('id', '=', int(user_id))])
        background_color1 = []
        border_color1 = []
        background_color2 = []
        border_color2 = []
        period_list = []
        received_payment = []
        target_amount_list = []
        unit_master_obj = self.env['unit.master'].search([])
        for unit in unit_master_obj:
            target_amount = 0.0
            collections = 0.0
            partner_incentive_obj = self.env['partner.incentive'].search([('unit_name', '=', unit.id),
                                                                          ('classified', '=', True)])
            for incentive in partner_incentive_obj:
                for line in incentive.classified_line:
                    target_amount += line.target_amt
                    collections += line.recieved_payment
            if target_amount > 0 or collections > 0:
                period_list.append(unit.name)
                received_payment.append(round(collections, 2))
                target_amount_list.append(round(target_amount, 2))
            for i in range(len(partner_incentive_obj)):
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                rgb_str = "#{:02X}{:02X}{:02X}".format(r, g, b)
                rgba_str = str(rgb_str) + 'ad'
                background_color1.append(str(rgba_str))
                border_color1.append(str(rgba_str))
            for i in range(len(partner_incentive_obj)):
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
            'target_amount': target_amount_list,
            'background_color1': background_color1,
            'border_color1': border_color1,
            'background_color2': background_color2,
            'border_color2': border_color2,
        }

    def get_display_data(self, user_id):
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
                for line in incentive.classified_line:
                    target_amount += line.target_amt
                    ro_value += line.so_total_amt
                    collections += line.recieved_payment
            if target_amount != 0.00:
                progress = round(collections / target_amount * 100)
            else:
                progress = 0

            if target_amount > 0 or ro_value > 0 or collections > 0:
                unit_target_incentive_lines.append({
                    'unit_name': unit.name,
                    'target_amount': round(target_amount, 2),
                    'ro_value': round(ro_value, 2),
                    'collections': round(collections, 2),
                    'progress': progress
                })

        unit_top_cio_lines = []
        unit_top_cio_lines_least = []
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

            if cio_value > 0 or top_cio_collections > 0:
                unit_top_cio_lines.append({
                    'unit_name': unit.name,
                    'cio_value': round(cio_value, 2),
                    'top_cio_collections': round(top_cio_collections, 2),
                    'progress': top_cio_progress
                })
                unit_top_cio_lines_least.append({
                    'unit_name': unit.name,
                    'cio_value': round(cio_value, 2),
                    'top_cio_collections': round(top_cio_collections, 2),
                    'progress': top_cio_progress
                })
        cash = 0.0
        upi_qr = 0.0
        bank_neft = 0.0
        pdc = 0.0
        payment_info = self.env['payment.informations'].search([])
        for pay_mode in payment_info:
            if pay_mode.payment_mode == 'cash':
                cash += pay_mode.payment_amount
            elif pay_mode.payment_mode == 'upi':
                upi_qr += pay_mode.payment_amount
            elif pay_mode.payment_mode == 'bank':
                bank_neft += pay_mode.payment_amount
            elif pay_mode.payment_mode == 'pdc':
                pdc += pay_mode.payment_amount

        # incentive_obj = self.env['partner.incentive.line'].search([('partner_id', '=', user_id.partner_id.id)])

        return {
            'issued_cio': len(classified_order_cio_obj),
            'total_value_cio': "{0:.2f}".format(total_value),
            'received_ro': len(classified_order_ro_obj),
            'total_value_ro': "{0:.2f}".format(total_value_ro),
            'pending_payment': "{0:.2f}".format(pending_payment),
            'payment_collected': "{0:.2f}".format(payment_collected),
            'cash': "{0:.2f}".format(cash),
            'upi_qr': "{0:.2f}".format(upi_qr),
            'bank_neft': "{0:.2f}".format(bank_neft),
            'pdc': "{0:.2f}".format(pdc),
            'unit_target_incentive_lines': unit_target_incentive_lines,
            'unit_top_cio_lines': sorted(unit_top_cio_lines, key=itemgetter('cio_value'), reverse=True),
            'unit_top_cio_lines_least': sorted(unit_top_cio_lines_least, key=itemgetter('cio_value'))
        }


class ManagementDashBoardCio(models.Model):
    _inherit = 'sale.order'

    def classified_management_dashboard_cio(self):
        return {
            'name': _('CIO'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
            'domain': [('classified_bool_field', '=', True),('classified_state', '=', 'draft')],
            'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                      (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

        }

    def classified_management_dashboard_release_orders(self):
        return {
            'name': _('Release Orders'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
            'domain': [('classified_bool_field', '=', True),('classified_state', '=', 'sale')],
            'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                      (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

        }

    def classified_management_dashboard_payment_collections(self):
        return {
            'name': _('Payment Collections'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'context': {'readonly_by_pass': True, 'check_domain': True, 'create': False},
            'domain': [('classified_bool_field', '=', True), ('classified_state', '!=', 'cancel')],
            'views': [(self.env.ref('sale.view_order_form').id or False, 'form'),
                      (self.env.ref('eenadu_reta.reta_tree_view').id or False, 'tree')],

        }
