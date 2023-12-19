from odoo import fields, api, models
from odoo.exceptions import UserError
from datetime import datetime,date



class VehicleReport(models.AbstractModel):
    _name = 'report.transport_portal.report_transport_portal'

    @api.model
    def _get_report_values(self, docids, data):
        # docs = self.env[''].browse(docids)
        print(data, 'jas')
        print(docids, 'jas')
        print(data.get('src_location'), 'jas')
        if data.get('hand_off_date_times'):
            data_date = datetime.strptime(data['hand_off_date_times'], '%Y-%m-%d').date()
        docs = self.env['transport.entry.details'].search(
            [('src_location', '=', data.get('src_location')), ('des_location', '=', data.get('des_location'))])
        vehicles = []
        for doc in docs:
            print(doc.hand_off_date_time, 'abcd')
            print(data.get('hand_off_date_times'), 'hemanth')
            if doc.hand_off_date_time:
                print(doc.hand_off_date_time.date(), 'abcd')

                if doc.hand_off_date_time.date() == data_date:
                    print(doc.hand_off_date_time.date(), data.get('hand_off_date_times'), 'comapree time')

                    for vehicle in docs:
                        vehicles.append(vehicle.vehicle.reg_no)
                else:
                    print("its not")
        if vehicles:
            return {
                'doc_ids': docids,
                'doc_model': 'transport.entry.details',
                # 'docs': docs,
                'docs': docs,
                'vehicle': vehicles
            }
        else:
            raise UserError("Date not matched")


class WizardPickingEntry(models.TransientModel):
    _name = 'wizard.picking.entry'

    src_location = fields.Many2one('transporter.routes', string='Source Location')
    des_location = fields.Many2one('transporter.routes', string='Destination Location')
    hand_off_date_times = fields.Date(string="DateTime")


    def print_report(self):
        report_name11 = 'transport_portal.report_transport_portal'
        report = self.env['ir.actions.report']._get_report_from_name(report_name11)
        data = {
            'src_location': self.src_location.id,
            'des_location': self.des_location.id,
            'hand_off_date_times': self.hand_off_date_times,
        }
        # return report.report_action(self, data=data)

        return self.env.ref('transport_portal.report_wizard_picking_entry_action_id').report_action(self, data=data)
    # def print_report(self):
    #     domain = [
    #         # (‘name’, ‘=’, self.name),
    #         ('src_location', '>=', self.src_location.id),
    #         ('des_location', '<=', self.des_location.id),
    #     ]
    #     name = self.env['transport.entry.details'].search(domain)
    #     return self.env.ref('transport_portal.report_wizard_picking_entry_action_id').report_action(name)
    
    
class VehicleReports(models.AbstractModel):
    _name = 'report.transport_portal.report_transport_portals'

    @api.model
    def _get_report_values(self, docids, data):
        # docs = self.env[''].browse(docids)
        # print(data, 'jas')
        # print(docids, 'jas')
        # print(data.get('src_location'), 'jas')
        # print(data.get('route_type'),'sdfghujikl')
        if data.get('hand_off_date_times'):
            data_date = datetime.strptime(data['hand_off_date_times'], '%Y-%m-%d').date()

        # hand_off_date = datetime.strptime(data.get('hand_off_date_time'), '%Y-%m-%d %H:%M:%S').date()
        docs = self.env['transport.entry.details'].search(
            [('src_location', '=', data.get('src_location')), ('des_location', '=', data.get('des_location')), ('route_type', '=', data.get('route_type')),
             ])
        vehicles = []
        for doc in docs:
            print(doc.hand_off_date_time,'abcd')
            print(data.get('hand_off_date_times'),'hemanth')
            if doc.hand_off_date_time:
                print(doc.hand_off_date_time.date(), 'abcd')

                if doc.hand_off_date_time.date() == data_date:
                    print(doc.hand_off_date_time.date(),data.get('hand_off_date_times'),'comapree time')

                    for vehicle in docs:
                        vehicles.append(vehicle.vehicle.reg_no)
                else:
                    print("its not")
            else:
                continue
        if vehicles:
            return {
                'doc_ids': docids,
                'doc_model': 'transport.entry.details',
                # 'docs': docs,
                'docs': docs,
                'vehicle': vehicles
            }
        else:
            raise UserError("Date not matched")



class WizardPickingEntryDup(models.TransientModel):
    _name = 'wizard.picking.entry.dup'

    src_location = fields.Many2one('transporter.routes', string='Source Location')
    des_location = fields.Many2one('transporter.routes', string='Destination Location')
    route_type = fields.Selection([('main', 'Main'), ('link', 'Link'), ('sub', 'Sub')], string='Route Type')
    hand_off_date_times = fields.Date(string="DateTime")


    def print_reports(self):
        report_name11 = 'transport_portal.report_transport_portal'
        report = self.env['ir.actions.report']._get_report_from_name(report_name11)
        data = {
            'src_location': self.src_location.id,
            'des_location': self.des_location.id,
            'route_type':self.route_type,
            'hand_off_date_times':self.hand_off_date_times,
        }
        # return report.report_action(self, data=data)

        return self.env.ref('transport_portal.report_wizard_picking_entry_action_ids').report_action(self, data=data)

        # No matching records found, you can handle this case as needed
        # For example, raise an error or show a message to the user
        # Or return False to indicate that no report should be generated



