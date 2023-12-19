from odoo import api, fields, models


class VehicleReport(models.AbstractModel):
    _name = 'report.eenadu_reta.report_eenadu_detail'

    @api.model
    def _get_report_values(self, docids, data):
        print('am printed')
        # docs = self.env[''].browse(docids)

        docs = self.env['sale.order'].search(
            [('specific_date', '=', data.get('specific_date')), ('classified_bool_field', '=', True)])
        classified = []
        # for rec in docs:
        #     for lines in rec.classified_order_line:
        #         if lines.main_category:
        #             classified.append(lines)
        for list in range(0, 16):
            classified.append(list)

        print('classified', classified)
        # vehicles = []
        # for vehicle in docs:
        #     vehicles.append(vehicle.vehicle.reg_no)

        return {
            # 'doc_ids': docids,
            # 'doc_model': 'transport.entry.details',
            # 'docs': docs,
            'docs': docs,
            'classified': classified,
            'columns': [0, 1],
            # 'vehicle': vehicles
        }


class WizardPickingEntry(models.TransientModel):
    _name = 'wizard.eenadu.report'

    specific_date = fields.Date('Specific Date')

    def print_report(self):
        report_name11 = 'eenadu_reta.report_eenadu_detail'
        report = self.env['ir.actions.report']._get_report_from_name(report_name11)
        print(report, 'lkkkkkkkkkkkkkkk')
        data = {
            'specific_date': self.specific_date
            # 'src_location': self.src_location.id,
            # 'des_location': self.des_location.id,
        }
        # return report.report_action(self, data=data)

        return self.env.ref('eenadu_reta.eenadu_report_action').report_action(self, data=data)
