from odoo import fields, api, models
from odoo.exceptions import UserError
import json
import requests
import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gst_verified = fields.Boolean(string="GST Verified", default=False, readonly=True)
    gst_status = fields.Char(string="GST Status", readonly=True)
    current_date = fields.Char(reaonly=True, string="", readonly=True)

    def fetch_address(self):
        subscription_key = self.env.user.company_id.subscription_key
        gstin_number = self.env.user.company_id.gstin_number
        source_type = self.env.user.company_id.source_type
        reference_no = self.env.user.company_id.reference_no
        location = self.env.user.company_id.location


        for rec in self:
            if rec.vat:
                url = "https://api.wepgst.com/asp/rg/Einvoice/v1.03/GetGstin?GSTIN=" + str(rec.vat)

                headers = {
                    "Ocp-Apim-Subscription-Key": subscription_key,
                    "Gstin": gstin_number,
                    "sourcetype": source_type,
                    "referenceno": reference_no,
                    "Location": location
                }
                response = requests.get(url, headers=headers)
                result = response.json()
                current_date_time = datetime.datetime.now()
                formatted_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
                res = result.get('OutputResponse')
                street = str(res.get('AddrBnm')) + str(res.get('AddrBno')) + str(res.get('AddrFlno'))
                status = res.get('Status')
                state = self.env['res.country.state'].search([('l10n_in_tin', '=', res.get('StateCode'))])

                if status == "ACT":
                    rec.write({
                        'name': res.get('TradeName') if res.get('TradeName') else res.get('LegalName'),
                        'company_name': res.get('LegalName') if res.get('LegalName') else '',
                        'street': street if street else '',
                        'street2': res.get('AddrSt') if res.get('AddrSt') else '',
                        'city': res.get('AddrLoc') if res.get('AddrLoc') else '',
                        'state_id': state.id,
                        'zip': res.get('AddrPncd') if res.get('AddrPncd') else 0,
                        'country_id': self.env.ref('base.in').id,
                        'gst_verified': True,
                        'gst_status': res.get('Status') if res.get('Status') else '',
                        'current_date': formatted_date_time
                    })
                else:
                    rec.write({
                        'name': res.get('TradeName') if res.get('TradeName') else res.get('LegalName'),
                        'company_name': res.get('LegalName') if res.get('LegalName') else '',
                        'street': street if street else '',
                        'street2': res.get('AddrSt') if res.get('AddrSt') else '',
                        'city': res.get('AddrLoc') if res.get('AddrLoc') else '',
                        'state_id': state.id,
                        'zip': res.get('AddrPncd') if res.get('AddrPncd') else 0,
                        'country_id': self.env.ref('base.in').id,
                        'gst_status': res.get('Status') if res.get('Status') else '',
                        'current_date': formatted_date_time
                    })


    @api.onchange('vat')
    def onchange_gst_verified(self):
        for rec in self:
            if rec.vat:
                rec.gst_verified = False


class ResCompany(models.Model):
    _inherit = 'res.company'


    gstin_number = fields.Char(string="GSTIN")
    subscription_key = fields.Char(string="Subscription Key")
    source_type = fields.Char(string="Source Type")
    reference_no = fields.Char(string="Reference Number")
    location = fields.Char(string="Location")
