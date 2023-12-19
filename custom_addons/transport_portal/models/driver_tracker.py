from odoo import models, fields, api
from geopy.geocoders import Nominatim


class DriverTracker(models.Model):
    _name = 'driver.tracker'
    _rec_name = 'vehicle'

    vehicle = fields.Many2one('transport.vehicle', string="Vehicle")
    vehicle_route_source = fields.Many2one('transporter.routes', string="Source Location")
    vehicle_route_destination = fields.Many2one('transporter.routes', string="Destination Location")
    hand_off_id = fields.Many2one('transport.entry.details', string="Hand Off ID")
    hand_of_date = fields.Date(string="DateTime")
    driver_tracker_line = fields.One2many('driver.tracker.line', 'driver_tracker_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'), ('drop', 'Drop'),
    ], default='draft', help="The states is help to know to driver tracker")

    @api.constrains('vehicle', 'hand_of_date')
    def add_drop_location(self):
        for drop_locations in self.driver_tracker_line:
            drop_locations.unlink()
        transport_entry_details_id = self.env['transport.entry.details'].search([])
        for routes in transport_entry_details_id:
            if routes.vehicle.id == self.vehicle.id and routes.hand_off_date_time and routes.hand_off_date_time.date() == self.hand_of_date:
                vals = {
                    'vehicle_drop_location': routes.location.id,
                    'distance_of_location': routes.distance,
                    'hours_id': routes.hours,
                    'no_of_parcels_to_drop': routes.no_of_parcels
                }
                self.write({
                    'driver_tracker_line': [(0, 0, vals)]
                })


class DriverTrackerLine(models.Model):
    _name = 'driver.tracker.line'

    vehicle_drop_location = fields.Many2one('transporter.routes', string="Drop Location")
    distance_of_location = fields.Float(string="Distance(KM)")
    hours_id = fields.Float(string="Hours")
    no_of_parcels_to_drop = fields.Integer(string="No Of Parcels")
    driver_tracker_id = fields.Many2one('driver.tracker', string="Driver Tracker")
    state = fields.Selection([('waiting', 'Waiting'), ('drop', 'Drop')], default='waiting')
    lat_long = fields.Char(string="Address")

    def action_to_drop(self):
        location = Nominatim(user_agent="GetLoc")

    # print(getLocation())
        # for rec in self:
        #     rec.state = 'drop'

    def write(self, values):
        result = super(DriverTrackerLine, self).write(values)
        # Get the unique set of states from all sale order lines
        line_states = self.mapped('state')
        # If all sale order lines have the same state, update the main sale order's state
        if len(line_states) == 1:
            new_state = line_states[0]
            self.driver_tracker_id.write({'state': new_state})
        return result












