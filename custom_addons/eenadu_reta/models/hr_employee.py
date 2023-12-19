from odoo import fields, api, models


class HrEmployeeInheritSmartButton(models.Model):
    _inherit = 'hr.employee'

    agent_count = fields.Integer('Reta Agent Count', compute='_compute_agent_count')

    def _compute_agent_count(self):
        for rec in self:
            count = self.env['res.partner'].search_count([('hr_employee_id', '=', rec.id)])
            if count:
                rec.agent_count = count
            else:
                rec.agent_count = 0

    def display_reta_agents(self):
        domain = [('hr_employee_id', '=', self.id)]
        action = {
            'name': 'Reta Agents',
            'view_mode': 'tree,form',
            'res_model': 'res.partner',
            'type': 'ir.actions.act_window',
            'domain': domain,
            'target': 'current',
        }
        return action



class AccountAnalyticAccountCheckBox(models.Model):
    _inherit = 'account.analytic.account'

    is_advertisement = fields.Boolean('Is Advertisement')