from odoo import api, fields, models


class NapResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals_list):
        if vals_list.get('is_newsprint_agent'):
            nap_ro_seq_obj = self.env['ir.sequence'].search(
                [('code', '=', str(vals_list.get('agent_code')) + ' nap.RO')])
            nap_cio_seq_obj = self.env['ir.sequence'].search(
                [('code', '=', str(vals_list.get('agent_code')) + ' nap.CIO')])

            if not nap_cio_seq_obj:
                self.env['ir.sequence'].sudo().create({
                    'name': str(vals_list.get('agent_code')) + ' NAP',
                    'code': str(vals_list.get('agent_code')) + ' nap.CIO',
                    'prefix': '/NAP/CIO/',
                    'padding': 5
                })
            if not nap_ro_seq_obj:
                self.env['ir.sequence'].sudo().create({
                    'name': str(vals_list.get('agent_code')) + ' NAP',
                    'code': str(vals_list.get('agent_code')) + ' nap.RO',
                    'prefix': '/NAP/RO/',
                    'padding': 5
                })
        return super(NapResPartner, self).create(vals_list)
