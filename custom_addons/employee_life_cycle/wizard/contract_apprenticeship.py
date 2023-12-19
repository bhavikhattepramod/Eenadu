from odoo import models, fields, api
from datetime import *

class ContractApprenticeship(models.TransientModel):
    _name = "contract.apprenticeship"

    name_id = fields.Many2one('hr.employee', string='Name')
    date = fields.Date(string='Date', default=fields.Date.today())
    authorsied_id = fields.Many2one('res.company', string='Authorsied By')

    def action_print(self):
        data = {
            # 'nomination': self.read()[0],
        }
        return self.env.ref('employee_life_cycle.contract_report_action').report_action(self, data=data)
