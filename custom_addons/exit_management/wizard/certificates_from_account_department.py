from odoo import models, fields, api
from datetime import datetime

class CertificatesAccountDepartment(models.TransientModel):
    _name = 'certificates.account.department'

    name_id = fields.Many2one('hr.resignation', string='Name', required=True)
    date = fields.Date(string="Date", default=fields.Datetime.now(), date_format="%dd/%mm/%yyyy")

    def action_print(self):
        data = {
            # 'nomination': self.read()[0],
        }
        return self.env.ref('exit_management.certificates_from_account_department_action').report_action(self, data=data)

