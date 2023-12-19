from odoo import api, fields, models


# created class for the purpose nomination form report

class NominationFormWizard(models.TransientModel):
    _name = 'nomination.formwizard'

    name = fields.Many2one('hr.employee', string="Name")

    def nomination_form_print(self):
        data = {
            # 'model': 'nomination.formwizard',
            # 'form': self.read()[0]

        }
        return self.env.ref('hrms_nomination_form_report.nomination_form_report_wizard').report_action(self, data=data)
