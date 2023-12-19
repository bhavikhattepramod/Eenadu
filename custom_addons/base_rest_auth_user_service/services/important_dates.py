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
    _name = "partner.new_api.service.important_dates"
    _usage = "important_dates"
    _collection = "base_rest_auth_user_service.services"
    _description = """ """

    @restapi.method([(["/important_dates"], "GET")], auth="public")
    def get_important_dates(self):
        imp_dates = []
        data = self.env['important.dates'].sudo().search([])

        for rec in data:
            imp_dates.append({
                'date': rec.date,
                'name': rec.name,
                'type': rec.type
            })

        return imp_dates
