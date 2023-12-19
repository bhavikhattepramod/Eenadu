from odoo.http import request, root
from odoo.service import security
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
from odoo.fields import Command

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
    _name = "partner.new_api.service.payment"
    _usage = "payment"
    _collection = "base_rest_auth_user_service.services"
    _description = """ """

    @restapi.method([(["/cash"], "POST")], auth="public")
    def cash(self):
        params = request.params
        if params.get('payment_mode') == 'Cash':
            payment_mode = 'cash'
        elif params.get('payment_mode') == 'UPI/QR':
            payment_mode = 'upi'
        elif params.get('payment_mode') == 'Bank - NEFT':
            payment_mode = 'bank'
        elif params.get('payment_mode') == 'Cheque':
            payment_mode = 'pdc'

        if params.get('payment_type') == 'Full Payment':
            payment_type = 'full'
        elif params.get('payment_type') == 'Partial Payment':
            payment_type = 'partial'

        so_obj = self.env['sale.order'].browse(params.get('order_id'))
        if so_obj.cio_paid_amount == 0.00:
            inv_line = []
            for line in so_obj.reta_order_line:
                inv_line.append((0, 0, {
                    'display_type': line.display_type or 'product',
                    'sequence': line.sequence,
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom.id,
                    'quantity': line.product_uom_qty,
                    'discount': line.discount,
                    'price_unit': line.price_unit,
                    'tax_ids': [Command.set(line.tax_id.ids)],
                    'sale_line_ids': [Command.link(line.id)],
                    'is_downpayment': line.is_downpayment,
                }))
            create_values = {
                'ref': so_obj.client_order_ref or '',
                'move_type': 'out_invoice',
                'narration': so_obj.note,
                'currency_id': so_obj.currency_id.id,
                'campaign_id': so_obj.campaign_id.id,
                'medium_id': so_obj.medium_id.id,
                'source_id': so_obj.source_id.id,
                'team_id': so_obj.team_id.id,
                'partner_id': so_obj.partner_invoice_id.id,
                'partner_shipping_id': so_obj.partner_shipping_id.id,
                'fiscal_position_id': (
                        so_obj.fiscal_position_id or so_obj.fiscal_position_id._get_fiscal_position(
                    so_obj.partner_invoice_id)).id,
                'invoice_origin': so_obj.name,
                'invoice_payment_term_id': so_obj.payment_term_id.id,
                'invoice_user_id': so_obj.user_id.id,
                'payment_reference': so_obj.reference,
                'transaction_ids': [Command.set(so_obj.transaction_ids.ids)],
                'company_id': so_obj.company_id.id,
                'reta_bool_field': True,
                'invoice_line_ids': inv_line
            }
            new_inv_obj = self.env['account.move'].create(create_values)
            new_inv_obj.action_post()
            payment_values = {
                'payment_type': 'inbound',
                'partner_id': so_obj.partner_id.id,
                'amount': params.get('payment_amount'),
                'company_id': so_obj.company_id.id,
                'sale_order_id': so_obj.id,
            }
            new_payment_obj = self.env['account.payment'].create(payment_values)
            new_payment_obj.action_post()
        else:
            payment_values = {
                'payment_type': 'inbound',
                'partner_id': so_obj.partner_id.id,
                'amount': params.get('payment_amount'),
                'company_id': so_obj.company_id.id,
                'sale_order_id': so_obj.id,
            }
            new_payment_obj = self.env['account.payment'].create(payment_values)
            new_payment_obj.action_post()

        so_obj.cio_paid_amount += params.get('payment_amount')

        payment_info_create_obj = self.env['payment.informations'].create({
                'payment_type' : payment_type,
                'payment_mode' : payment_mode,
                'payee_name' : params.get('payee_name'),
                'payee_mobile' : params.get('payee_mobile'),
                'payment_amount' : params.get('payment_amount'),
                'agent_id' : params.get('agent_id'),
                'payment_confirmation_file' : params.get('payment_confirmation_file'),
                'payment_datetime' : params.get('payment_datetime'),
                'payment_location' : params.get('payment_location'),
                'payment_information_id' : so_obj.id
            })

        if new_payment_obj:
            return {
                "Status": "Success"
            }

    @restapi.method([(["/upi"], "POST")], auth="public")
    def upi(self):

        params = request.params
        if params.get('payment_mode') == 'Cash':
            payment_mode = 'cash'
        elif params.get('payment_mode') == 'UPI/QR':
            payment_mode = 'upi'
        elif params.get('payment_mode') == 'Bank - NEFT':
            payment_mode = 'bank'
        elif params.get('payment_mode') == 'Cheque':
            payment_mode = 'pdc'

        payment_media = ''
        if params.get('payment_media') == 'Google Pay':
            payment_media = 'gpay'
        elif params.get('payment_media') == 'Phonepe':
            payment_media = 'phonepe'
        elif params.get('payment_media') == 'Paytm':
            payment_media = 'paytm'
        elif params.get('payment_media') == 'UPI':
            payment_media = 'upi'

        so_obj = self.env['sale.order'].browse(params.get('order_id'))
        if so_obj.cio_paid_amount == 0.00:
            inv_line = []
            for line in so_obj.reta_order_line:
                inv_line.append((0, 0, {
                    'display_type': line.display_type or 'product',
                    'sequence': line.sequence,
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom.id,
                    'quantity': line.product_uom_qty,
                    'discount': line.discount,
                    'price_unit': line.price_unit,
                    'tax_ids': [Command.set(line.tax_id.ids)],
                    'sale_line_ids': [Command.link(line.id)],
                    'is_downpayment': line.is_downpayment,
                }))
            create_values = {
                'ref': so_obj.client_order_ref or '',
                'move_type': 'out_invoice',
                'narration': so_obj.note,
                'currency_id': so_obj.currency_id.id,
                'campaign_id': so_obj.campaign_id.id,
                'medium_id': so_obj.medium_id.id,
                'source_id': so_obj.source_id.id,
                'team_id': so_obj.team_id.id,
                'partner_id': so_obj.partner_invoice_id.id,
                'partner_shipping_id': so_obj.partner_shipping_id.id,
                'fiscal_position_id': (
                        so_obj.fiscal_position_id or so_obj.fiscal_position_id._get_fiscal_position(
                    so_obj.partner_invoice_id)).id,
                'invoice_origin': so_obj.name,
                'invoice_payment_term_id': so_obj.payment_term_id.id,
                'invoice_user_id': so_obj.user_id.id,
                'payment_reference': so_obj.reference,
                'transaction_ids': [Command.set(so_obj.transaction_ids.ids)],
                'company_id': so_obj.company_id.id,
                'reta_bool_field': True,
                'invoice_line_ids': inv_line
            }
            new_inv_obj = self.env['account.move'].create(create_values)
            new_inv_obj.action_post()
            payment_values = {
                'payment_type': 'inbound',
                'partner_id': so_obj.partner_id.id,
                'amount': params.get('payment_amount'),
                'company_id': so_obj.company_id.id,
                'sale_order_id': so_obj.id,
            }
            new_payment_obj = self.env['account.payment'].create(payment_values)
            new_payment_obj.action_post()
        else:
            payment_values = {
                'payment_type': 'inbound',
                'partner_id': so_obj.partner_id.id,
                'amount': params.get('payment_amount'),
                'company_id': so_obj.company_id.id,
                'sale_order_id': so_obj.id,
            }
            new_payment_obj = self.env['account.payment'].create(payment_values)
            new_payment_obj.action_post()

        so_obj.cio_paid_amount += params.get('payment_amount')

        if params.get('payment_type') == 'Full Payment':
            payment_type = 'full'
        elif params.get('payment_type') == 'Partial Payment':
            payment_type = 'partial'

        payment_info_create_obj = self.env['payment.informations'].create({
            'payment_type' : payment_type,
            'payment_mode' : payment_mode,
            'payee_name' : params.get('payee_name'),
            'payee_mobile' : params.get('payee_mobile'),
            'payment_amount' : params.get('payment_amount'),
            'agent_id' : params.get('agent_id'),
            'payment_confirmation_file' : params.get('payment_confirmation_file'),
            'payment_datetime' : params.get('payment_datetime'),
            'payment_location' : params.get('payment_location'),
            'sender_acc_no' : params.get('sender_acc_no'),
            'tnx_id' : params.get('tnx_id'),
            'payment_media' : payment_media,
            'utr_no' : params.get('utr_no'),
            'payment_information_id' : so_obj.id
        })

        if new_payment_obj:
            return {
                "Status": "Success"
            }

    @restapi.method([(["/neft"], "POST")], auth="public")
    def neft(self):
        params = request.params
        if params.get('payment_mode') == 'Cash':
            payment_mode = 'cash'
        elif params.get('payment_mode') == 'UPI/QR':
            payment_mode = 'upi'
        elif params.get('payment_mode') == 'Bank - NEFT':
            payment_mode = 'bank'
        elif params.get('payment_mode') == 'Cheque':
            payment_mode = 'pdc'

        so_obj = self.env['sale.order'].browse(params.get('order_id'))
        if so_obj.cio_paid_amount == 0.00:
            inv_line = []
            for line in so_obj.reta_order_line:
                inv_line.append((0, 0, {
                    'display_type': line.display_type or 'product',
                    'sequence': line.sequence,
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom.id,
                    'quantity': line.product_uom_qty,
                    'discount': line.discount,
                    'price_unit': line.price_unit,
                    'tax_ids': [Command.set(line.tax_id.ids)],
                    'sale_line_ids': [Command.link(line.id)],
                    'is_downpayment': line.is_downpayment,
                }))
            create_values = {
                'ref': so_obj.client_order_ref or '',
                'move_type': 'out_invoice',
                'narration': so_obj.note,
                'currency_id': so_obj.currency_id.id,
                'campaign_id': so_obj.campaign_id.id,
                'medium_id': so_obj.medium_id.id,
                'source_id': so_obj.source_id.id,
                'team_id': so_obj.team_id.id,
                'partner_id': so_obj.partner_invoice_id.id,
                'partner_shipping_id': so_obj.partner_shipping_id.id,
                'fiscal_position_id': (
                        so_obj.fiscal_position_id or so_obj.fiscal_position_id._get_fiscal_position(
                    so_obj.partner_invoice_id)).id,
                'invoice_origin': so_obj.name,
                'invoice_payment_term_id': so_obj.payment_term_id.id,
                'invoice_user_id': so_obj.user_id.id,
                'payment_reference': so_obj.reference,
                'transaction_ids': [Command.set(so_obj.transaction_ids.ids)],
                'company_id': so_obj.company_id.id,
                'reta_bool_field': True,
                'invoice_line_ids': inv_line
            }
            new_inv_obj = self.env['account.move'].create(create_values)
            new_inv_obj.action_post()
            payment_values = {
                'payment_type': 'inbound',
                'partner_id': so_obj.partner_id.id,
                'amount': params.get('payment_amount'),
                'company_id': so_obj.company_id.id,
                'sale_order_id': so_obj.id,
            }
            new_payment_obj = self.env['account.payment'].create(payment_values)
            new_payment_obj.action_post()
        else:
            payment_values = {
                'payment_type': 'inbound',
                'partner_id': so_obj.partner_id.id,
                'amount': params.get('payment_amount'),
                'company_id': so_obj.company_id.id,
                'sale_order_id': so_obj.id,
            }
            new_payment_obj = self.env['account.payment'].create(payment_values)
            new_payment_obj.action_post()


        so_obj.cio_paid_amount += params.get('payment_amount')

        if params.get('payment_type') == 'Full Payment':
            payment_type = 'full'
        elif params.get('payment_type') == 'Partial Payment':
            payment_type = 'partial'

        payment_info_create_obj = self.env['payment.informations'].create({
            'payment_type' : payment_type,
            'payment_mode' : payment_mode,
            'payee_name' : params.get('payee_name'),
            'payee_mobile' : params.get('payee_mobile'),
            'payment_amount' : params.get('payment_amount'),
            'agent_id' : params.get('agent_id'),
            'payment_datetime' : params.get('payment_datetime'),
            'payment_location' : params.get('payment_location'),
            'payment_confirmation_file' : params.get('payment_confirmation_file'),
            'sender_acc_no' : params.get('sender_acc_no'),
            'tnx_id' : params.get('tnx_id'),
            'utr_no' : params.get('utr_no'),
            'payment_information_id' : so_obj.id
        })

        if new_payment_obj:
            return {
                "Status": "Success"
            }

    @restapi.method([(["/pdc"], "POST")], auth="public")
    def pdc(self):
        params = request.params
        if params.get('payment_mode') == 'Cash':
            payment_mode = 'cash'
        elif params.get('payment_mode') == 'UPI/QR':
            payment_mode = 'upi'
        elif params.get('payment_mode') == 'Bank - NEFT':
            payment_mode = 'bank'
        elif params.get('payment_mode') == 'Cheque':
            payment_mode = 'pdc'

        so_obj = self.env['sale.order'].browse(params.get('order_id'))
        if so_obj.cio_paid_amount == 0.00:
            inv_line = []
            for line in so_obj.reta_order_line:
                inv_line.append((0, 0, {
                    'display_type': line.display_type or 'product',
                    'sequence': line.sequence,
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom.id,
                    'quantity': line.product_uom_qty,
                    'discount': line.discount,
                    'price_unit': line.price_unit,
                    'tax_ids': [Command.set(line.tax_id.ids)],
                    'sale_line_ids': [Command.link(line.id)],
                    'is_downpayment': line.is_downpayment,
                }))
            create_values = {
                'ref': so_obj.client_order_ref or '',
                'move_type': 'out_invoice',
                'narration': so_obj.note,
                'currency_id': so_obj.currency_id.id,
                'campaign_id': so_obj.campaign_id.id,
                'medium_id': so_obj.medium_id.id,
                'source_id': so_obj.source_id.id,
                'team_id': so_obj.team_id.id,
                'partner_id': so_obj.partner_invoice_id.id,
                'partner_shipping_id': so_obj.partner_shipping_id.id,
                'fiscal_position_id': (
                        so_obj.fiscal_position_id or so_obj.fiscal_position_id._get_fiscal_position(
                    so_obj.partner_invoice_id)).id,
                'invoice_origin': so_obj.name,
                'invoice_payment_term_id': so_obj.payment_term_id.id,
                'invoice_user_id': so_obj.user_id.id,
                'payment_reference': so_obj.reference,
                'transaction_ids': [Command.set(so_obj.transaction_ids.ids)],
                'company_id': so_obj.company_id.id,
                'reta_bool_field': True,
                'invoice_line_ids': inv_line
            }
            new_inv_obj = self.env['account.move'].create(create_values)
            new_inv_obj.action_post()
            payment_values = {
                'payment_type': 'inbound',
                'partner_id': so_obj.partner_id.id,
                'amount': params.get('payment_amount'),
                'company_id': so_obj.company_id.id,
                'sale_order_id': so_obj.id,
            }
            new_payment_obj = self.env['account.payment'].create(payment_values)
            new_payment_obj.action_post()
        else:
            payment_values = {
                'payment_type': 'inbound',
                'partner_id': so_obj.partner_id.id,
                'amount': params.get('payment_amount'),
                'company_id': so_obj.company_id.id,
                'sale_order_id': so_obj.id,
            }
            new_payment_obj = self.env['account.payment'].create(payment_values)
            new_payment_obj.action_post()

        so_obj.cio_paid_amount += params.get('payment_amount')

        if params.get('payment_type') == 'Full Payment':
            payment_type = 'full'
        elif params.get('payment_type') == 'Partial Payment':
            payment_type = 'partial'

        payment_info_create_obj = self.env['payment.informations'].create({
            'payment_type' : payment_type,
            'payment_mode' : payment_mode,
            'payee_name' : params.get('payee_name'),
            'payee_mobile' : params.get('payee_mobile'),
            'payment_amount' : params.get('payment_amount'),
            'agent_id' : params.get('agent_id'),
            'payment_datetime' : params.get('payment_datetime'),
            'payment_location' : params.get('payment_location'),
            'payment_confirmation_file' : params.get('payment_confirmation_file'),
            'bank_name' : params.get('bank_name'),
            'acc_branch_name': params.get('acc_branch_name'),
            'cheque_no': params.get('cheque_no'),
            'cheque_date': params.get('cheque_date'),
            'cheque_expiry_date': params.get('cheque_expiry_date'),
            'payment_information_id': so_obj.id

        })

        if new_payment_obj:
            return {
                "Status": "Success"
            }
            
            
    @restapi.method([(["/invoices"], "GET")], auth="public")
    def invoices(self):

        user_id = self.env.user
        # ('agent_name', '=', user_id.partner_id.id)

        invoice_obj = self.env['account.move'].search([('move_type', '=', 'out_invoice'),('partner_id', '=', user_id.partner_id.id)])
        invoices_list = []

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

            invoices_list.append({
                'id': invoice.id if invoice.id else 0,
                'number': invoice.name if invoice.name else '',
                'name': invoice.invoice_partner_display_name if invoice.invoice_partner_display_name else '',
                'invoice_date': invoice.invoice_date if invoice.invoice_date else '',
                'due_date': invoice.invoice_date_due if invoice.invoice_date_due else '',
                'tax_excluded': invoice.amount_untaxed_signed if invoice.amount_untaxed_signed else 0.0,
                'total_amount': invoice.amount_total_signed if invoice.amount_total_signed else 0.0,
                'payment_status': payment_state,
                'status': invoice_status
            })

        return invoices_list

    @restapi.method([(["/invoices/<rec_id>"], "GET")], auth="public")
    def invoices_id(self, rec_id):

        user_id = self.env.user
        # ('agent_name', '=', user_id.partner_id.id)
        invoice_obj = self.env['account.move'].search(
            [('move_type', '=', 'out_invoice'),('id','=',rec_id)])
        invoices_list = []

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

            invoices_list.append({
                'id': invoice.id if invoice.id else 0,
                'number': invoice.name if invoice.name else '',
                'name': invoice.invoice_partner_display_name if invoice.invoice_partner_display_name else '',
                'invoice_date': invoice.invoice_date if invoice.invoice_date else '',
                'due_date': invoice.invoice_date_due if invoice.invoice_date_due else '',
                'tax_excluded': invoice.amount_untaxed_signed if invoice.amount_untaxed_signed else 0.0,
                'total_amount': invoice.amount_total_signed if invoice.amount_total_signed else 0.0,
                'payment_status': payment_state,
                'status': invoice_status
            })

        return invoices_list


