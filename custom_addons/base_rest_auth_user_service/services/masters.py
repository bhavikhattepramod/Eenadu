from odoo.http import request, root
from odoo.service import security
from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
import logging
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
    _name = "partner.new_api.service.masters"
    _usage = "masters"
    _collection = "base_rest_auth_user_service.services"
    _description = """ """

    @restapi.method([(["/customer_details"], "GET")], auth="public")
    def customer_details(self):
        customer_det = []
        customer_names = self.env['res.partner'].search(
            [('is_newsprint_agent', '=', False), ('is_clearing_agent', '=', False)])
        for cust in customer_names:
            l10n_in_gst_treatment = ''
            if cust.l10n_in_gst_treatment == 'regular':
                l10n_in_gst_treatment = 'Registered Business - Regular'
            if cust.l10n_in_gst_treatment == 'composition':
                l10n_in_gst_treatment = 'Registered Business - Composition'
            elif cust.l10n_in_gst_treatment == 'unregistered':
                l10n_in_gst_treatment = 'Unregistered Business'
            elif cust.l10n_in_gst_treatment == 'consumer':
                l10n_in_gst_treatment = 'Consumer'
            elif cust.l10n_in_gst_treatment == 'overseas':
                l10n_in_gst_treatment = 'Overseas'
            elif cust.l10n_in_gst_treatment == 'special_economic_zone':
                l10n_in_gst_treatment = 'Special Economic Zone'
            elif cust.l10n_in_gst_treatment == 'deemed_export':
                l10n_in_gst_treatment = 'Deemed Export'
            elif cust.l10n_in_gst_treatment == 'uin_holders':
                l10n_in_gst_treatment = 'UIN Holders'

            customer_det.append({
                'id': cust.id if cust.id else 0,
                'name': cust.name if cust.name else '',
                'gst_treatment': l10n_in_gst_treatment,
                'mobile_number': cust.mobile if cust.mobile else '',
            })
        return customer_det

    @restapi.method([(["/pricelist"], "GET")], auth="public")
    def pricelist(self):
        price_dict = list()
        pricelist = self.env['product.pricelist'].search([])
        for price in pricelist:
            price_order = []
            classifieds_price_list = []
            for rec in price.item_ids:
                price_order.append({
                    'id': rec.id if rec.id else 0,
                    'product_id': rec.product_tmpl_id.id if rec.product_tmpl_id.id else 0,
                    'product_name': rec.product_tmpl_id.name if rec.product_tmpl_id.name else '',
                    'product_variants_id': rec.product_id.id if rec.product_id.id else rec.product_id.id,
                    'product_variants_name': rec.product_id.product_template_attribute_value_ids.name if rec.product_id.product_template_attribute_value_ids else rec.product_id.name,
                    'fixed_price': rec.fixed_price if rec.fixed_price else 0.0,
                    'publication_id': rec.publication_id.id if rec.publication_id.id else 0,
                    'publication_name': rec.publication_id.name if rec.publication_id.name else '',
                    'reta_regions_id': rec.reta_regions_id.id if rec.reta_regions_id.id else 0,
                    'reta_regions_name': rec.reta_regions_id.name if rec.reta_regions_id.name else '',
                })
            for line in price.classified_rate_o2m:
                classifieds_price_list.append({
                    'id': line.id if line.id else 0,
                    'product_id': line.product_id.id if line.product_id.id else 0,
                    'product_name': line.product_id.name if line.product_id.name else '',
                    'packages_id': line.packages.id if line.packages.id else 0,
                    'pricelist_id': line.pricelist_id.id if line.pricelist_id.id else 0,
                    'pricelist_name': line.pricelist_id.name if line.pricelist_id.name else '',
                    'packages_name': line.packages.name if line.packages.name else '',
                    'minimum_lines': line.minimum_lines if line.minimum_lines else 0,
                    'minimum_lines_price': line.minimum_lines_price if line.minimum_lines_price else 0,
                    'additional_line_price': line.additional_line_price if line.additional_line_price else 0,
                    'classified_regions_id': line.regions_id.id if line.regions_id.id else 0,
                    'classified_regions_name': line.regions_id.name if line.regions_id.name else '',
                })
            price_dict.append({
                'id': price.id if price.id else 0,
                'pricelist_name': price.name if price.name else '',
                'order_lines': price_order,
                'classifieds_price_list': classifieds_price_list
            })
        return price_dict

    @restapi.method([(["/quotation_template"], "GET")], auth="public")
    def quotation_template(self):
        pay_dict = list()
        quotation_template = self.env['sale.order.template'].search([])
        order_lines = self.env['sale.order.template.line'].search([])
        order = []
        for rec in order_lines:
            order.append({
                'product_name': rec.product_id.name if rec.product_id.name else '',
                'description': rec.name if rec.name else '',
                'quantity': rec.product_uom_qty if rec.product_uom_qty else 0,
                'unit_of_measure': rec.product_uom_id.name if rec.product_uom_id.name else ''
            })
        for quotation in quotation_template:
            pay_dict.append({
                'id': quotation.id if quotation.id else 0,
                'name': quotation.name if quotation.name else '',
                'quotation_expires_after': quotation.number_of_days if quotation.number_of_days else '',
                'confirmation_mail': quotation.mail_template_id.name if quotation.mail_template_id.name else '',
                'product': order
            })
        return pay_dict

    @restapi.method([(["/products"], "GET")], auth="public")
    def products(self):
        prod_list = []
        categ_obj = self.env['product.category'].search([('name', '=', 'Reta')])
        products = self.env['product.template'].search([('categ_id', '=', categ_obj.id)])
        for prod in products:
            product_variants_obj = self.env['product.product'].search([('product_tmpl_id', '=', prod.id)])
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
                'description': prod.name if prod.name else '',
                "unit_of_measure_id": prod.uom_id.id if prod.uom_id.id else 0,
                "unit_of_measure": prod.uom_id.name if prod.uom_id.name else '',
                "customer_taxes": tax_list,
                'product_variants': attributes
            })
        return prod_list

    @restapi.method([(["/classified_products"], "GET")], auth="public")
    def classified_products(self):
        prod_list = []
        categ_obj = self.env['product.category'].search([('name', '=', 'Classifieds')])
        products = self.env['product.template'].search([('categ_id', '=', categ_obj.id)])
        for prod in products:
            product_variants_obj = self.env['product.product'].search([('product_tmpl_id', '=', prod.id)])
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
                'description': prod.name,
                "unit_of_measure_id": prod.uom_id.id if prod.uom_id.id else 0,
                "unit_of_measure": prod.uom_id.name if prod.uom_id.name else '',
                "customer_taxes": tax_list,
                'product_variants': attributes
            })
        return prod_list

    @restapi.method([(["/payment_terms"], "GET")], auth="public")
    def payment_terms(self):
        payment_list = []
        payment_terms = self.env['account.payment.term'].search([])
        for payment in payment_terms:
            payment_list.append({
                'id': payment.id if payment.id else 0,
                'name': payment.name if payment.name else ''
            })
        return payment_list

    @restapi.method([(["/ads_packages"], "GET")], auth="public")
    def ads_packages(self):
        package_list = []
        ad_packages_obj = self.env['ads.packages'].search([])
        for package in ad_packages_obj:
            package_list.append({
                'id': package.id if package.id else 0,
                'name': package.name if package.name else ''
            })
        return package_list

    @restapi.method([(["/unit_of_measure"], "GET")], auth="public")
    def unit_of_measure(self):
        uom_dict = list()
        unit_of_measure = self.env['uom.uom'].search([])
        for uom in unit_of_measure:
            uom_dict.append({
                'id': uom.id if uom.id else 0,
                'name': uom.name if uom.name else '',
                'category': uom.category_id.name if uom.category_id.name else '',
                'indian_gst_uqc': uom.l10n_in_code if uom.l10n_in_code else '',
                'type': uom.uom_type if uom.uom_type else '',
                'ration': uom.factor if uom.factor else '',
                'rounding': uom.rounding if uom.rounding else ''
            })
        return uom_dict

    @restapi.method([(["/account_deposit"], "GET")], auth="public")
    def account_deposit(self):
        account_dep = []
        user_id = self.env.user
        account = self.env['account.deposit'].search([('partner_id', '=', user_id.partner_id.id)])

        for deposit in account:
            order = []
            order_lines = self.env['deposit.outstanding'].search([])
            for rec in order_lines:
                order.append({
                    'period': rec.periodd if rec.periodd else '',
                    'actual_amount': rec.actual_amt if rec.actual_amt else 0.0,
                    'interest_amount': rec.interest_amt if rec.interest_amt else 0.0,
                    'outstanding_amount': rec.outstanding_amt if rec.outstanding_amt else 0.0
                })
            account_dep.append({
                'id': deposit.id if deposit.id else 0,
                'partner': deposit.partner_id.name if deposit.partner_id.name else '',
                'deposit_amount': deposit.deposit_amt if deposit.deposit_amt else 0.0,
                'interest_percentage': deposit.interest_percent if deposit.interest_percent else 0.0,
                'total_outstanding': deposit.total_outstanding if deposit.total_outstanding else 0.0,
                'partial_payment_pending': deposit.remaining_amount_payment if deposit.remaining_amount_payment else 0.0,
                'order_lines': order
            })
        return account_dep

    @restapi.method([(["/sale_document_type"], "GET")], auth="public")
    def sale_document_type(self):
        sale = []
        sale_document = self.env['sale.document.type'].search([])
        for sales in sale_document:
            sale.append({
                'id': sales.id if sales.id else 0,
                'name': sales.name if sales.name else ''
            })
        return sale

    @restapi.method([(["/page_details"], "GET")], auth="public")
    def page_details(self):
        page_det = []
        pages = self.env['newspaper.page.details'].search([])
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

        return page_det

    @restapi.method([(["/unit_details"], "GET")], auth="public")
    def unit_details(self):
        unit_det = []
        units = self.env['unit.master'].search([])

        for unit in units:
            unit_det.append({
                'id': unit.id if unit.id else 0,
                'unit_code': unit.unit_code if unit.unit_code else '',
                'unit_name': unit.name if unit.name else '',
                'unit_address': unit.unit_address if unit.unit_address else '',
                'pincode': int(unit.pincode) if unit.pincode else 0,
                'unit_incharge1': unit.unit_incharge1.name if unit.unit_incharge1 else '',
                'unit_incharge2': unit.unit_incharge2.name if unit.unit_incharge2 else '',
            })
        return unit_det

    @restapi.method([(["/region_details"], "GET")], auth="public")
    def region_details(self):
        regions_det = []
        regions_obj = self.env['reta.regions'].search([])

        for region in regions_obj:
            if region.sale_type == 'main':
                sale_type = 'Main'
            elif region.sale_type == 'mini':
                sale_type = 'Mini'
            else:
                sale_type = ''

            if region.advertising_region_type == 'region':
                advertising_region_type = 'Region'
            elif region.advertising_region_type == 'edition':
                advertising_region_type = 'Editions'
            elif region.advertising_region_type == 'district':
                advertising_region_type = 'District'
            elif region.advertising_region_type == 'clusters':
                advertising_region_type = 'Clusters'
            elif region.advertising_region_type == 'combined':
                advertising_region_type = 'Combination'
            else:
                advertising_region_type = ''

            regions_det.append({
                'id': region.id if region.id else 0,
                'name': region.name if region.name else '',
                'base_price': region.base_price if region.base_price else 0.00,
                'sale_type': sale_type,
                'adv_region_type': advertising_region_type,
            })
        return regions_det

    @restapi.method([(["/publication_details"], "GET")], auth="public")
    def publication_details(self):
        publication_det = []
        publication_obj = self.env['publication.details'].search([])

        for publication in publication_obj:
            pub_det = []
            for pub in publication.related_publications:
                pub_det.append({
                    'id': pub.id if pub.id else 0,
                    'name': pub.name if pub.name else ''
                })
            publication_det.append({
                'id': publication.id if publication.id else 0,
                'name': publication.name if publication.name else '',
                'related_publications': pub_det
            })
        return publication_det

    @restapi.method([(["/advertisement_position"], "GET")], auth="public")
    def advertisement_position(self):
        advt = []
        advertisement = self.env['advertisement.position'].search([])
        for add in advertisement:
            advt.append({
                'id': add.id if add.id else 0,
                'name': add.name if add.name else ''
            })
        return advt

    @restapi.method([(["/taxes"], "GET")], auth="public")
    def taxes(self):
        tax_dict = list()
        order_lines = self.env['account.tax'].search([])
        order = []
        for tax in order_lines:
            order.append({
                'id': tax.id if tax.id else 0,
                'tax_name': tax.name if tax.name else '',
                'tax_computation': tax.amount_type if tax.amount_type else '',
                'amount': tax.amount if tax.amount else 0.0
            })
        return tax_dict

    @restapi.method([(["/get_user_role"], "GET")], auth="public")
    def get_user_role(self):
        user_id = self.env.user
        employee_obj = self.env['hr.employee'].search([('user_partner_id', '=', user_id.partner_id.id)],
                                                             limit=1)

        return employee_obj.job_id.name

    @restapi.method([(["/display_target_lines/<int:rec_id>"], "GET")], auth="public")
    def display_target_lines(self, rec_id):
        employee_obj = self.env['hr.employee'].search([('id', '=', rec_id)], limit=1)
        emp_child_obj = self.env['hr.employee'].search(
            [('parent_id', '=', employee_obj.id), ('id', '!=', employee_obj.id)])
        target_obj = self.env['partner.incentive.line'].search(
            [('employee_id', '=', employee_obj.id)])

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
                'target_amount': target.target_amt if target.target_amt else 0.0,
                'ro_total_amount': target.so_total_amt if target.so_total_amt else 0.0,
                'recieved_payment': target.recieved_payment if target.recieved_payment else 0.0,
                'progress': str(target.progress) + ' %',
            })

        user_list = []
        user_list_role = ''
        for child_emp in emp_child_obj:
            user_list_role = child_emp.job_id.name if user_list_role.job_id.name else ''
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })

        for child_emp in emp_child_obj:
            user_list.append({
                'id': child_emp.id if child_emp.id else 0,
                'name': child_emp.name if child_emp.name else ''
            })
        if rec_id:
            target_line_vals = {
                'target_lines': [{
                    'id': employee_obj.id if employee_obj.id else 0,
                    'name': employee_obj.name if employee_obj.name else '',
                    'user_role': employee_obj.job_id.name if employee_obj.job_id else '',
                    'target': target_lines
                }],
                'user_list_role': user_list_role,
                'user_list': user_list,
            }
            return target_line_vals
        else:
            return {"error": ''}

    @restapi.method([(["/state"], "GET")], auth="public")
    def state(self):
        state_list = []
        state_obj = self.env['res.country.state'].search([('country_id', '=', 'IN')])

        for state in state_obj:
            state_list.append({
                "id": state.id if state.id else 0,
                "name": state.name if state.name else ''
            })
        return state_list

    @restapi.method([(["/country"], "GET")], auth="public")
    def country(self):
        country_list = []
        country_obj = self.env['res.country'].search([('code', '=', 'IN')])
        for country in country_obj:
            country_list.append({
                "id": country.id if country.id else 0,
                "name": country.name if country.name else '',
                "code": country.code if country.code else ''
            })
        return country_list

    @restapi.method([(["/district"], "GET")], auth="public")
    def district(self):
        district_list = []
        district_obj = self.env['res.state.district'].search([])
        for district in district_obj:
            district_list.append({
                "state_id": district.state_id.id if district.state_id.id else 0,
                "state_name": district.state_id.name if district.state_id.name else '',
                "id": district.id if district.id else 0,
                "name": district.name if district.name else ''
            })
        return district_list

    @restapi.method([(["/sale_category"], "GET")], auth="public")
    def sale_category(self):
        sale_category_list = []
        cate_obj = self.env['sale.category'].search([])
        for category in cate_obj:
            sale_category_list.append({
                'id': category.id if category.id else 0,
                'name': category.name if category.name else '',
                'parent_category_id': category.parent_category.id if category.parent_category.id else 0,
                'parent_category': category.parent_category.name if category.parent_category.name else '',

            })
        return sale_category_list

    @restapi.method([(["/multi_discount"], "GET")], auth="public")
    def multi_discount(self):
        multi_discount_list = []
        discount_obj = self.env['multi.discount'].search([])
        for discount in discount_obj:
            multi_discount_list.append({
                'id': discount.id if discount.id else 0,
                'name': discount.name if discount.name else '',
                'is_multi_region': discount.is_multi_region,
                'is_multi_edition': discount.is_multi_edition,
                'is_multi_zone': discount.is_multi_zone,
                'discount': discount.discount if discount.discount else 0.0,
                'second_hightest_discount': discount.second_hightest_discount if discount.second_hightest_discount else 0.0,
                'third_hightest_discount': discount.third_hightest_discount if discount.third_hightest_discount else 0.0,
            })
        return multi_discount_list

    @restapi.method([(["/category_discount"], "GET")], auth="public")
    def category_discount(self):
        category_discount_list = []
        category_obj = self.env['category.discount'].search([])
        for discount in category_obj:
            if discount.category_type == 'repetitive':
                category_type = 'Repetitive'
            elif discount.category_type == 'non_repetitive':
                category_type  = 'Non-Repetitive'
            category_discount_list.append({
                'id': discount.id if discount.id else 0,
                'name': discount.name if discount.name else '',
                'category_type': category_type,
                'max_discount': discount.max_discount if discount.max_discount else 0.00,
            })
        return category_discount_list

    @restapi.method([(["/area"], "GET")], auth="public", cors="*")
    def area(self):
        area_list = []
        httprequest = request.httprequest
        headers = dict(httprequest.headers)
        area_obj = self.env['area.area'].search([])
        for area in area_obj:
            area_list.append({
                'id': area.id if area.id else 0,
                'name': area.name if area.name else '',
                'parent_id': area.parent_name.id if area.parent_name.id else 0,
                'parent_name': area.parent_name.name if area.parent_name.name else '',
            })
        return area_list
