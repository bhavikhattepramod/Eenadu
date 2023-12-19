from odoo import api, fields, models


class TransportRoutes(models.Model):
    _name = 'transport.routes'
    _rec_name = 'route'

    name = fields.Many2one('res.partner', domain=[('is_printing_unit', '=', True)])
    route = fields.Char('Name')
    route_lines = fields.One2many('transport.routes.lines', 'route_id')


class RoutesLines(models.Model):
    _name = 'transport.routes.lines'

    distance = fields.Integer('Distance(KM)')
    hours = fields.Float('Hours')
    src_location = fields.Many2one('transporter.routes', string='Source Location')
    des_location = fields.Many2one('transporter.routes', string='Destination Location')
    route_id = fields.Many2one('transport.routes')
    stock_picking = fields.Many2one('stock.picking')
