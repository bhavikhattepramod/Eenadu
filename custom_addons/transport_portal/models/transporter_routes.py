from odoo import models, fields, api


class TransporterRoutes(models.Model):
    _name = 'transporter.routes'

    name = fields.Char(string="Main Route")
    child_route = fields.Many2one('transporter.routes', string='Sub Route')
    parent_route = fields.Many2one('transporter.routes', string="Link Route")
    transport_vehicle_id = fields.Many2one('transport.vehicle')
