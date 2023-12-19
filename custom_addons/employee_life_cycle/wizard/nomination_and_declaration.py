from odoo import models, fields, api

class NominationAndDeclaration(models.Model):
    _name = "nomination.declaration"


    name = fields.Many2one('hr.employee',string='Employee Name')

    def action_print_report(self):
        data = {
            'nomination' : self.read()[0],
        }
        return self.env.ref('employee_life_cycle.nomination_and_declaration_report_action').report_action(self,data=data)