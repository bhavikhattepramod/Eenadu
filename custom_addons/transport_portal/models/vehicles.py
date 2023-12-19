from odoo import models, fields, api


class Vehicles(models.Model):
    _inherit = 'res.partner'

    is_vehicles = fields.Boolean(string='Is Vehicles?')
    transporter_id = fields.Many2one('res.partner', string="Transport Unit", domain=[('is_printing_unit', '=', True)])


class VehiclesNew(models.Model):
    _name = 'transport.vehicle'
    _rec_name = 'reg_no'

    partner_id = fields.Many2one('res.partner', string="Vehicle Partner",
                                 domain=[('is_transport_vendor', '=', True),
                                         ('is_active_vendor', '=', True)])
    unit_id = fields.Many2one('res.partner', string="Transport Unit", domain=[('is_printing_unit', '=', True)])
    reg_no = fields.Char(string="Vehicle Reg No.")
    transport_routes_id = fields.Many2one('transport.routes', string="Route")
    vehicle_type = fields.Many2one('vehicle.type', string="Vehicle Type")
    transport_vehicle_line_ids = fields.One2many('transport.vehicle.line', 'transport_vehicle_line_id',
                                                 string='Transport vehicle line ref')

    @api.constrains('transport_routes_id')
    def add_drop_location(self):
        for transport in self.transport_vehicle_line_ids:
            transport.unlink()
        for routes in self.transport_routes_id.route_lines:
            agent_route = self.env['res.partner'].search([])
            for rec in agent_route:
                if rec.from_place_id.id == routes.src_location.id and rec.to_place_id.id == routes.des_location.id:
                    vals = {
                        'drop_point_id': rec.agent_loc.id,
                        'agent_id': rec.id
                    }
                    self.write({
                        'transport_vehicle_line_ids': [(0, 0, vals)]
                    })


class TransportVehicleLine(models.Model):
    _name = 'transport.vehicle.line'

    drop_point_id = fields.Many2one('transporter.routes', string='Drop Point')
    agent_id = fields.Many2one('res.partner', 'Agent')
    agent_code = fields.Char('Agent Code', related='agent_id.agent_code')
    transport_vehicle_line_id = fields.Many2one('transport.vehicle', string='Transport Vehicle Ref')


class VehiclesType(models.Model):
    _name = 'vehicle.type'

    name = fields.Char(string="Name")
