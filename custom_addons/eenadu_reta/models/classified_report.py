from odoo import api, models


class ClassifiedReportAds(models.Model):
    _name = 'classified.report.ads'

    def compute_report_values(self):
        report_list = []
        line_no = ''
        for rec in range(0, 75):
            number = 0
            number = rec + 1
            line_no = str('Line - ') + str(number)
            report_list.append(line_no)
        print(report_list)

        return report_list