from odoo import fields,models

class StateInsuranceCorporation(models.TransientModel):
    _name = 'employee.state.insurance.corporation'

    name = fields.Many2one('hr.employee',string='Employee Code')
    def action_print_report_button(self):
        data = {
            # 'form_values': self.read()[0],
        }
        return self.env.ref('employee_life_cycle.hr_employee_state_insurance_corporation_report').report_action(self,data=data)
