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
    _name = "partner.new_api.service"
    _usage = "partner"
    _collection = "base_rest_auth_user_service.services"
    _description = """
        Partner New API Services
        Services developed with the new api provided by base_rest
    """


    @restapi.method([(["/create_customer"], "POST")], auth="public")
    def create_customer(self):
        params = request.params
        state = self.env['res.country.state'].search([('name', '=', params.get('state_id'))])
        district = self.env['res.state.district'].search([('name', '=', params.get('district_id'))])
        country = self.env['res.country'].search([('name', '=', params.get('country_id'))])

        company_type = ""
        if params.get('company_type') == 'Individual':
            company_type += 'person'
        elif params.get('company_type') == 'Company':
            company_type += 'company'
        l10n_in_gst_treatment = ''
        if params.get('l10n_in_gst_treatment') == 'Registered Business - Regular':
            l10n_in_gst_treatment += 'regular'
        if params.get('l10n_in_gst_treatment') == 'Registered Business - Composition':
            l10n_in_gst_treatment += 'composition'
        elif params.get('l10n_in_gst_treatment') == 'Unregistered Business':
            l10n_in_gst_treatment += 'unregistered'
        elif params.get('l10n_in_gst_treatment') == 'Consumer':
            l10n_in_gst_treatment += 'consumer'
        elif params.get('l10n_in_gst_treatment') == 'Overseas':
            l10n_in_gst_treatment += 'overseas'
        elif params.get('l10n_in_gst_treatment') == 'Special Economic Zone':
            l10n_in_gst_treatment += 'special_economic_zone'
        elif params.get('l10n_in_gst_treatment') == 'Deemed Export':
            l10n_in_gst_treatment += 'deemed_export'
        elif params.get('l10n_in_gst_treatment') == 'UIN Holders':
            l10n_in_gst_treatment += 'uin_holders'

        customer_list = {
            'company_name': params.get('company_name'),
            # 'cust_seq': params.get('cust_seq'),
            'company_type': company_type,
            'name': params.get('name'),
            'l10n_in_gst_treatment': l10n_in_gst_treatment,
            'street': params.get('street'),
            'street2': params.get('street2'),
            'city': params.get('city'),
            'district_id': district.id,
            'state_id': params.get('state_id'),
            'country_id': country.id,
            'zip': params.get('zip'),
            'l10n_in_pan': params.get('l10n_in_pan'),
            'phone': params.get('phone'),
            'mobile': params.get('mobile'),
            'email': params.get('email'),
            'website': params.get('website'),
            'vat': params.get('vat'),
            'gst_verified': params.get('gst_verified'),
            'gst_status': params.get('gst_status')
        }
        if params.get('mobile') != '':
            gst_treatment = self.env['res.partner'].sudo().search([('mobile', '=', params.get('mobile'))])
        else:
            return "Please fill Mobile Number"
        
        if gst_treatment:
            return "Customer Already Existing"
        else:
            customer = self.env['res.partner'].sudo().create(customer_list)
            return {
                "id": customer.id,
                "Status": "Customer has been created successfully"
            }

    @restapi.method([(["/update_customer"], "PATCH")], auth="public")
    def update_customer(self):
        params = request.params
        record_id = self.env['res.partner'].search([('id', "=", params.get('id'))])
        state = self.env['res.country.state'].search([('name', '=', params.get('state_id'))])
        district = self.env['res.state.district'].search([('name', '=', params.get('district_id'))])
        country = self.env['res.country'].search([('name', '=', params.get('country_id'))])
        team = self.env['crm.team'].search([('name', '=', params.get('team_id'))])
        payment_terms = self.env['account.payment.term'].search(
            [('name', '=', params.get('property_payment_term_id'))])
        company_type = ""
        if params.get('company_type') == 'Individual':
            company_type += 'person'
        elif params.get('company_type') == 'Company':
            company_type += 'company'
        l10n_in_gst_treatment = ""
        if params.get('l10n_in_gst_treatment') == 'Registered Business - Regular':
            l10n_in_gst_treatment += 'regular'
        if params.get('l10n_in_gst_treatment') == 'Registered Business - Composition':
            l10n_in_gst_treatment += 'composition'
        elif params.get('l10n_in_gst_treatment') == 'Unregistered Business':
            l10n_in_gst_treatment += 'unregistered'
        elif params.get('l10n_in_gst_treatment') == 'Consumer':
            l10n_in_gst_treatment += 'consumer'
        elif params.get('l10n_in_gst_treatment') == 'Overseas':
            l10n_in_gst_treatment += 'overseas'
        elif params.get('l10n_in_gst_treatment') == 'Special Economic Zone':
            l10n_in_gst_treatment += 'special_economic_zone'
        elif params.get('l10n_in_gst_treatment') == 'Deemed Export':
            l10n_in_gst_treatment += 'deemed_export'
        else:
            l10n_in_gst_treatment += 'uin_holders'

        record_id.company_type = company_type
        record_id.name = params.get('name')
        record_id.l10n_in_gst_treatment = l10n_in_gst_treatment
        record_id.street = params.get('street')
        record_id.street2 = params.get('street2')
        record_id.city = params.get('city')
        record_id.district_id = district.id
        record_id.state_id = state.id
        record_id.country_id = country.id
        record_id.zip = params.get('zip')
        record_id.l10n_in_pan = params.get('l10n_in_pan')
        record_id.phone = params.get('phone')
        record_id.mobile = params.get('mobile')
        record_id.email = params.get('email')
        record_id.website = params.get('website')
        record_id.vat = params.get('vat')
        record_id.team_id = team.id,
        record_id.property_payment_term_id = payment_terms.id,

        return {"Status": "Details Updated successfully"}

    @restapi.method([(["/job_applications"], "POST")], auth="public")
    def job_applications(self):
        params = request.params
        degree = self.env['hr.recruitment.degree'].search([('name', '=', params.get('type_id'))])
        job_id = self.env['hr.job'].search([('name', '=', params.get('job_id'))])
        title = ""
        if params.get('title') == 'Dr':
            title += 'dr'
        elif params.get('title') == 'Ms':
            title += 'ms'
        elif params.get('title') == 'Mrs':
            title += 'mrs'
        else:
            title += 'mrs'
        Attachments = request.env['ir.attachment']
        att_bin = params['attachement_id1']
        attachment_id = Attachments.sudo().create({
            'name': params.get('name') + ' ' + 'resume',
            # 'res_name': 'name',
            'type': 'binary',
            'res_model': 'hr.applicant',
            'public': True,
            'datas': att_bin,
        })
        candidate_list = {
            'name': params.get('name'),
            'title': title,
            'partner_name': params.get('partner_name'),
            'email_from': params.get('email_from'),
            'location': params.get('location'),
            'partner_mobile': params.get('partner_mobile'),
            'job_id': job_id.id,
            'type_id': degree.id,
            'attachement_id1': attachment_id,
        }
        job = self.env['hr.applicant'].sudo().create(candidate_list)
        return {"Status": "Success", "id": job.id}

    @restapi.method([(["/job_positions"], "GET")], auth="public")
    def job_positions(self):
        position_list = []
        positions = self.env['hr.job'].search([])
        for addr in positions:
            address = str(addr.address_id.street if addr.address_id.street else ' ') + ' ' + str(
                addr.address_id.street2 if addr.address_id.street2 else ' ') + ' ' + str(
                addr.address_id.city if addr.address_id.city else ' ') + ' ' + str(
                addr.address_id.country_id.name if addr.address_id.country_id.name else ' ')

        for pos in positions:
            position_list.append({
                'id': pos.id,
                'job position': pos.name,
                'department': pos.department_id.name,
                'company name': pos.address_id.name,
                'job location': address,
                'number of openings': pos.no_of_recruitment,
                'website published': pos.website_published,
                'recruiter': pos.user_id.name,
            })
        return {"Job Position": position_list}
