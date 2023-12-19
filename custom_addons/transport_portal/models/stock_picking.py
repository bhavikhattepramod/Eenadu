from odoo import api, fields, models, _
import datetime


class StockPickingTransport(models.Model):
    _inherit = 'stock.picking'

    transport_route = fields.One2many('transport.routes.lines', 'stock_picking')
    transport_entry_details = fields.One2many('transport.entry.details', 'stock_picking')
    res_unit = fields.Many2one('res.partner', string='Printing Unit', related='move_ids.res_unit')
    vehicle_id = fields.Many2one('transport.vehicle', string='Vehicle No.', related='transport_entry_details.vehicle', store=True)

    # def adding_parcel_qty(self):
    #     if self.origin:
    #         if self.origin.startswith('IO'):
    #             total_qty = 0
    #             bundle_size = 100
    #             for stock in self.move_line_ids_without_package:
    #                 total_qty += stock.net_qty
    #             bundles = total_qty // bundle_size
    #             remaining_bundles = total_qty % bundle_size
    #             total = []
    #             for rec in range(int(bundles)):
    #                 total.append(1 * 100)
    #             parcels = len(total) - 1
    #             last_parcels = total[len(total) - 1] + remaining_bundles
    #             if last_parcels < 150:
    #                 parcels += 1
    #             elif last_parcels >= 150:
    #                 parcels += 2
    #             self.transport_entry_details.write({
    #                 'no_of_parcels': parcels
    #             })
        # self.no_of_parcels = parcels

    def button_validate(self):
        for res in self:
            agents = self.env['res.partner'].search([('id', '=', res.partner_id.id)])
            for agent in agents:
                vehicles = self.env['transport.vehicle'].search([])
                for vehicle in vehicles:
                    for drop_point in vehicle.transport_vehicle_line_ids:
                        if agent.agent_loc.id == drop_point.drop_point_id.id:
                            if agent.id == drop_point.agent_id.id:
                                vals = {
                                    'picking': res.id,
                                    'vehicle': vehicle.id,
                                    'transporter': vehicle.unit_id.id,
                                    'location': agent.agent_loc.id,
                                    'src_location': agent.from_place_id.id,
                                    'des_location': agent.to_place_id.id,
                                }
                                if agent.agent_loc.parent_route:
                                    vals.update({
                                        'route_type': 'link'
                                    })
                                elif agent.agent_loc.child_route:
                                    vals.update({
                                        'route_type': 'sub'
                                    })
                                else:
                                    vals.update({
                                        'route_type': 'main'
                                    })
                                routes_vals = {
                                    'src_location': agent.from_place_id.id,
                                    'des_location': agent.to_place_id.id,
                                }
                                for route in vehicle.transport_routes_id.route_lines:
                                    if agent.from_place_id.id == route.src_location.id and agent.to_place_id.id == route.des_location.id:
                                        vals.update({
                                            'distance': route.distance,
                                            'hours': route.hours
                                        })
                                        routes_vals.update({
                                            'distance': route.distance,
                                            'hours': route.hours
                                        })
                                res.write({
                                    'transport_entry_details': [(0, 0, vals)]
                                })
                                res.write({
                                    'transport_route': [(0, 0, routes_vals)]
                                })
        # self.adding_parcel_qty()
            if res.origin:
                if res.origin.startswith('IO'):
                    total_qty = 0
                    bundle_size = 100
                    for stock in res.move_line_ids_without_package:
                        total_qty += stock.net_qty
                    bundles = total_qty // bundle_size
                    remaining_bundles = total_qty % bundle_size
                    total = []
                    for rec in range(int(bundles)):
                        total.append(1 * 100)
                    parcels = len(total) - 1
                    last_parcels = total[len(total) - 1] + remaining_bundles
                    if last_parcels < 150:
                        parcels += 1
                    elif last_parcels >= 150:
                        parcels += 2
                    res.transport_entry_details.write({
                        'no_of_parcels': parcels
                    })
        super(StockPickingTransport, self).button_validate()

    def hand_off_sequence(self):
        unit_list = []
        for unit in self:
            if unit.res_unit:
                unit_list.append(unit.res_unit.id)

        map_hand_off_key = {}
        for hand_off in set(unit_list):
            unit_name = self.env['res.partner'].browse(hand_off)
            map_hand_off_key[hand_off] = unit_name.unit_ref + self.env['ir.sequence'].next_by_code('hand.off.sequence')

        for records in self:
            for ids in map_hand_off_key:
                if records.res_unit.id == ids:
                    vals = {'transport_entry_details': []}
                    for transport_entry_details in records.transport_entry_details:
                        vals['transport_entry_details'].append([1, transport_entry_details.id, {
                            'hand_off_id': map_hand_off_key[ids],
                            'hand_off_date_time': datetime.datetime.now(),
                        }])
                    records.write(vals)


