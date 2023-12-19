from odoo.http import request, root
from odoo.service import security
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
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
    _name = "partner.new_api.service.scheduling"
    _usage = "scheduling"
    _collection = "base_rest_auth_user_service.services"
    _description = """ """

    @restapi.method([(["/filter_params"], "GET")], auth="public", cors="*")
    def filter_params(self):
        advt = []
        page_det = []
        values = []
        prod_list = []
        nap_list = []
        reta_list = []
        current_date = datetime.now().date()
        tomorrow_date = current_date + timedelta(days=1)

        categ_obj = self.env['product.category'].sudo().search([('name', '=', 'Reta')])
        products = self.env['product.template'].sudo().search([('categ_id', '=', categ_obj.id)])
        advertisement = self.env['advertisement.position'].sudo().search([])
        pages = self.env['newspaper.page.details'].sudo().search([])
        nap_obj = self.env['nap.scheduling.details'].sudo().search([('source', '=', 'nap')])
        # ('publish_date', '=', tomorrow_date)
        reta_obj = self.env['nap.scheduling.details'].sudo().search([('source', '=', 'reta')])

        for reta in reta_obj:

            reta_product_name = ''
            reta_prod_id = 0
            for nap_prod in reta.product_id:
                reta_product_name = nap_prod.name + ' ' + '(' + nap_prod.product_template_attribute_value_ids.name + ')'

            # Concatenate the values of field1 and field2
            if reta.page_no:
                display_name = f"{reta.page_no.name} - {reta.page_no.page_name}"
            else:
                display_name = reta.page_no.name
            reta_list.append({
                'id': reta.id,
                'ad_type_id': reta_prod_id,
                'ad_type': reta_product_name,
                'page_id': reta.page_no.id,
                'page_name': display_name,
                'position_id': reta.ad_position.id if reta.ad_position.id else 0,
                'position_name': reta.ad_position.name if reta.ad_position.name else '',
                'publish_date': reta.publish_date if reta.publish_date else '',
                'edition_type': reta.edition_type,
                'paper_number': reta.paper_number,
                'ad_template': reta.ad_template,
                'dummy_chart_position_x': reta.dummy_chart_position_x if reta.dummy_chart_position_x else '',
                'dummy_chart_position_y': reta.dummy_chart_position_y if reta.dummy_chart_position_y else '',
                'size': reta.size if reta.size else '',

            })

        for nap in nap_obj:
            nap_product_name = ''
            nap_prod_id = 0
            for nap_prod in nap.product_id:
                    nap_product_name = nap_prod.name + ' ' + '(' + nap_prod.product_template_attribute_value_ids.name + ')'

            # Concatenate the values of field1 and field2
            if nap.page_no:
                display_name = f"{nap.page_no.name} - {nap.page_no.page_name}"
            else:
                display_name = nap.page_no.name

            nap_list.append({
                'id':nap.id if nap.id else 0,
                'ad_type_id': nap_prod_id,
                'ad_type': nap_product_name,
                'page_id':nap.page_no.id,
                'page_name': display_name,
                'position_id': nap.ad_position.id if nap.ad_position.id else 0,
                'position_name': nap.ad_position.name if nap.ad_position.name else '',
                'publish_date': nap.publish_date if nap.publish_date else '',
                'edition_type': nap.edition_type,
                'paper_number': nap.paper_number,
                'ad_template': nap.ad_template,
                'dummy_chart_position_x':nap.dummy_chart_position_x if nap.dummy_chart_position_x else '',
                'dummy_chart_position_y':nap.dummy_chart_position_y if nap.dummy_chart_position_y else '',
                'size': nap.size if nap.size else '',
            })

        for record in pages:
            display_name = ''
            # Concatenate the values of field1 and field2
            if record.page_name:
                display_name += f"{record.name} - {record.page_name}"
            else:
                display_name += record.name

            page_det.append({
                'id': record.id if record.id else 0,
                'page_name': display_name,
            })

        for add in advertisement:
            advt.append({
                'id': add.id if add.id else 0,
                'name': add.name if add.name else ''
            })

        for prod in products:
            product_variants_obj = self.env['product.product'].sudo().search([('product_tmpl_id', '=', prod.id)])
            tax_list = []
            for tax in prod.taxes_id:
                tax_list.append({
                    'tax_id': tax.id if tax.id else 0,
                    'tax_name': tax.name if tax.name else ''
                })

            attributes = []
            for variant in product_variants_obj:
                attributes.append({
                    'id': variant.id if variant.id else 0,
                    'name': variant.product_template_attribute_value_ids.name if variant.product_template_attribute_value_ids else variant.name
                })
            prod_list.append({
                'id': prod.id if prod.id else 0,
                "name": prod.name if prod.name else '',
            })

        values.append({
            'ad_type': prod_list,
            'page_number': page_det,
            'position': advt,
            'nap': nap_list,
            'reta': reta_list
        })

        return {
            'data': values
        }

    @restapi.method([(["/fetch_dummy_chart"], "POST")], auth="public",cors="*")
    def fetch_dummy_chart(self):
        params = request.params

        if params.get('edition_type') and params.get('paper_number'):
            scheduling_position = self.env['nap.scheduling.details'].sudo().search([
                ('page_no', '=', params.get('page_id')), 
                ('publish_date', '=', str(params.get('publish_date'))),
                ('edition_type', '=', params.get('edition_type')),
                ('paper_number', '=', params.get('paper_number'))
                ])
        else:            
            scheduling_position = self.env['nap.scheduling.details'].sudo().search([
                ('page_no', '=', params.get('page_id')), 
                ('publish_date', '=', str(params.get('publish_date')))
                ])

        values = []
        for scheduling in scheduling_position:
            if scheduling.edition_type == 'single':
                edition_type = 'single'
            elif scheduling.edition_type == 'twin':
                edition_type = 'twin'
            else:
                edition_type = ''

            if scheduling.paper_number == 'one':
                paper_number = 'one'
            elif scheduling.paper_number == 'two':
                paper_number = 'two'
            else:
                paper_number = ''

            if scheduling.ad_template == 'template_1':
                ad_template = 'template_1'
            elif scheduling.ad_template == 'template_2':
                ad_template = 'template_2'
            elif scheduling.ad_template == 'template_3':
                ad_template = 'template_3'
            else:
                ad_template = ''

            if params.get('position_id') and params.get('ad_type_id'):
                if params.get('position_id') == scheduling.ad_position.id and params.get(
                        'ad_type_id') == scheduling.product_id.id:
                    if scheduling.page_no:
                        page_name = f"{scheduling.page_no.name} - {scheduling.page_no.page_name}"
                    else:
                        page_name = scheduling.page_no.name
                    values.append({
                        'id': scheduling.id,
                        'ad_type_id': scheduling.product_id.id if scheduling.product_id.id else 0,
                        'ad_type': scheduling.product_id.name if scheduling.product_id.name else '',
                        'page_id': scheduling.page_no.id if scheduling.page_no.id else 0,
                        'page_name': page_name if page_name else '',
                        'position_id': scheduling.ad_position.id if scheduling.ad_position.id else 0,
                        'position_name': scheduling.ad_position.name if scheduling.ad_position.name else '',
                        'publish_date': scheduling.publish_date if scheduling.publish_date else '',
                        'size': scheduling.size if scheduling.size else '',
                        'dummy_chart_position_x': scheduling.dummy_chart_position_x if scheduling.dummy_chart_position_x else '',
                        'dummy_chart_position_y': scheduling.dummy_chart_position_y if scheduling.dummy_chart_position_y else '',
                        'edition_type': edition_type,
                        'paper_number': paper_number,
                        'ad_template':ad_template
                    })

            elif params.get('position_id'):
                if params.get('position_id') == scheduling.ad_position.id:
                    if scheduling.page_no:
                        page_name = f"{scheduling.page_no.name} - {scheduling.page_no.page_name}"
                    else:
                        page_name = scheduling.page_no.name
                    values.append({
                        'id': scheduling.id,
                        'ad_type_id': scheduling.product_id.id if scheduling.product_id.id else 0,
                        'ad_type': scheduling.product_id.name if scheduling.product_id.name else '',
                        'page_id': scheduling.page_no.id if scheduling.page_no.id else 0,
                        'page_name': page_name if page_name else '',
                        'position_id': scheduling.ad_position.id if scheduling.ad_position.id else 0,
                        'position_name': scheduling.ad_position.name if scheduling.ad_position.name else '',
                        'publish_date': scheduling.publish_date if scheduling.publish_date else '',
                        'size': scheduling.size if scheduling.size else '',
                        'dummy_chart_position_x': scheduling.dummy_chart_position_x if scheduling.dummy_chart_position_x else '',
                        'dummy_chart_position_y': scheduling.dummy_chart_position_y if scheduling.dummy_chart_position_y else '',
                        'edition_type': edition_type,
                        'paper_number': paper_number,
                        'ad_template':ad_template
                    })
            elif params.get('ad_type_id'):
                if params.get('ad_type_id') == scheduling.product_id.id:
                    if scheduling.page_no:
                        page_name = f"{scheduling.page_no.name} - {scheduling.page_no.page_name}"
                    else:
                        page_name = scheduling.page_no.name
                    values.append({
                        'id': scheduling.id,
                        'ad_type_id': scheduling.product_id.id if scheduling.product_id.id else 0,
                        'ad_type': scheduling.product_id.name if scheduling.product_id.name else '',
                        'page_id': scheduling.page_no.id if scheduling.page_no.id else 0,
                        'page_name': page_name if page_name else '',
                        'position_id': scheduling.ad_position.id if scheduling.ad_position.id else 0,
                        'position_name': scheduling.ad_position.name if scheduling.ad_position.name else '',
                        'publish_date': scheduling.publish_date if scheduling.publish_date else '',
                        'size': scheduling.size if scheduling.size else '',
                        'dummy_chart_position_x': scheduling.dummy_chart_position_x if scheduling.dummy_chart_position_x else '',
                        'dummy_chart_position_y': scheduling.dummy_chart_position_y if scheduling.dummy_chart_position_y else '',
                        'edition_type': edition_type,
                        'paper_number': paper_number,
                        'ad_template':ad_template
                    })
            else:
                if scheduling.page_no:
                    page_name = f"{scheduling.page_no.name} - {scheduling.page_no.page_name}"
                else:
                    page_name = scheduling.page_no.name
                values.append({
                    'id': scheduling.id,
                    'ad_type_id': scheduling.product_id.id if scheduling.product_id.id else 0,
                    'ad_type': scheduling.product_id.name if scheduling.product_id.name else '',
                    'page_id': scheduling.page_no.id if scheduling.page_no.id else 0,
                    'page_name': page_name if page_name else '',
                    'position_id': scheduling.ad_position.id if scheduling.ad_position.id else 0,
                    'position_name': scheduling.ad_position.name if scheduling.ad_position.name else '',
                    'publish_date': scheduling.publish_date if scheduling.publish_date else '',
                    'size': scheduling.size if scheduling.size else '',
                    'dummy_chart_position_x': scheduling.dummy_chart_position_x if scheduling.dummy_chart_position_x else '',
                    'dummy_chart_position_y': scheduling.dummy_chart_position_y if scheduling.dummy_chart_position_y else '',
                    'edition_type': edition_type,
                    'paper_number': paper_number,
                    'ad_template': ad_template
                })

        return values

    @restapi.method([(["/post_dummy_chart"], "POST")], auth="public",cors="*")
    def post_dummy_chart(self):

        params = request.params

        scheduling_details = params.get('scheduling_details')
        
        scheduling_list = []
        for sched in scheduling_details:
            scheduling_obj = self.env['nap.scheduling.details'].sudo().browse(int(sched['id']))

            scheduling_obj.page_no = sched['page_id']
            scheduling_obj.paper_number = sched['paper_number']
            scheduling_obj.edition_type = sched['edition_type']
            scheduling_obj.dummy_chart_position_x = sched['dummy_chart_position_x']
            scheduling_obj.dummy_chart_position_y = sched['dummy_chart_position_y']
            scheduling_obj.ad_template = sched['ad_template']

            scheduling_list.append({
                "id": sched['id'],
                "Status": "Success"
                })
        if request.session.sid:
            return scheduling_list
