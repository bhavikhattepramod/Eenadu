from odoo.http import request, root
from odoo.service import security
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component

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
    _name = "partner.new_api.service.circulation_payment"
    _usage = "circulation_payment"
    _collection = "base_rest_auth_user_service.services"
    _description = """ """

    @restapi.method([(["/cash"], "POST")], auth="public")
    def circulation_cash(self):
        params = request.params
        if params.get('payment_mode') == 'Cash':
            payment_mode = 'cash'
        elif params.get('payment_mode') == 'UPI/QR':
            payment_mode = 'upi'
        elif params.get('payment_mode') == 'Bank - NEFT':
            payment_mode = 'bank'
        elif params.get('payment_mode') == 'Cheque':
            payment_mode = 'pdc'
        else:
            payment_mode = ''

        if params.get('payment_type') == 'Full Payment':
            payment_type = 'full'
        elif params.get('payment_type') == 'Partial Payment':
            payment_type = 'partial'
        else:
            payment_type = ''

        payment_obj = self.env['account.move'].browse(params.get('id'))

        if params.get('payment_type') == 'Full Payment':
            payment_obj.payment_state = 'in_payment'
        elif params.get('payment_type') == 'Partial Payment':
            payment_obj.payment_state = 'partial'

        payment_info_create_obj = self.env['payment.informations.invoice'].create({
            'payment_type': payment_type,
            'payment_mode': payment_mode,
            'payee_name': params.get('payee_name'),
            'payee_mobile': params.get('payee_mobile'),
            'payment_amount': params.get('payment_amount'),
            'agent_id': params.get('agent_id'),
            'payment_confirmation_file': params.get('payment_confirmation_file'),
            'payment_datetime': params.get('payment_datetime'),
            'payment_location': params.get('payment_location'),
            'invoice_id': payment_obj.id
        })


        payment_obj.payment_details += payment_info_create_obj

        payment_values = {
            'payment_type': 'inbound',
            'partner_id': payment_obj.partner_id.id,
            'amount': params.get('payment_amount'),
        }

        new_payment_obj = self.env['account.payment'].create(payment_values)

        new_payment_obj.action_post()

        if new_payment_obj:
            return {
                "id": payment_info_create_obj.id,
                "Status": "Success"
            }

    @restapi.method([(["/upi"], "POST")], auth="public")
    def circulation_upi(self):
        params = request.params
        if params.get('payment_mode') == 'Cash':
            payment_mode = 'cash'
        elif params.get('payment_mode') == 'UPI/QR':
            payment_mode = 'upi'
        elif params.get('payment_mode') == 'Bank - NEFT':
            payment_mode = 'bank'
        elif params.get('payment_mode') == 'Cheque':
            payment_mode = 'pdc'
        else:
            payment_mode = ''

        if params.get('payment_type') == 'Full Payment':
            payment_type = 'full'
        elif params.get('payment_type') == 'Partial Payment':
            payment_type = 'partial'
        else:
            payment_type = ''

        payment_obj = self.env['account.move'].browse(params.get('id'))

        if params.get('payment_type') == 'Full Payment':
            payment_obj.payment_state = 'in_payment'
        elif params.get('payment_type') == 'Partial Payment':
            payment_obj.payment_state = 'partial'

        payment_info_create_obj = self.env['payment.informations.invoice'].create({
            'payment_type': payment_type,
            'payment_mode': payment_mode,
            'payee_name': params.get('payee_name'),
            'payee_mobile': params.get('payee_mobile'),
            'payment_amount': params.get('payment_amount'),
            'agent_id': params.get('agent_id'),
            'payment_datetime': params.get('payment_datetime'),
            'payment_location': params.get('payment_location'),
            'payment_confirmation_file': params.get('payment_confirmation_file'),
            'sender_acc_no': params.get('sender_acc_no'),
            'tnx_id': params.get('tnx_id'),
            'utr_no': params.get('utr_no'),
            'invoice_id': payment_obj.id
        })

        payment_obj.payment_details += payment_info_create_obj

        payment_values = {
            'payment_type': 'inbound',
            'partner_id': payment_obj.partner_id.id,
            'amount': params.get('payment_amount'),
        }

        new_payment_obj = self.env['account.payment'].create(payment_values)

        new_payment_obj.action_post()

        if new_payment_obj:
            return {
                "id": payment_info_create_obj.id,
                "Status": "Success"
            }

    @restapi.method([(["/neft"], "POST")], auth="public")
    def circulation_neft(self):
        params = request.params
        if params.get('payment_mode') == 'Cash':
            payment_mode = 'cash'
        elif params.get('payment_mode') == 'UPI/QR':
            payment_mode = 'upi'
        elif params.get('payment_mode') == 'Bank - NEFT':
            payment_mode = 'bank'
        elif params.get('payment_mode') == 'Cheque':
            payment_mode = 'pdc'
        else:
            payment_mode = ''

        if params.get('payment_type') == 'Full Payment':
            payment_type = 'full'
        elif params.get('payment_type') == 'Partial Payment':
            payment_type = 'partial'
        else:
            payment_type = ''

        payment_obj = self.env['account.move'].browse(params.get('id'))

        if params.get('payment_type') == 'Full Payment':
            payment_obj.payment_state = 'in_payment'
        elif params.get('payment_type') == 'Partial Payment':
            payment_obj.payment_state = 'partial'

        payment_info_create_obj = self.env['payment.informations.invoice'].create({
            'payment_type': payment_type,
            'payment_mode': payment_mode,
            'payee_name': params.get('payee_name'),
            'payee_mobile': params.get('payee_mobile'),
            'payment_amount': params.get('payment_amount'),
            'agent_id': params.get('agent_id'),
            'payment_confirmation_file': params.get('payment_confirmation_file'),
            'payment_datetime': params.get('payment_datetime'),
            'payment_location': params.get('payment_location'),
            'sender_acc_no': params.get('sender_acc_no'),
            'tnx_id': params.get('tnx_id'),
            'utr_no': params.get('utr_no'),
            'invoice_id': payment_obj.id
        })

        payment_obj.payment_details += payment_info_create_obj

        payment_values = {
            'payment_type': 'inbound',
            'partner_id': payment_obj.partner_id.id,
            'amount': params.get('payment_amount'),
        }

        new_payment_obj = self.env['account.payment'].create(payment_values)

        new_payment_obj.action_post()

        if new_payment_obj:
            return {
                "id": payment_info_create_obj.id,
                "Status": "Success"
            }

    @restapi.method([(["/pdc"], "POST")], auth="public")
    def circulation_pdc(self):
        params = request.params
        if params.get('payment_mode') == 'Cash':
            payment_mode = 'cash'
        elif params.get('payment_mode') == 'UPI/QR':
            payment_mode = 'upi'
        elif params.get('payment_mode') == 'Bank - NEFT':
            payment_mode = 'bank'
        elif params.get('payment_mode') == 'Cheque':
            payment_mode = 'pdc'
        else:
            payment_mode = ''

        if params.get('payment_type') == 'Full Payment':
            payment_type = 'full'
        elif params.get('payment_type') == 'Partial Payment':
            payment_type = 'partial'
        else:
            payment_type = ''

        payment_obj = self.env['account.move'].browse(params.get('id'))

        if params.get('payment_type') == 'Full Payment':
            payment_obj.payment_state = 'in_payment'
        elif params.get('payment_type') == 'Partial Payment':
            payment_obj.payment_state = 'partial'

        payment_info_create_obj = self.env['payment.informations.invoice'].create({
            'payment_type': payment_type,
            'payment_mode': payment_mode,
            'payee_name': params.get('payee_name'),
            'payee_mobile': params.get('payee_mobile'),
            'payment_amount': params.get('payment_amount'),
            'agent_id': params.get('agent_id'),
            'payment_confirmation_file': params.get('payment_confirmation_file'),
            'payment_datetime': params.get('payment_datetime'),
            'payment_location': params.get('payment_location'),
            'sender_acc_no': params.get('sender_acc_no'),
            'tnx_id': params.get('tnx_id'),
            'utr_no': params.get('utr_no'),
            'invoice_id': payment_obj.id
        })

        payment_obj.payment_details += payment_info_create_obj

        payment_values = {
            'payment_type': 'inbound',
            'partner_id': payment_obj.partner_id.id,
            'amount': params.get('payment_amount'),
        }

        new_payment_obj = self.env['account.payment'].create(payment_values)

        new_payment_obj.action_post()

        if new_payment_obj:
            return {
                "id": payment_info_create_obj.id,
                "Status": "Success"
            }