class TransportDetails(models.Model):
    _name = 'transport.entry.details'

    stock_picking = fields.Many2one('stock.picking')
    agent_name = fields.Many2one('res.partner', 'Agent Name', related='stock_picking.partner_id')
    agent_number = fields.Char('Agent Number', related='agent_name.phone')
    transporter = fields.Many2one('res.partner', 'Transporter')
    location = fields.Many2one('transporter.routes', string='location')
    route_type = fields.Selection([('main', 'Main'), ('link', 'Link'), ('sub', 'Sub')], string='Route Type')
    picking = fields.Many2one('stock.picking', string='Picking')
    vehicle = fields.Many2one('transport.vehicle')
    no_of_parcels = fields.Integer('No of Parcels')
    distance = fields.Float('Distance(KM)')
    hours = fields.Float('Hours')
    src_location = fields.Many2one('transporter.routes', string='Source Location')
    des_location = fields.Many2one('transporter.routes', string='Destination Location')
    hand_off_id = fields.Char(string="HAND OFF")
    hand_off_date_time = fields.Datetime(string="DateTime", readonly=1)
    state = fields.Selection([('waiting', 'Waiting'),
                              ('picked', 'Picked'),
                              ('drop', 'Drop')], default='waiting')

    # parcels_no = fields.Integer('parcels', related='stock_picking.transport_entry_details.no_of_parcels')
    def waiting_to_picked(self):
        for rec in self:
            rec.state = 'picked'

    def picked_to_drop(self):
        for rec in self:
            rec.state = 'drop'

    def call_wizard(self):
        action = self.env.ref('transport_portal.wizard_picking_entry_action').read()[0]
        return action

    def _compute_parcel_qty(self):
        total_qty = 0
        bundle_size = 100
        for stock in self.stock_picking.move_line_ids_without_package:
            total_qty += stock.net_qty
        bundles = total_qty // bundle_size
        remaining_bundles = total_qty % bundle_size
        total = []
        for rec in range(int(bundles)):
            total.append(1 * 100)
        parcels = len(total) - 1
        last_parcels = total[len(total) - 1] + remaining_bundles
        if last_parcels < 150:
            parcels += 1
        elif last_parcels >= 150:
            parcels += 2
        self.no_of_parcels = parcels

        # rem = total_qty - (bundels * bundle_size)
        # print(rem)

    # @api.depends('location')
    # def _compute_route_type(self):
    #     for rec in self:
    #         location_id = self.env['transporter.routes'].search([('id', '=', rec.location.id)])
    #         if location_id.parent_route:
    #             rec.route_type = 'link'
    #         else:
    #             rec.route_type = 'main'


class ResPartnerTransport(models.Model):
    _inherit = "res.partner"

    from_place_id = fields.Many2one('transporter.routes', string='From Place')
    to_place_id = fields.Many2one('transporter.routes', string='To Place')
    agent_loc = fields.Many2one('transporter.routes', 'Location')
