from odoo.http import request, root
from odoo.service import security
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
import logging
from datetime import datetime, timedelta
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
    _name = "partner.new_api.service.circulation"
    _usage = "circulation"
    _collection = "base_rest_auth_user_service.services"
    _description = """ """

    @restapi.method([(["/create_demand_request"], "POST")], auth="public")
    def create_demand_request(self):
        params = request.params
        user_id = request.env.user

        if params.get('demand_type') == 'Specific date':
            selection_field = "specific_date"
        elif params.get('demand_type') == 'Permanent':
            selection_field = "permanent"
        else:
            selection_field = ''

        if params.get('demand_update_type') == 'Increase Copies':
            selection_update_agent_copies = "increase"
        elif params.get('demand_update_type') == 'Decrease Copies':
            selection_update_agent_copies = "decrease"
        else:
            selection_update_agent_copies = ''

        if params.get('update_demand') == 'Increase of Additional Copies':
            selection_additional_type = "increase_additional"
        elif params.get('update_demand') == 'Decrease of Additional Copies':
            selection_additional_type = "decrease_additional"
        else:
            selection_additional_type = ''

        if params.get('types_of_copies') == 'Agent Copies':
            types_of_copies = "agent"
        elif params.get('types_of_copies') == 'Free Copies':
            types_of_copies = "free"
        elif params.get('types_of_copies') == 'Voucher Copies':
            types_of_copies = "voucher"
        elif params.get('types_of_copies') == 'Promotional Copies':
            types_of_copies = "promotional"
        elif params.get('types_of_copies') == 'Correspondents Copies':
            types_of_copies = "correspondents"
        elif params.get('types_of_copies') == 'Office Copies':
            types_of_copies = "office"
        elif params.get('types_of_copies') == 'Postal Copies':
            types_of_copies = "postal"
        else:
            types_of_copies = ''

        values = {
            'Agent_id': params.get('agent_id'),
            'Agent_copies': user_id.partner_id.n_q_zone,
            'selection_field': selection_field,
            'permanent_date': params.get('permanent_date') if params.get('permanent_date') else datetime.now(),
            'specific_date': params.get('specific_date') if params.get('specific_date') else datetime.now(),
            'selection_update_agent_copies': selection_update_agent_copies,
            'decrease_agent_copies': params.get('decrease_agent_copies'),
            'selection_additional_type': selection_additional_type,
            'decrease_additional_copies': params.get('decrease_additional_copies'),
            'update_agent_copies': params.get('increase_agent_copies'),
            'no_of_additional_copies': params.get('increase_of_additional_copies'),
            'total_copies': params.get('total_copies'),
            'types_of_copies': types_of_copies
        }

        result = request.env['demand.request'].create(values)
        result.state_waiting()

        return {
                "id": result.id,
                "Status": "Success"
            }

    @restapi.method([(["/demand_request_waiting"], "GET")], auth="public")
    def demand_request_waiting(self):
        user_id = request.env.user
        demand_request_obj = self.env['demand.request'].search(
            [('state', '=', 'waiting')])
        demand_list = []
        for waiting in demand_request_obj:

            if waiting.selection_field == 'specific_date':
                selection_field = "Specific date"
            elif waiting.selection_field == 'permanent':
                selection_field = "Permanent"
            else:
                selection_field = ''

            if waiting.selection_update_agent_copies == 'increase':
                selection_update_agent_copies = "Increase Copies"
            elif waiting.selection_update_agent_copies == 'decrease':
                selection_update_agent_copies = "Decrease Copies"
            else:
                selection_update_agent_copies = ''

            if waiting.selection_additional_type == 'increase_additional':
                selection_additional_type = "Increase of Additional Copies"
            elif waiting.selection_additional_type == 'decrease_additional':
                selection_additional_type = "Decrease of Additional Copies"
            else:
                selection_additional_type = ''

            if waiting.types_of_copies == 'agent':
                types_of_copies = "Agent Copies"
            elif waiting.types_of_copies == 'free':
                types_of_copies = "Free Copies"
            elif waiting.types_of_copies == 'voucher':
                types_of_copies = "Voucher Copies"
            elif waiting.types_of_copies == 'promotional':
                types_of_copies = "Promotional Copies"
            elif waiting.types_of_copies == 'correspondents':
                types_of_copies = "Correspondents Copies"
            elif waiting.types_of_copies == 'office':
                types_of_copies = "Office Copies"
            elif waiting.types_of_copies == 'postal':
                types_of_copies = "Postal Copies"
            else:
                types_of_copies = ''

            demand_list.append({
                'id': waiting.id if waiting.id else 0,
                'agent_id': waiting.Agent_id.id if waiting.Agent_id.id else 0,
                'agent_name': waiting.Agent_id.name if waiting.Agent_id.name else '',
                'agent_copies': waiting.Agent_copies if waiting.Agent_copies else 0,
                'demand_type': selection_field,
                'permanent_date': waiting.permanent_date if waiting.permanent_date else '',
                'specific_date': waiting.specific_date if waiting.specific_date else '',
                'demand_update_type': selection_update_agent_copies,
                'decrease_agent_copies': waiting.decrease_agent_copies if waiting.decrease_agent_copies else 0,
                'decrease_additional_copies': waiting.decrease_additional_copies if waiting.decrease_additional_copies else 0,
                'update_demand': selection_additional_type,
                'type_of_copies': types_of_copies,
                'increase_agent_copies': waiting.update_agent_copies if waiting.update_agent_copies else 0,
                'increase_of_additional_copies': waiting.no_of_additional_copies if waiting.no_of_additional_copies else 0,
                'free_copies': waiting.free_copies if waiting.free_copies else 0,
                'postal_copies': waiting.postal_copies if waiting.postal_copies else 0,
                'voucher_copies': waiting.voucher_copies if waiting.voucher_copies else 0,
                'promotional_copies': waiting.promotional_copies if waiting.promotional_copies else 0,
                'correspondent_copies': waiting.correspondents_copies if waiting.correspondents_copies else 0,
                'office_copies': waiting.office_copies if waiting.office_copies else 0,
                'total_copies': waiting.total_copies if waiting.total_copies else 0,
            })

        return demand_list

    @restapi.method([(["/demand_request_rejected"], "GET")], auth="public")
    def demand_request_rejected(self):
        demand_request_obj = self.env['demand.request'].search(
            [('state', '=', 'rejected')])
        demand_list = []
        for rejected in demand_request_obj:

            if rejected.selection_field == 'specific_date':
                selection_field = "Specific date"
            elif rejected.selection_field == 'permanent':
                selection_field = "Permanent"
            else:
                selection_field = ''

            if rejected.selection_update_agent_copies == 'increase':
                selection_update_agent_copies = "Increase Copies"
            elif rejected.selection_update_agent_copies == 'decrease':
                selection_update_agent_copies = "Decrease Copies"
            else:
                selection_update_agent_copies = ''
            if rejected.selection_additional_type == 'increase_additional':
                selection_additional_type = "Increase of Additional Copies"
            elif rejected.selection_additional_type == 'decrease_additional':
                selection_additional_type = "Decrease of Additional Copies"
            else:
                selection_additional_type = ''

            if rejected.types_of_copies == 'agent':
                types_of_copies = "Agent Copies"
            elif rejected.types_of_copies == 'free':
                types_of_copies = "Free Copies"
            elif rejected.types_of_copies == 'voucher':
                types_of_copies = "Voucher Copies"
            elif rejected.types_of_copies == 'promotional':
                types_of_copies = "Promotional Copies"
            elif rejected.types_of_copies == 'correspondents':
                types_of_copies = "Correspondents Copies"
            elif rejected.types_of_copies == 'office':
                types_of_copies = "Office Copies"
            elif rejected.types_of_copies == 'postal':
                types_of_copies = "Postal Copies"
            else:
                types_of_copies = ''

            demand_list.append({
                'id': rejected.id if rejected.id else 0,
                'agent_id': rejected.Agent_id.id if rejected.Agent_id.id else 0,
                'agent_name': rejected.Agent_id.name if rejected.Agent_id.name else '',
                'agent_copies': rejected.Agent_copies if rejected.Agent_copies else 0,
                'demand_type': selection_field,
                'permanent_date': rejected.permanent_date if rejected.permanent_date else '',
                'specific_date': rejected.specific_date if rejected.specific_date else '',
                'demand_update_type': selection_update_agent_copies,
                'decrease_agent_copies': rejected.decrease_agent_copies if rejected.decrease_agent_copies else 0,
                'decrease_additional_copies': rejected.decrease_additional_copies if rejected.decrease_additional_copies else 0,
                'update_demand': selection_additional_type,
                'type_of_copies': types_of_copies,
                'increase_agent_copies': rejected.update_agent_copies if rejected.update_agent_copies else 0,
                'increase_of_additional_copies': rejected.no_of_additional_copies if rejected.no_of_additional_copies else 0,
                'free_copies': rejected.free_copies if rejected.free_copies else 0,
                'postal_copies': rejected.postal_copies if rejected.postal_copies else 0,
                'voucher_copies': rejected.voucher_copies if rejected.voucher_copies else 0,
                'promotional_copies': rejected.promotional_copies if rejected.promotional_copies else 0,
                'correspondent_copies': rejected.correspondents_copies if rejected.correspondents_copies else 0,
                'office_copies': rejected.office_copies if rejected.office_copies else 0,
                'total_copies': rejected.total_copies if rejected.total_copies else 0,
            })

        return demand_list

    @restapi.method([(["/demand_request_approved"], "GET")], auth="public")
    def demand_request_approved(self):
        demand_request_obj = self.env['demand.request'].search(
            [('state', '=', 'approved')])
        demand_list = []
        for approved in demand_request_obj:

            if approved.selection_field == 'specific_date':
                selection_field = "Specific date"
            elif approved.selection_field == 'permanent':
                selection_field = "Permanent"
            else:
                selection_field = ''

            if approved.selection_update_agent_copies == 'increase':
                selection_update_agent_copies = "Increase Copies"
            elif approved.selection_update_agent_copies == 'decrease':
                selection_update_agent_copies = "Decrease Copies"
            else:
                selection_update_agent_copies = ''

            if approved.selection_additional_type == 'increase_additional':
                selection_additional_type = "Increase of Additional Copies"
            elif approved.selection_additional_type == 'decrease_additional':
                selection_additional_type = "Decrease of Additional Copies"
            else:
                selection_additional_type = ''

            if approved.types_of_copies == 'agent':
                types_of_copies = "Agent Copies"
            elif approved.types_of_copies == 'free':
                types_of_copies = "Free Copies"
            elif approved.types_of_copies == 'voucher':
                types_of_copies = "Voucher Copies"
            elif approved.types_of_copies == 'promotional':
                types_of_copies = "Promotional Copies"
            elif approved.types_of_copies == 'correspondents':
                types_of_copies = "Correspondents Copies"
            elif approved.types_of_copies == 'office':
                types_of_copies = "Office Copies"
            elif approved.types_of_copies == 'postal':
                types_of_copies = "Postal Copies"
            else:
                types_of_copies = ''

            demand_list.append({
                'id': approved.id if approved.id else 0,
                'agent_id': approved.Agent_id.id if approved.Agent_id.id else 0,
                'agent_name': approved.Agent_id.name if approved.Agent_id.name else '',
                'agent_copies': approved.Agent_copies if approved.Agent_copies else 0,
                'demand_type': selection_field,
                'permanent_date': approved.permanent_date if approved.permanent_date else '',
                'specific_date': approved.specific_date if approved.specific_date else '',
                'demand_update_type': selection_update_agent_copies,
                'decrease_agent_copies': approved.decrease_agent_copies if approved.decrease_agent_copies else 0,
                'decrease_additional_copies': approved.decrease_additional_copies if approved.decrease_additional_copies else 0,
                'update_demand': selection_additional_type,
                'type_of_copies': types_of_copies,
                'increase_agent_copies': approved.update_agent_copies if approved.update_agent_copies else 0,
                'increase_of_additional_copies': approved.no_of_additional_copies if approved.no_of_additional_copies else 0,
                'free_copies': approved.free_copies if approved.free_copies else 0,
                'postal_copies': approved.postal_copies if approved.postal_copies else 0,
                'voucher_copies': approved.voucher_copies if approved.voucher_copies else 0,
                'promotional_copies': approved.promotional_copies if approved.promotional_copies else 0,
                'correspondent_copies': approved.correspondents_copies if approved.correspondents_copies else 0,
                'office_copies': approved.office_copies if approved.office_copies else 0,
                'total_copies': approved.total_copies if approved.total_copies else 0,
            })

        return demand_list

    @restapi.method([(["/return_request"], "GET")], auth="public")
    def return_request(self):
        return_req_obj = request.env['return.request'].search(
            [])

        return_list = []
        for return_request in return_req_obj:
            requests = []
            for return_line in return_request.return_request_line:
                product_type = ''
                return_type = ''
                if return_line.product_type == 'newspaper':
                    product_type += 'NewsPaper'
                elif return_line.product_type == 'magazine':
                    product_type += 'Magazine'

                if return_line.return_type == 'full_paper':
                    return_type += 'Full Paper'
                elif return_line.return_type == 'master_head':
                    return_type += 'Master Head'

                requests.append({
                    'id': return_line.id if return_line.id else 0,
                    'date': return_line.date if return_line.date else 0,
                    'product_type': product_type,
                    'return_type': return_type,
                    'no_of_copies': return_line.no_of_copies if return_line.no_of_copies else 0,
                    'weight': return_line.weight if return_line.weight else 0.0,
                    'is_credit_done': return_line.is_credit_done
                })

            return_list.append({
                'id': return_request.id if return_request.id else 0,
                'agent_name': return_request.agent_id.name if return_request.agent_id.name else '',
                'products': return_request.product_news_paper_id.name if return_request.product_news_paper_id.name else '',
                'from_date': return_request.from_date if return_request.from_date else 0,
                'to_date': return_request.to_date if return_request.to_date else 0,
                'return_requests_line': requests,
            })

        return return_list

    @restapi.method([(["/return_request_form/<int:rec_id>"], "GET")], auth="public")
    def return_request_form(self, rec_id):
        return_req_obj = request.env['return.request'].search([('id', '=', rec_id)])
        return_list = []
        for return_request in return_req_obj:
            requests = []
            for return_line in return_request.return_request_line:
                product_type = ''
                return_type = ''
                if return_line.product_type == 'newspaper':
                    product_type += 'NewsPaper'
                elif return_line.product_type == 'magazine':
                    product_type += 'Magazine'

                if return_line.return_type == 'full_paper':
                    return_type += 'Full Paper'
                elif return_line.return_type == 'master_head':
                    return_type += 'Master Head'

                requests.append({
                    'id': return_line.id if return_line.id else 0,
                    'date': return_line.date if return_line.date else 0,
                    'product_type': product_type,
                    'return_type': return_type,
                    'no_of_copies': return_line.no_of_copies if return_line.no_of_copies else 0,
                    'weight': return_line.weight if return_line.weight else 0.0,
                    'is_credit_done': return_line.is_credit_done
                })

            return_list.append({
                'id': return_request.id if return_request.id else 0,
                'agent_name': return_request.agent_id.name if return_request.agent_id.name else '',
                'products': return_request.product_news_paper_id.name if return_request.product_news_paper_id.name else '',
                'from_date': return_request.from_date if return_request.from_date else 0,
                'to_date': return_request.to_date if return_request.to_date else 0,
                'state': return_request.state if return_request.state else '',
                'return_requests_line': requests,
            })

        return return_list

    @restapi.method([(["/create_return_request"], "POST")], auth="public")
    def create_return_request(self):
        params = request.params

        values = []

        return_request_lines = params.get('return_requests_line')

        for ret_lines in return_request_lines:
            if ret_lines['product_type'] == 'NewsPaper':
                product_type = 'newspaper'
            elif ret_lines['product_type'] == 'Magazine':
                product_type = 'magazine'
            else:
                product_type = ''

            if ret_lines['return_type'] == 'Full Paper':
                return_type = 'full_paper'
            elif ret_lines['return_type'] == 'Master Head':
                return_type = 'master_head'
            else:
                return_type = ''

            values.append({
                'return_id': ret_lines['id'],
                'date': ret_lines['date'],
                'product_type': product_type,
                'return_type': return_type,
                'no_of_copies': ret_lines['no_of_copies'],
                'weight': ret_lines['weight'],
                'is_credit_done': ret_lines['is_credit_done']
            })

        result = request.env['return.request.line'].create(values)
        result.send_return_request_mail()
        final_result = []
        for res in result:
            final_result.append({
                "id": res.id,
                "status": "Success"
            })
        return final_result

    @restapi.method([(["/return_request_waiting"], "GET")], auth="public")
    def return_request_waiting(self):
        return_req_obj = request.env['return.request'].search(
            [('state', '=', 'waiting')])
        return_list = []

        for return_request in return_req_obj:
            requests = []
            for return_line in return_request.return_request_line:
                product_type = ''
                return_type = ''
                if return_line.product_type == 'newspaper':
                    product_type += 'NewsPaper'
                elif return_line.product_type == 'magazine':
                    product_type += 'Magazine'

                if return_line.return_type == 'full_paper':
                    return_type += 'Full Paper'
                elif return_line.return_type == 'master_head':
                    return_type += 'Master Head'

                requests.append({
                    'id': return_line.id if return_line.id else 0,
                    'date': return_line.date if return_line.date else 0,
                    'product_type': product_type,
                    'return_type': return_type,
                    'no_of_copies': return_line.no_of_copies if return_line.no_of_copies else 0,
                    'weight': return_line.weight if return_line.weight else 0.0,
                    'is_credit_done': return_line.is_credit_done
                })

            return_list.append({
                'id': return_request.id if return_request.id else 0,
                'agent_name': return_request.agent_id.name if return_request.agent_id.name else '',
                'products': return_request.product_news_paper_id.name if return_request.product_news_paper_id.name else '',
                'from_date': return_request.from_date if return_request.from_date else 0,
                'to_date': return_request.to_date if return_request.to_date else 0,
                'return_requests_line': requests,
            })
        return return_list

    @restapi.method([(["/return_request_approved"], "GET")], auth="public")
    def return_request_approved(self):
        return_req_obj = request.env['return.request'].search(
            [('state', '=', 'approved')])
        return_list = []

        for return_request in return_req_obj:
            requests = []
            for return_line in return_request.return_request_line:
                product_type = ''
                return_type = ''
                if return_line.product_type == 'newspaper':
                    product_type += 'NewsPaper'
                elif return_line.product_type == 'magazine':
                    product_type += 'Magazine'

                if return_line.return_type == 'full_paper':
                    return_type += 'Full Paper'
                elif return_line.return_type == 'master_head':
                    return_type += 'Master Head'

                requests.append({
                    'id': return_line.id if return_line.id else 0,
                    'date': return_line.date if return_line.date else 0,
                    'product_type': product_type,
                    'return_type': return_type,
                    'no_of_copies': return_line.no_of_copies if return_line.no_of_copies else 0,
                    'weight': return_line.weight if return_line.weight else 0.0,
                    'is_credit_done': return_line.is_credit_done
                })

            return_list.append({
                'id': return_request.id if return_request.id else 0,
                'agent_name': return_request.agent_id.name if return_request.agent_id.name else '',
                'products': return_request.product_news_paper_id.name if return_request.product_news_paper_id.name else '',
                'from_date': return_request.from_date if return_request.from_date else 0,
                'to_date': return_request.to_date if return_request.to_date else 0,
                'return_requests_line': requests,
            })
        return return_list

    @restapi.method([(["/return_request_news_paper_received"], "GET")], auth="public")
    def return_request_news_paper_received(self):
        return_req_obj = request.env['return.request'].search(
            [('state', '=', 'news_paper_received')])
        return_list = []

        for return_request in return_req_obj:
            requests = []
            for return_line in return_request.return_request_line:
                product_type = ''
                return_type = ''
                if return_line.product_type == 'newspaper':
                    product_type += 'NewsPaper'
                elif return_line.product_type == 'magazine':
                    product_type += 'Magazine'

                if return_line.return_type == 'full_paper':
                    return_type += 'Full Paper'
                elif return_line.return_type == 'master_head':
                    return_type += 'Master Head'

                requests.append({
                    'id': return_line.id if return_line.id else 0,
                    'date': return_line.date if return_line.date else 0,
                    'product_type': product_type,
                    'return_type': return_type,
                    'no_of_copies': return_line.no_of_copies if return_line.no_of_copies else 0,
                    'weight': return_line.weight if return_line.weight else 0.0,
                    'is_credit_done': return_line.is_credit_done
                })

            return_list.append({
                'id': return_request.id if return_request.id else 0,
                'agent_name': return_request.agent_id.name if return_request.agent_id.name else '',
                'products': return_request.product_news_paper_id.name if return_request.product_news_paper_id.name else '',
                'from_date': return_request.from_date if return_request.from_date else 0,
                'to_date': return_request.to_date if return_request.to_date else 0,
                'return_requests_line': requests,
            })
        return return_list

    @restapi.method([(["/return_request_credit_note_done"], "GET")], auth="public")
    def return_request_credit_note_done(self):
        return_req_obj = request.env['return.request'].search(
            [('state', '=', 'credit_note_done')])
        return_list = []

        for return_request in return_req_obj:
            requests = []
            for return_line in return_request.return_request_line:
                product_type = ''
                return_type = ''
                if return_line.product_type == 'newspaper':
                    product_type += 'NewsPaper'
                elif return_line.product_type == 'magazine':
                    product_type += 'Magazine'

                if return_line.return_type == 'full_paper':
                    return_type += 'Full Paper'
                elif return_line.return_type == 'master_head':
                    return_type += 'Master Head'

                requests.append({
                    'id': return_line.id if return_line.id else 0,
                    'date': return_line.date if return_line.date else 0,
                    'product_type': product_type,
                    'return_type': return_type,
                    'no_of_copies': return_line.no_of_copies if return_line.no_of_copies else 0,
                    'weight': return_line.weight if return_line.weight else 0.0,
                    'is_credit_done': return_line.is_credit_done
                })

            return_list.append({
                'id': return_request.id if return_request.id else 0,
                'agent_name': return_request.agent_id.name if return_request.agent_id.name else '',
                'products': return_request.product_news_paper_id.name if return_request.product_news_paper_id.name else '',
                'from_date': return_request.from_date if return_request.from_date else 0,
                'to_date': return_request.to_date if return_request.to_date else 0,
                'return_requests_line': requests,
            })
        return return_list

    @restapi.method([(["/number_of_copies"], "GET")], auth="public")
    def number_of_copies(self):
        user_id = request.env.user
        copies = []
        copies.append({
            'agent_id': user_id.partner_id.id,
            'agent_name': user_id.name,
            'agent_copies': user_id.partner_id.n_q_zone,
            'free_copies': user_id.partner_id.f_q_zone,
            'postal_copies': user_id.partner_id.p_q_zone,
            'voucher_copies': user_id.partner_id.v_q_zone,
            'promotional_copies': user_id.partner_id.c_c_zone,
            'office_copies': user_id.partner_id.o_q_zone,
            'total_copies' : user_id.partner_id.t_c_zone,
        })
        return copies

    @restapi.method([(["/dashboard_details"], "GET")], auth="public")
    def dashboard_details(self):
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
        demand_request_list = []
        payment_collections_total = 0.0
        total_amount = 0.0
        total_amount_due = 0.0
        total_commission_total = 0.0
        account_deposit_total_amount = 0.0
        account_deposit_total_amount_outstanding = 0.0
        invoice_lines = []
        if super_admin:
            demand_request = self.env['demand.request'].search([('Agent_id', 'in', super_admin),
                                                                ('state', '=', 'waiting')])
            for demand in demand_request:
                demand_request_list.append(demand.id)
            account_payment = self.env['account.payment'].search([('partner_id', 'in', super_admin),
                                                                  ('state', '=', 'posted')])
            for pay in account_payment:
                payment_collections_total += pay.amount_company_currency_signed

            unit_account_move = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                 ('move_type', '=', 'out_invoice'),
                                                                 ('state', '=', 'posted'),
                                                                 ('partner_id', 'in', super_admin)])
            for agent in unit_account_move:
                total_amount += agent.amount_total_signed
                total_amount_due += agent.amount_residual_signed
                total_commission_total += agent.commission_total
            circulation_head_account_deposit = self.env['account.deposit'].search([
                ('partner_id', '=', super_admin)])
            for deposit in circulation_head_account_deposit:
                account_deposit_total_amount += deposit.deposit_amt
                account_deposit_total_amount_outstanding += deposit.total_outstanding
            unit_agents_account_move_lines = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                              ('move_type', '=', 'out_invoice'),
                                                                              ('state', '=', 'posted'),
                                                                              ('partner_id', 'in', super_admin)])
            for invoice in unit_agents_account_move_lines:
                if invoice.amount_total != 0.00:
                    progress = round(invoice.amount_residual / invoice.amount_total * 100)
                else:
                    progress = 0
                invoice_lines.append({
                    'agent_name': invoice.partner_id.name,
                    'invoice_number': invoice.name,
                    'invoice_due_date': invoice.invoice_date_due,
                    'total_amount': invoice.amount_total,
                    'amount_residual': invoice.amount_residual,
                    'progress': progress
                })
        elif circulation_head:
            demand_request = self.env['demand.request'].search([('Agent_id', 'in', circulation_head),
                                                                ('state', '=', 'waiting')])
            for demand in demand_request:
                demand_request_list.append(demand.id)
            account_payment = self.env['account.payment'].search([('partner_id', 'in', circulation_head),
                                                                  ('state', '=', 'posted')])
            for pay in account_payment:
                payment_collections_total += pay.amount_company_currency_signed

            unit_account_move = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                 ('move_type', '=', 'out_invoice'),
                                                                 ('state', '=', 'posted'),
                                                                 ('partner_id', 'in', circulation_head)])
            for agent in unit_account_move:
                total_amount += agent.amount_total_signed
                total_amount_due += agent.amount_residual_signed
                total_commission_total += agent.commission_total
            circulation_head_account_deposit = self.env['account.deposit'].search([
                ('partner_id', '=', circulation_head)])
            for deposit in circulation_head_account_deposit:
                account_deposit_total_amount += deposit.deposit_amt
                account_deposit_total_amount_outstanding += deposit.total_outstanding
            unit_agents_account_move_lines = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                              ('move_type', '=', 'out_invoice'),
                                                                              ('state', '=', 'posted'),
                                                                              ('partner_id', 'in', circulation_head)])
            for invoice in unit_agents_account_move_lines:
                if invoice.amount_total != 0.00:
                    progress = round(invoice.amount_residual / invoice.amount_total * 100)
                else:
                    progress = 0
                invoice_lines.append({
                    'agent_name': invoice.partner_id.name,
                    'invoice_number': invoice.name,
                    'invoice_due_date': invoice.invoice_date_due,
                    'total_amount': invoice.amount_total,
                    'amount_residual': invoice.amount_residual,
                    'progress': progress
                })
        elif circulation_admin:
            demand_request = self.env['demand.request'].search([('Agent_id', 'in', circulation_admin),
                                                                ('state', '=', 'waiting')])
            for demand in demand_request:
                demand_request_list.append(demand.id)
            account_payment = self.env['account.payment'].search([('partner_id', 'in', circulation_admin),
                                                                  ('state', '=', 'posted')])
            for pay in account_payment:
                payment_collections_total += pay.amount_company_currency_signed

            unit_account_move = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                 ('move_type', '=', 'out_invoice'),
                                                                 ('state', '=', 'posted'),
                                                                 ('partner_id', 'in', circulation_admin)])
            for agent in unit_account_move:
                total_amount += agent.amount_total_signed
                total_amount_due += agent.amount_residual_signed
                total_commission_total += agent.commission_total
            circulation_head_account_deposit = self.env['account.deposit'].search([
                ('partner_id', '=', circulation_admin)])
            for deposit in circulation_head_account_deposit:
                account_deposit_total_amount += deposit.deposit_amt
                account_deposit_total_amount_outstanding += deposit.total_outstanding
            unit_agents_account_move_lines = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                              ('move_type', '=', 'out_invoice'),
                                                                              ('state', '=', 'posted'),
                                                                              ('partner_id', 'in', circulation_admin)])
            for invoice in unit_agents_account_move_lines:
                if invoice.amount_total != 0.00:
                    progress = round(invoice.amount_residual / invoice.amount_total * 100)
                else:
                    progress = 0
                invoice_lines.append({
                    'agent_name': invoice.partner_id.name,
                    'invoice_number': invoice.name,
                    'invoice_due_date': invoice.invoice_date_due,
                    'total_amount': invoice.amount_total,
                    'amount_residual': invoice.amount_residual,
                    'progress': progress
                })
        elif regional_head:
            demand_request = self.env['demand.request'].search([('Agent_id', 'in', regional_head),
                                                                ('state', '=', 'waiting')])
            for demand in demand_request:
                demand_request_list.append(demand.id)
            account_payment = self.env['account.payment'].search([('partner_id', 'in', regional_head),
                                                                  ('state', '=', 'posted')])
            for pay in account_payment:
                payment_collections_total += pay.amount_company_currency_signed

            unit_account_move = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                 ('move_type', '=', 'out_invoice'),
                                                                 ('state', '=', 'posted'),
                                                                 ('partner_id', 'in', regional_head)])
            for agent in unit_account_move:
                total_amount += agent.amount_total_signed
                total_amount_due += agent.amount_residual_signed
                total_commission_total += agent.commission_total
            circulation_head_account_deposit = self.env['account.deposit'].search([
                ('partner_id', '=', regional_head)])
            for deposit in circulation_head_account_deposit:
                account_deposit_total_amount += deposit.deposit_amt
                account_deposit_total_amount_outstanding += deposit.total_outstanding
            unit_agents_account_move_lines = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                              ('move_type', '=', 'out_invoice'),
                                                                              ('state', '=', 'posted'),
                                                                              ('partner_id', 'in', regional_head)])
            for invoice in unit_agents_account_move_lines:
                if invoice.amount_total != 0.00:
                    progress = round(invoice.amount_residual / invoice.amount_total * 100)
                else:
                    progress = 0
                invoice_lines.append({
                    'agent_name': invoice.partner_id.name,
                    'invoice_number': invoice.name,
                    'invoice_due_date': invoice.invoice_date_due,
                    'total_amount': invoice.amount_total,
                    'amount_residual': invoice.amount_residual,
                    'progress': progress
                })
        elif unit_incharge:
            demand_request = self.env['demand.request'].search([('Agent_id', 'in', unit_incharge),
                                                                ('state', '=', 'waiting')])
            for demand in demand_request:
                demand_request_list.append(demand.id)
            account_payment = self.env['account.payment'].search([('partner_id', 'in', unit_incharge),
                                                                  ('state', '=', 'posted')])
            for pay in account_payment:
                payment_collections_total += pay.amount_company_currency_signed

            unit_account_move = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                 ('move_type', '=', 'out_invoice'),
                                                                 ('state', '=', 'posted'),
                                                                 ('partner_id', 'in', unit_incharge)])
            for agent in unit_account_move:
                total_amount += agent.amount_total_signed
                total_amount_due += agent.amount_residual_signed
                total_commission_total += agent.commission_total
            circulation_head_account_deposit = self.env['account.deposit'].search([
                ('partner_id', '=', unit_incharge)])
            for deposit in circulation_head_account_deposit:
                account_deposit_total_amount += deposit.deposit_amt
                account_deposit_total_amount_outstanding += deposit.total_outstanding
            unit_agents_account_move_lines = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                              ('move_type', '=', 'out_invoice'),
                                                                              ('state', '=', 'posted'),
                                                                              ('partner_id', 'in', unit_incharge)])
            for invoice in unit_agents_account_move_lines:
                if invoice.amount_total != 0.00:
                    progress = round(invoice.amount_residual / invoice.amount_total * 100)
                else:
                    progress = 0
                invoice_lines.append({
                    'agent_name': invoice.partner_id.name,
                    'invoice_number': invoice.name,
                    'invoice_due_date': invoice.invoice_date_due,
                    'total_amount': invoice.amount_total,
                    'amount_residual': invoice.amount_residual,
                    'progress': progress
                })
        elif circulation_incharge:
            demand_request = self.env['demand.request'].search([('Agent_id', 'in', circulation_incharge),
                                                                ('state', '=', 'waiting')])
            for demand in demand_request:
                demand_request_list.append(demand.id)
            account_payment = self.env['account.payment'].search([('partner_id', 'in', circulation_incharge),
                                                                  ('state', '=', 'posted')])
            for pay in account_payment:
                payment_collections_total += pay.amount_company_currency_signed

            unit_account_move = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                 ('move_type', '=', 'out_invoice'),
                                                                 ('state', '=', 'posted'),
                                                                 ('partner_id', 'in', circulation_incharge)])
            for agent in unit_account_move:
                total_amount += agent.amount_total_signed
                total_amount_due += agent.amount_residual_signed
                total_commission_total += agent.commission_total
            circulation_head_account_deposit = self.env['account.deposit'].search([
                ('partner_id', '=', circulation_incharge)])
            for deposit in circulation_head_account_deposit:
                account_deposit_total_amount += deposit.deposit_amt
                account_deposit_total_amount_outstanding += deposit.total_outstanding
            unit_agents_account_move_lines = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                              ('move_type', '=', 'out_invoice'),
                                                                              ('state', '=', 'posted'),
                                                                              ('partner_id', 'in',
                                                                               circulation_incharge)])
            for invoice in unit_agents_account_move_lines:
                if invoice.amount_total != 0.00:
                    progress = round(invoice.amount_residual / invoice.amount_total * 100)
                else:
                    progress = 0
                invoice_lines.append({
                    'agent_name': invoice.partner_id.name,
                    'invoice_number': invoice.name,
                    'invoice_due_date': invoice.invoice_date_due,
                    'total_amount': invoice.amount_total,
                    'amount_residual': invoice.amount_residual,
                    'progress': progress
                })
        elif publications_incharge:
            demand_request = self.env['demand.request'].search([('Agent_id', 'in', publications_incharge),
                                                                ('state', '=', 'waiting')])
            for demand in demand_request:
                demand_request_list.append(demand.id)
            account_payment = self.env['account.payment'].search([('partner_id', 'in', publications_incharge),
                                                                  ('state', '=', 'posted')])
            for pay in account_payment:
                payment_collections_total += pay.amount_company_currency_signed

            unit_account_move = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                 ('move_type', '=', 'out_invoice'),
                                                                 ('state', '=', 'posted'),
                                                                 ('partner_id', 'in', publications_incharge)])
            for agent in unit_account_move:
                total_amount += agent.amount_total_signed
                total_amount_due += agent.amount_residual_signed
                total_commission_total += agent.commission_total
            circulation_head_account_deposit = self.env['account.deposit'].search([
                ('partner_id', '=', publications_incharge)])
            for deposit in circulation_head_account_deposit:
                account_deposit_total_amount += deposit.deposit_amt
                account_deposit_total_amount_outstanding += deposit.total_outstanding
            unit_agents_account_move_lines = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                              ('move_type', '=', 'out_invoice'),
                                                                              ('state', '=', 'posted'),
                                                                              ('partner_id', 'in',
                                                                               publications_incharge)])
            for invoice in unit_agents_account_move_lines:
                if invoice.amount_total != 0.00:
                    progress = round(invoice.amount_residual / invoice.amount_total * 100)
                else:
                    progress = 0
                invoice_lines.append({
                    'agent_name': invoice.partner_id.name,
                    'invoice_number': invoice.name,
                    'invoice_due_date': invoice.invoice_date_due,
                    'total_amount': invoice.amount_total,
                    'amount_residual': invoice.amount_residual,
                    'progress': progress
                })
        elif field_segment_incharge:
            demand_request = self.env['demand.request'].search([('Agent_id', 'in', field_segment_incharge),
                                                                ('state', '=', 'waiting')])
            for demand in demand_request:
                demand_request_list.append(demand.id)
            account_payment = self.env['account.payment'].search([('partner_id', 'in', field_segment_incharge),
                                                                  ('state', '=', 'posted')])
            for pay in account_payment:
                payment_collections_total += pay.amount_company_currency_signed

            unit_account_move = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                 ('move_type', '=', 'out_invoice'),
                                                                 ('state', '=', 'posted'),
                                                                 ('partner_id', 'in', field_segment_incharge)])
            for agent in unit_account_move:
                total_amount += agent.amount_total_signed
                total_amount_due += agent.amount_residual_signed
                total_commission_total += agent.commission_total
            circulation_head_account_deposit = self.env['account.deposit'].search([
                ('partner_id', '=', field_segment_incharge)])
            for deposit in circulation_head_account_deposit:
                account_deposit_total_amount += deposit.deposit_amt
                account_deposit_total_amount_outstanding += deposit.total_outstanding
            unit_agents_account_move_lines = self.env['account.move'].search([('internal_order_bool', '=', True),
                                                                              ('move_type', '=', 'out_invoice'),
                                                                              ('state', '=', 'posted'),
                                                                              ('partner_id', 'in',
                                                                               field_segment_incharge)])
            for invoice in unit_agents_account_move_lines:
                if invoice.amount_total != 0.00:
                    progress = round(invoice.amount_residual / invoice.amount_total * 100)
                else:
                    progress = 0
                invoice_lines.append({
                    'agent_name': invoice.partner_id.name,
                    'invoice_number': invoice.name,
                    'invoice_due_date': invoice.invoice_date_due,
                    'total_amount': invoice.amount_total,
                    'amount_residual': invoice.amount_residual,
                    'progress': progress
                })

        current_day = datetime.today().strftime('%Y-%m-%d')
        previous_day = datetime.today() - timedelta(days=1)
        previous_day_str = previous_day.strftime('%Y-%m-%d')
        partner_id = self.env['res.partner'].search([('id', '=', user_id.partner_id.id)])

        indent_supplied = self.env['sale.order'].search([('internal_order', '=', True),
                                                         ('user_id', '=', user_id.id),
                                                         ('create_date', '>=', current_day + ' 00:00:00'),
                                                         ('create_date', '<', current_day + ' 23:59:59')])

        circulation_head_indent_supplied = self.env['sale.order'].search([
            ('internal_order', '=', True),
            ('create_date', '>=', current_day + ' 00:00:00'),
            ('create_date', '<', current_day + ' 23:59:59')])

        indent_supplied_previous_day = self.env['sale.order'].search([
            ('internal_order', '=', True),
            ('user_id', '=', user_id.id),
            ('create_date', '>=', previous_day_str + ' 00:00:00'),
            ('create_date', '<', previous_day_str + ' 23:59:59')])

        circulation_head_indent_supplied_previous_day = self.env['sale.order'].search([
            ('internal_order', '=', True),
            ('create_date', '>=', previous_day_str + ' 00:00:00'),
            ('create_date', '<', previous_day_str + ' 23:59:59')])

        total_copies_current_day = 0
        total_copies_previous_day = 0
        if indent_supplied:
            for so_line in indent_supplied.order_line:
                if so_line.product_id.is_newspaper == True:
                    total_copies_current_day += so_line.product_uom_qty

        else:
            if circulation_head_indent_supplied:
                for so_line in circulation_head_indent_supplied.order_line:
                    if so_line.product_id.is_newspaper == True:
                        total_copies_current_day += so_line.product_uom_qty

        if indent_supplied_previous_day:
            for so_line in indent_supplied_previous_day.order_line:
                if so_line.product_id.is_newspaper == True:
                    total_copies_previous_day += so_line.product_uom_qty

        else:
            for so_line in circulation_head_indent_supplied_previous_day.order_line:
                if so_line.product_id.is_newspaper == True:
                    total_copies_previous_day += so_line.product_uom_qty

        agent_list = []
        unit_ids = self.env['res.partner'].search([('is_printing_unit', '=', True), ('user_id', '=', user_id.id)])
        circulation_head_unit_ids = self.env['res.partner'].search([('is_printing_unit', '=', True)])

        if unit_ids:
            for unit in unit_ids:
                for edition in unit.servie_regions:
                    for district in edition.district_o2m:
                        for zones in district.zone_o2m:
                            for agents in zones.add_zones_to_line:
                                agent_list.append(agents.cc_zone.id)

        else:
            for unit in circulation_head_unit_ids:
                for edition in unit.servie_regions:
                    for district in edition.district_o2m:
                        for zones in district.zone_o2m:
                            for agents in zones.add_zones_to_line:
                                agent_list.append(agents.cc_zone.id)

        unit_payment_ids = self.env['res.partner'].search([('is_printing_unit', '=', True),
                                                           ('user_id', '=', user_id.id)])
        circulation_head__payment_unit_ids = self.env['res.partner'].search([('is_printing_unit', '=', True)])
        unit_agent_ids = []
        head_agent_ids = []

        if unit_payment_ids:
            for unit in unit_payment_ids:
                for edition in unit.servie_regions:
                    for district in edition.district_o2m:
                        for zones in district.zone_o2m:
                            for agents in zones.add_zones_to_line:
                                unit_agent_ids.append(agents.cc_zone.id)

        else:
            for unit in circulation_head__payment_unit_ids:
                for edition in unit.servie_regions:
                    for district in edition.district_o2m:
                        for zones in district.zone_o2m:
                            for agents in zones.add_zones_to_line:
                                head_agent_ids.append(agents.cc_zone.id)

        transportation_bill = self.env['account.move'].search([('move_type', '=', 'in_invoice'),
                                                               ('is_transportation', '=', True),
                                                               ('state', '=', 'posted')])
        transportation_bill_total_amount = 0.0
        transportation_bill_total_amount_due = 0.0
        if transportation_bill:
            for vendor_bill in transportation_bill:
                transportation_bill_total_amount += vendor_bill.amount_total_signed
                transportation_bill_total_amount_due += vendor_bill.amount_residual

        deposits_obj = self.env['account.deposit'].search(
            [('partner_id', '=', user_id.partner_id.id), ('circulation', '=', True), ('status', '=', 'running')])

        deposit_amt = 0.00
        outstanding_amt = 0.00
        if unit_agent_ids:
            for deposits in deposits_obj:
                if deposits.partner_id.id in unit_agent_ids:
                    deposit_amt += deposits.deposit_amt
                    outstanding_amt += deposits.total_outstanding

        else:
            for deposits in deposits_obj:
                if deposits.partner_id.id in head_agent_ids:
                    deposit_amt += deposits.deposit_amt
                    outstanding_amt += deposits.total_outstanding


        circulation_units_agents_head_agent_invoices = self.env['account.move'].search([
            ('internal_order_bool', '=', True),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted')])

        total_demand_request = 0
        demand_request = self.env['demand.request'].search([('state', '=', 'waiting')])

        if unit_agent_ids:
            for demand_agent in demand_request:
                if demand_agent.Agent_id.id in unit_agent_ids:
                    total_demand_request += 1

        else:
            if head_agent_ids:
                for demand_agent in demand_request:
                    if demand_agent.Agent_id.id in head_agent_ids:
                        total_demand_request += 1

        sale_order_lines = []
        unit_wise = self.env['sale.order'].search([('user_id', '=', user_id.id), ('internal_order', '=', True)])
        circulation_head_wise = self.env['sale.order'].search([('internal_order', '=', True)])
        if unit_wise:
            for lines in unit_wise.order_line:
                sale_order_lines.append({
                    'agent_name': lines.region_s.name,
                    'newspaper_date': lines.newspaper_date,
                    'agent_copies': lines.agent_copies,
                    'free_copies': lines.free_copies,
                    'postal_copies': lines.postal_copies,
                    'voucher_copies': lines.voucher_copies,
                    'promotional_copies': lines.promotional_copies,
                    'correspondents_copies': lines.correspondents_copies,
                    'office_copies': lines.office_copies,
                    'product_uom_qty': lines.product_uom_qty,
                })
        if not unit_wise:
            for lines in circulation_head_wise.order_line:
                sale_order_lines.append({
                    'agent_name': lines.region_s.name,
                    'newspaper_date': lines.newspaper_date,
                    'agent_copies': lines.agent_copies,
                    'free_copies': lines.free_copies,
                    'postal_copies': lines.postal_copies,
                    'voucher_copies': lines.voucher_copies,
                    'promotional_copies': lines.promotional_copies,
                    'correspondents_copies': lines.correspondents_copies,
                    'office_copies': lines.office_copies,
                    'product_uom_qty': lines.product_uom_qty,
                })

        current_year = datetime.now().year

        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year, 12, 31)

        domain = [('invoice_date', '>=', start_date), ('invoice_date', '<=', end_date),
                  ('internal_order_bool', '=', True)]
        records = self.env['account.move'].search(domain)
        invoice_unit_ids = self.env['res.partner'].search([('is_printing_unit', '=', True)])

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

        return {
            'todays_demand': total_copies_current_day,
            'indent_history': total_copies_previous_day,
            'total_demand_request': len(demand_request_list),
            'bill_total_amount': "{0:.2f}".format(total_amount),
            'bill_pending_due': "{0:.2f}".format(total_amount_due),
            'payment_collections_total': "{0:.2f}".format(payment_collections_total),
            # 'total_commission_total': "{0:.2f}".format(total_commission_total),
            'deposit_total_amount': "{0:.2f}".format(account_deposit_total_amount),
            'deposit_total_outstanding_amount': "{0:.2f}".format(account_deposit_total_amount_outstanding),
            # 'transportation_bill_total_amount': "{0:.2f}".format(transportation_bill_total_amount),
            # 'transportation_bill_total_amount_due': "{0:.2f}".format(transportation_bill_total_amount_due),
            # 'indent_lines': sale_order_lines,
            'invoice_lines': invoice_lines,
            'user_list_role': user_list_role,
            'user_list': user_list,
            'reta_cio_next_sequence_number': reta_cio_next_sequence_number,
            'reta_ro_next_sequence_number': reta_ro_next_sequence_number,
            'classifieds_cio_next_sequence_number': classifieds_cio_next_sequence_number,
            'classifieds_ro_next_sequence_number': classifieds_ro_next_sequence_number,
            'customer_next_seq_number': customer_next_seq_number,
            'mobile_number': mobile,
        }

    @restapi.method([(["/agent_indent"], "GET")], auth="public")
    def agent_indent(self):

        agent_dict = []
        agent_indent = request.env['sale.order.line'].search([])

        for agent in agent_indent:

            if agent.demand_state == 'increase':
                demand_state = 'Increase'
            elif agent.demand_state == 'decrease':
                demand_state = 'Decrease'
            else:
                demand_state = ''

            agent_dict.append({
                'id': agent.id if agent.id else 0,
                'newspaper_date': agent.newspaper_date if agent.newspaper_date else '',
                'agent_code': agent.agent_code if agent.agent_code else '',
                'agent_name': agent.region_s.name if agent.region_s.name else '',
                'agent_copies': agent.agent_copies if agent.agent_copies else 0,
                'free_copies': agent.free_copies if agent.free_copies else 0,
                'postal_copies': agent.postal_copies if agent.postal_copies else 0,
                'voucher_copies': agent.voucher_copies if agent.voucher_copies else 0,
                'promotional_copies': agent.promotional_copies if agent.promotional_copies else 0,
                'correspondents_copies': agent.correspondents_copies if agent.correspondents_copies else 0,
                'office_copies': agent.office_copies if agent.office_copies else 0,
                'demand_changes': agent.demand_changes if agent.demand_changes else 0,
                'demand_state': demand_state,
                'quantity': agent.product_uom_qty if agent.product_uom_qty else 0.0,
            })

        return agent_dict

    @restapi.method([(["/agent_indent/<rec_id>"], "GET")], auth="public")
    def agent_indent_rec_id(self, rec_id):

        agent_dict = []
        agent_indent = request.env['sale.order.line'].search([('id', "=", rec_id)])

        for agent in agent_indent:
            tax_list = []
            for tax in agent.tax_id:
                tax_list.append({
                    'id': tax.id if tax.id else 0,
                    'name': tax.name if tax.name else '',
                })
            agent_dict.append({
                'id': agent.id if agent.id else 0,
                'order_id':agent.order_id.id if agent.order_id.id else 0,
                'order_reference':agent.order_id.name if agent.order_id.name else '',
                'product_id': agent.product_id.id if agent.product_id.id else 0,
                'product_name': agent.product_id.name if agent.product_id.name else '',
                'description': agent.name if agent.name else '',
                'quantity':agent.product_uom_qty if agent.product_uom_qty else '',
                'newspaper_date': agent.newspaper_date if agent.newspaper_date else '',
                'quantity_delivered': agent.qty_delivered if agent.qty_delivered else '',
                'quantity_invoiced': agent.qty_invoiced if agent.qty_invoiced else 0.00,
                'unit_of_measure_id': agent.product_uom.id if agent.product_uom.id else 0,
                'unit_of_measure_name': agent.product_uom.name if agent.product_uom.name else '',
                'price_unit': agent.price_unit if agent.price_unit else 0.00,
                'discount': agent.discount if agent.discount else 0.00,
                'price_subtotal': agent.price_subtotal if agent.price_subtotal else 0.00,
                'tax':tax_list,
                'price_tax': agent.price_tax if agent.price_tax else 0.0,
                'price_total': agent.price_total if agent.price_total else 0.0,
            })

        return agent_dict

    @restapi.method([(["/dashboard_agent_invoices"], "GET")], auth="public")
    def dashboard_agent_invoices(self):
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
            super_admin.append(user_id.partner_id.id)
            invoice_obj = self.env['account.move'].search(
                [('partner_id', 'in', super_admin), ('state', '=', 'posted'),
                           ('internal_order_bool', '=', True)])
        elif circulation_head:
            circulation_head.append(user_id.partner_id.id)
            invoice_obj = self.env['account.move'].search(
                [('partner_id', 'in', circulation_head), ('state', '=', 'posted'),
                           ('internal_order_bool', '=', True)])

        elif regional_head:
            regional_head.append(user_id.partner_id.id)
            invoice_obj = self.env['account.move'].search(
                [('partner_id', 'in', regional_head), ('state', '=', 'posted'),
                           ('internal_order_bool', '=', True)])
        elif unit_incharge:
            unit_incharge.append(user_id.partner_id.id)
            invoice_obj = self.env['account.move'].search(
                [('partner_id', 'in', unit_incharge), ('state', '=', 'posted'),
                           ('internal_order_bool', '=', True)])
        elif circulation_incharge:
            circulation_incharge.append(user_id.partner_id.id)
            invoice_obj = self.env['account.move'].search(
                [('partner_id', 'in', circulation_incharge), ('state', '=', 'posted'),
                           ('internal_order_bool', '=', True)])
        elif publications_incharge:
            publications_incharge.append(user_id.partner_id.id)
            invoice_obj = self.env['account.move'].search(
                [('partner_id', 'in', publications_incharge), ('state', '=', 'posted'),
                           ('internal_order_bool', '=', True)])
        elif field_segment_incharge:
            field_segment_incharge.append(user_id.partner_id.id)
            invoice_obj = self.env['account.move'].search(
                [('partner_id', 'in', field_segment_incharge), ('state', '=', 'posted'),
                           ('internal_order_bool', '=', True)])
        else:
            invoice_obj = self.env['account.move'].search(
                [('partner_id', '=', user_id.partner_id.id), ('state', '=', 'posted'),
                           ('internal_order_bool', '=', True)])


        bill_list = []

        for bill in invoice_obj:
            if bill.payment_status == 'on_time':
                payment_status = 'Paid on Time'
            else:
                payment_status = 'Paid Late'

            if bill.payment_state == 'not_paid':
                payment_state = "Not Paid"
            elif bill.payment_state == 'in_payment':
                payment_state = "In Payment"
            elif bill.payment_state == 'paid':
                payment_state = "Paid"
            elif bill.payment_state == 'partial':
                payment_state = "Partially Paid"
            elif bill.payment_state == 'reversed':
                payment_state = "Reversed"
            else:
                payment_state = "Invoicing App Legacy"

            if bill.state == 'posted':
                status = 'Posted'
            else:
                status = ''

            bill_list.append({
                'id': bill.id if bill.id else 0,
                'number': bill.name if bill.name else '',
                'due_date': bill.invoice_date_due if bill.invoice_date_due else '',
                'tax_excluded': bill.amount_untaxed_signed if bill.amount_untaxed_signed else 0.00,
                'total': bill.amount_total_signed if bill.amount_total_signed else 0.00,
                'payment_state': payment_state,
                'payment_status': payment_status,
                'status': status,


            })

        return bill_list

    @restapi.method([(["/dashboard_deposit_history"], "GET")], auth="public")
    def dashboard_deposit_history(self):
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
            super_admin.append(user_id.partner_id.id)
            deposit_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', super_admin)])
        elif circulation_head:
            circulation_head.append(user_id.partner_id.id)
            deposit_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', circulation_head)])

        elif regional_head:
            regional_head.append(user_id.partner_id.id)
            deposit_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', regional_head)])
        elif unit_incharge:
            unit_incharge.append(user_id.partner_id.id)
            deposit_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', unit_incharge)])
        elif circulation_incharge:
            circulation_incharge.append(user_id.partner_id.id)
            deposit_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', circulation_incharge)])
        elif publications_incharge:
            publications_incharge.append(user_id.partner_id.id)
            deposit_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', publications_incharge)])
        elif field_segment_incharge:
            field_segment_incharge.append(user_id.partner_id.id)
            deposit_obj = self.env['account.deposit'].search(
                [('partner_id', 'in', field_segment_incharge)])
        else:
            deposit_obj = self.env['account.deposit'].search(
                [('partner_id', '=', user_id.partner_id.id)])


        deposit_list = []

        for deposit in deposit_obj:

            deposit_list.append({
                'id': deposit.id if deposit.id else 0,
                'name': deposit.name if deposit.name else '',
                'partner_id': deposit.partner_id.id if deposit.partner_id.name else 0,
                'partner_name': deposit.partner_id.name if deposit.partner_id.name else '',
                'initial_amount':deposit.deposit_amt if deposit.deposit_amt else 0.00,
                'interest_percentage': deposit.interest_percent if deposit.interest_percent else 0.00
            })

        return deposit_list

    @restapi.method([(["/dashboard_demand_request_approval"], "GET")], auth="public")
    def dashboard_demand_request_approval(self):
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
            super_admin.append(user_id.partner_id.id)
            demand_obj = self.env['demand.request'].search([('Agent_id', 'in', super_admin),
                                                                ('state', '=', 'waiting')])
        elif circulation_head:
            circulation_head.append(user_id.partner_id.id)
            demand_obj = self.env['demand.request'].search([('Agent_id', 'in', circulation_head),
                                                                ('state', '=', 'waiting')])

        elif regional_head:
            regional_head.append(user_id.partner_id.id)
            demand_obj =self.env['demand.request'].search([('Agent_id', 'in', regional_head),
                                                                ('state', '=', 'waiting')])
        elif unit_incharge:
            unit_incharge.append(user_id.partner_id.id)
            demand_obj = self.env['demand.request'].search([('Agent_id', 'in', unit_incharge),
                                                                ('state', '=', 'waiting')])
        elif circulation_incharge:
            circulation_incharge.append(user_id.partner_id.id)
            demand_obj = self.env['demand.request'].search([('Agent_id', 'in', circulation_incharge),
                                                                ('state', '=', 'waiting')])
        elif publications_incharge:
            publications_incharge.append(user_id.partner_id.id)
            demand_obj = self.env['demand.request'].search([('Agent_id', 'in', publications_incharge),
                                                                ('state', '=', 'waiting')])
        elif field_segment_incharge:
            field_segment_incharge.append(user_id.partner_id.id)
            demand_obj = self.env['demand.request'].search([('Agent_id', 'in', field_segment_incharge),
                                                                ('state', '=', 'waiting')])
        else:
            demand_obj = self.env['demand.request'].search([('Agent_id', '=', user_id.partner_id.id),
                                                                ('state', '=', 'waiting')])

        demand_list = []

        for demand in demand_obj:
            if demand.selection_field == 'permanent':
                selection_field = 'Permanent'
            elif demand.selection_field == 'specific_date':
                selection_field = 'Specific date'
            else:
                selection_field = ''

            if demand.demand_state == 'increase':
                demand_state = "Increase"
            elif demand.demand_state == 'decrease':
                demand_state = "Decrease"
            else:
                demand_state = ''

            if demand.state == 'new':
                status = "New"
            elif demand.state == 'waiting':
                status = "Waiting for approval"
            elif demand.state == 'approved':
                status = "Approved"
            elif demand.state == 'rejected':
                status = "Rejected"
            else:
                status = ''

            demand_list.append({
                'id': demand.id if demand.id else 0,
                'agent_id': demand.Agent_id.id if demand.Agent_id.id else 0 ,
                'agent_name': demand.Agent_id.name if demand.Agent_id.name else '',
                'agent_copies': demand.Agent_copies if demand.Agent_copies else 0,
                'selection_field': selection_field,
                'specific_date': demand.specific_date if demand.specific_date else '',
                'demand_changes': demand.demand_changes if demand.demand_changes else '',
                'demand_state': demand_state,
                'status': status,

            })
        return demand_list

    @restapi.method([(["/dashboard_payment_collections"], "GET")], auth="public")
    def dashboard_payment_collections(self):
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
            super_admin.append(user_id.partner_id.id)
            account_payment_obj = self.env['account.payment'].search([('partner_id', 'in', super_admin),
                                                                  ('state', '=', 'posted')])
        elif circulation_head:
            circulation_head.append(user_id.partner_id.id)
            account_payment_obj = self.env['account.payment'].search([('partner_id', 'in', circulation_head),
                                                                      ('state', '=', 'posted')])

        elif regional_head:
            regional_head.append(user_id.partner_id.id)
            account_payment_obj = self.env['account.payment'].search([('partner_id', 'in', regional_head),
                                                                      ('state', '=', 'posted')])
        elif unit_incharge:
            unit_incharge.append(user_id.partner_id.id)
            account_payment_obj = self.env['account.payment'].search([('partner_id', 'in', unit_incharge),
                                                                      ('state', '=', 'posted')])
        elif circulation_incharge:
            circulation_incharge.append(user_id.partner_id.id)
            account_payment_obj = self.env['account.payment'].search([('partner_id', 'in', circulation_incharge),
                                                                      ('state', '=', 'posted')])
        elif publications_incharge:
            publications_incharge.append(user_id.partner_id.id)
            account_payment_obj = self.env['account.payment'].search([('partner_id', 'in', publications_incharge),
                                                                      ('state', '=', 'posted')])
        elif field_segment_incharge:
            field_segment_incharge.append(user_id.partner_id.id)
            account_payment_obj = self.env['account.payment'].search([('partner_id', 'in', field_segment_incharge),
                                                                      ('state', '=', 'posted')])
        else:
            account_payment_obj = self.env['account.payment'].search([('partner_id', '=', user_id.partner_id.id),
                                                                      ('state', '=', 'posted')])

        account_payment_list = []

        for payment in account_payment_obj:

            account_payment_list.append({
                'id': payment.id if payment.id else 0,
                'date': payment.date if payment.date else '',
                'number': payment.name if payment.name else '',
                'journal_id': payment.journal_id.id if payment.journal_id.id else 0,
                'journal_name': payment.journal_id.name if payment.journal_id.name else '',
                'payment_method_id': payment.payment_method_line_id.id if payment.payment_method_line_id.id else 0,
                'payment_method_name': payment.payment_method_line_id.name if payment.payment_method_line_id.name else '',
                'customer_id': payment.partner_id.id if payment.partner_id.id else 0,
                'customer_name': payment.partner_id.name if payment.partner_id.name else '',
                'amount': payment.amount_company_currency_signed if payment.amount_company_currency_signed else 0.00,
            })
        return account_payment_list

    @restapi.method([(["/dashboard_indent_demand"], "GET")], auth="public")
    def dashboard_indent_demand(self):
        user = self.env.uid
        user_id = self.env['res.users'].browse(user)
        field_segment_incharge = []
        field_segment_incharge_new = []
        for loop_1 in self.env['res.partner'].search([('hr_employee_id.user_id', '=', user_id.id)]):
            field_segment_incharge.append(loop_1.id)
            field_segment_incharge_new.append(loop_1.name)
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
            super_admin.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('partner_id', 'in', super_admin), ('state', '=', 'posted')])
        elif circulation_head:
            circulation_head.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('partner_id', 'in', circulation_head), ('state', '=', 'posted')])
        elif circulation_admin:
            circulation_admin.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('partner_id', 'in', circulation_admin), ('state', '=', 'posted')])
        elif regional_head:
            regional_head.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('partner_id', 'in', regional_head), ('state', '=', 'posted')])
        elif unit_incharge:
            unit_incharge.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('partner_id', 'in', unit_incharge), ('state', '=', 'posted')])
        elif circulation_incharge:
            circulation_incharge.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('partner_id', 'in', circulation_incharge), ('state', '=', 'posted')])
        elif publications_incharge:
            publications_incharge.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('partner_id', 'in', publications_incharge), ('state', '=', 'posted')])
        elif field_segment_incharge:
            field_segment_incharge.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('partner_id', 'in', field_segment_incharge), ('state', '=', 'posted')])
        else:
            indent_demand_obj = self.env['sale.order'].search([('partner_id', '=', user_id.partner_id.id), ('state', '=', 'posted')])

        indent_demand_list = []
        for indent in indent_demand_obj:

            if indent.state_duplicate == 'Posted':
                state_duplicate = 'posted'
            else:
                state_duplicate = ''

            indent_demand_list.append({
                'id': indent.id if indent.id else 0,
                'unit_id': indent.unit_name.id if indent.unit_name.id else 0,
                'unit_name': indent.unit_name.name if indent.unit_name.name else '',
                'create_date': indent.create_date if indent.create_date else '',
                'internal_order_number': indent.new_seq if indent.new_seq else '',
                'agent_copies': indent.agent_copies if indent.agent_copies else 0,
                'free_copies': indent.free_copies if indent.free_copies else 0,
                'postal_copies': indent.postal_copies if indent.postal_copies else 0,
                'voucher_copies': indent.postal_copies if indent.postal_copies else 0,
                'promotional_copies': indent.promotional_copies if indent.promotional_copies else 0,
                'correspondents_copies': indent.correspondents_copies if indent.correspondents_copies else 0,
                'office_copies': indent.office_copies if indent.office_copies else 0,
                'demand_changes': indent.demand_changes if indent.demand_changes else 0,
                'total_copies': indent.total_copies if indent.total_copies else 0,
                'status': state_duplicate
        })

        return indent_demand_list

    @restapi.method([(["/dashboard_indent_supplied"], "GET")], auth="public")
    def dashboard_indent_supplied(self):

        previous_day = datetime.today() - timedelta(days=1)
        previous_day_str = previous_day.strftime('%Y-%m-%d')

        indent_supplied_previous_day = self.env['sale.order'].search([
            ('internal_order', '=', True),
            ('create_date', '>=', previous_day_str + ' 00:00:00'),
            ('create_date', '<', previous_day_str + ' 23:59:59')])

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
            super_admin.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('unit_name', 'in', super_admin), ('id', 'in', indent_supplied_previous_day.ids)])

        elif circulation_head:
            circulation_head.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('unit_name', 'in', circulation_head), ('id', 'in', indent_supplied_previous_day.ids)])

        elif circulation_admin:
            circulation_admin.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('unit_name', 'in', circulation_admin), ('id', 'in', indent_supplied_previous_day.ids)])
        elif regional_head:
            regional_head.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('unit_name', 'in', regional_head), ('id', 'in', indent_supplied_previous_day.ids)])
        elif unit_incharge:
            unit_incharge.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('unit_name', 'in', unit_incharge), ('id', 'in', indent_supplied_previous_day.ids)])
        elif circulation_incharge:
            circulation_incharge.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('unit_name', 'in', circulation_incharge), ('id', 'in', indent_supplied_previous_day.ids)])
        elif publications_incharge:
            publications_incharge.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('unit_name', 'in', publications_incharge), ('id', 'in', indent_supplied_previous_day.ids)])
        elif field_segment_incharge:
            field_segment_incharge.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('unit_name', 'in', field_segment_incharge), ('id', 'in', indent_supplied_previous_day.ids)])
        else:
            super_admin.append(user_id.partner_id.id)
            indent_demand_obj = self.env['sale.order'].search([('unit_name', '=', user_id.partner_id.id), ('id', 'in', indent_supplied_previous_day.ids)])

        indent_demand_list = []
        for indent in indent_demand_obj:

            if indent.state_duplicate == 'Demand':
                state_duplicate = 'draft'
            else:
                state_duplicate = ''

            indent_demand_list.append({
                'id': indent.id if indent.id else 0,
                'unit_id': indent.unit_name.id if indent.unit_name.id else 0,
                'unit_name': indent.unit_name.name if indent.unit_name.name else '',
                'create_date': indent.create_date if indent.create_date else '',
                'internal_order_number': indent.new_seq if indent.new_seq else '',
                'agent_copies': indent.agent_copies if indent.agent_copies else 0,
                'free_copies': indent.free_copies if indent.free_copies else 0,
                'postal_copies': indent.postal_copies if indent.postal_copies else 0,
                'voucher_copies': indent.postal_copies if indent.postal_copies else 0,
                'promotional_copies': indent.promotional_copies if indent.promotional_copies else 0,
                'correspondents_copies': indent.correspondents_copies if indent.correspondents_copies else 0,
                'office_copies': indent.office_copies if indent.office_copies else 0,
                'demand_changes': indent.demand_changes if indent.demand_changes else 0,
                'total_copies': indent.total_copies if indent.total_copies else 0,
                'status': state_duplicate
            })

        return indent_demand_list

    @restapi.method([(["/demand_request_approve"], "POST")], auth="user")
    def demand_request_approve(self):
        params = request.params
        sale_order_obj = self.env['demand.request'].sudo().browse(int(params.get('id')))
        sale_order_obj.sudo().action_approve()

        if params.get('id'):
            return "Success"

    @restapi.method([(["/return_request_approve"], "POST")], auth="user")
    def return_request_approve(self):
        params = request.params
        sale_order_obj = self.env['return.request.line'].sudo().browse(int(params.get('id')))
        sale_order_obj.sudo().approve_return_request()

        return "Success"






