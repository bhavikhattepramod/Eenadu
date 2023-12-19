from odoo import models, fields, api

class StoreDepartment(models.TransientModel):
    _name = "store.department"

    names_id = fields.Many2one('hr.resignation', string='Name')
    def action_print(self):
        data = {
        }
        return self.env.ref('exit_management.store_department_report_action').report_action(self, data=data)
