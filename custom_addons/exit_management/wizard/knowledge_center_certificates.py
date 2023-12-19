from odoo import models, fields, api
from datetime import datetime


class SuperannuationIntimationLetter(models.TransientModel):
    _name = "knowledge.center.certificate"

    name_id=fields.Many2one('hr.resignation', string="Name")
    current_date=fields.Date(string="Current date", default=fields.Date.today())


    def knowledge_center_certificates_print(self):
        data = {

        }
        return self.env.ref('exit_management.report_knowledge_center_certificates_wizards').report_action(self, data=data)
