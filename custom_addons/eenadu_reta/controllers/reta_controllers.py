from odoo import http
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import fields, http, _
from dateutil.relativedelta import relativedelta
from odoo.tools import date_utils
from odoo.http import request
from collections import OrderedDict
from odoo.osv.expression import AND, OR


class RetaControllers(http.Controller):

    @http.route(['/agent_commission', '/agent_commission/page/<int:page>'], type='http', auth="user", website=True)
    def agent_commission(self, page=1, search="", filterby=None, search_in="All", sortby="id", groupby="none"):
        user = request.env.uid
        user_id = request.env['res.users'].browse(user)
        values = {}
        reta_order = []
        reta_orders = request.env['reta.orders'].search([])
        invoices = request.env['account.move'].search([('user_id', "=", user_id.id)])
        comm = request.env['commission.settlement'].search([('agent_id', "=", user_id.partner_id.id)])
        search_list = {
            'All': {'label': 'All', 'input': 'all', 'domain': []}
        }
        search_domain = search_list[search_in]
        total_reta_orders = reta_orders.sudo().search_count([])
        state = ''
        commission = ''
        invoice_state = ''
        domain = request.env['reta.orders']

        for i in comm:
            commission = i.invoice_id.name
        for invoice in invoices:
            invoice_state = invoice.state

        if invoice_state == 'draft':
            state += 'Draft'
        elif invoice_state == 'posted':
            state += 'Posted'

        if comm:
            for orders in reta_orders:
                reta_order.append({
                    'reta_orders': orders.reta_order,
                    'date': orders.date,
                    'total_amt': orders.total_amt,
                    'amount_paid': orders.amount_paid,
                    'commission': orders.commission,
                    # 'invoice_id': orders.invoice_id,
                    'bill_number': commission,
                    'status': state
                })

        sorted_list = {
            'date': {'label': 'Date', 'order': 'date'},
            'name': {'label': 'Name', 'order': 'name'}
        }

        today = fields.Date.today()
        quarter_start, quarter_end = date_utils.get_quarter(today)
        last_week = today + relativedelta(weeks=-1)
        last_month = today + relativedelta(months=-1)
        last_year = today + relativedelta(years=-1)

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'today': {'label': _('Today'), 'domain': [("date", "=", today)]},
            'week': {'label': _('This week'), 'domain': [('date', '>=', date_utils.start_of(today, "week")),
                                                         ('date', '<=', date_utils.end_of(today, 'week'))]},
            'month': {'label': _('This month'), 'domain': [('date', '>=', date_utils.start_of(today, 'month')),
                                                           ('date', '<=', date_utils.end_of(today, 'month'))]},
            'year': {'label': _('This year'), 'domain': [('date', '>=', date_utils.start_of(today, 'year')),
                                                         ('date', '<=', date_utils.end_of(today, 'year'))]},
            'quarter': {'label': _('This Quarter'),
                        'domain': [('date', '>=', quarter_start), ('date', '<=', quarter_end)]},
            'last_week': {'label': _('Last week'), 'domain': [('date', '>=', date_utils.start_of(last_week, "week")),
                                                              ('date', '<=', date_utils.end_of(last_week, 'week'))]},
            'last_month': {'label': _('Last month'),
                           'domain': [('date', '>=', date_utils.start_of(last_month, 'month')),
                                      ('date', '<=', date_utils.end_of(last_month, 'month'))]},
            'last_year': {'label': _('Last year'), 'domain': [('date', '>=', date_utils.start_of(last_year, 'year')),
                                                              ('date', '<=', date_utils.end_of(last_year, 'year'))]},
        }

        if not filterby:
            filterby = 'all'
        # domain = AND([domain, searchbar_filters[filterby]['domain']])

        groupby_list = {
            'none': {'input': 'none', 'label': _('None'), "order": 1},
        }

        page_details = portal_pager(
            url='/agent_commission',
            total=total_reta_orders,
            page=page,
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'groupby': groupby,
                      'filterby': filterby},
            step=5,
        )

        orders = reta_orders.sudo().search([], limit=5, offset=page_details['offset'])
        values.update({
            'reta_orders': orders,
            'orders': reta_order,
            'page_name': 'agent_commission',
            'pager': page_details,
            # 'default_url': '/agent_commission',
            # 'groupby': groupby,
            # 'sortby': sortby,
            # 'searchbar_sortings': sorted_list,
            # 'search_in': search_in,
            # 'searchbar_inputs': search_list,
            # 'search': search,
            # 'searchbar_groupby': groupby_list,
            # 'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            # 'filterby': filterby,
        })

        return http.request.render('eenadu_reta.agent_commission', values)

    @http.route('/employee_incentive', type='http', auth="public", website=True)
    def employee_incentive(self):
        user = request.env.uid
        user_id = request.env['res.users'].browse(user)
        values = {}
        incentive_list = []
        # reta_orders = request.env['reta.orders'].search([])
        incentive = request.env['partner.incentive'].search([])
        incentive_line = request.env['partner.incentive.line'].search([])

        for incent_line in incentive_line:
            employee_name = incent_line.employee_id.name
            target_amount = incent_line.target_amt
            so_total_amount = incent_line.so_total_amt
            recieved_payment = incent_line.recieved_payment
            incentive_amt = incent_line.incentive_amt

        for incent in incentive:
            incentive_list.append({
                'unit_name': incent.unit_name.name,
                'from_date': incent.from_date,
                'to_date': incent.to_date,
                'employee_id': employee_name,
                'target_amount': target_amount,
                'so_total_amt': so_total_amount,
                'recieved_payment': recieved_payment,
                'incentive_amt': incentive_amt

            })

        values.update({
            'incentives': incentive_list,
            'page_name': 'employee_incentive'
        })


        return http.request.render('eenadu_reta.employee_incentive', values)


class RetaPortalCount(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super(RetaPortalCount, self)._prepare_home_portal_values(counters)
        user = request.env.uid
        user_id = request.env['res.users'].browse(user)
        values['agent_commission'] = request.env['commission.settlement'].search_count(
            [('agent_id', "=", user_id.partner_id.id)])
        values['employee_incentive'] = request.env['partner.incentive'].search_count([])

        return values
