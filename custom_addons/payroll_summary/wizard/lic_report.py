import calendar

from odoo import api, fields, models,_
from datetime import date, datetime ,timedelta
from odoo.tools.misc import format_date


class PayrollLICreport(models.TransientModel):
    _name = 'payroll.lic.report.wizard'
    _description = 'Payroll Lic Report Wizard'

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To", compute='_compute_date_to')
    unit_lic = fields.Many2many('unit.master')
    service_master = fields.Many2one('service.provider')
    today_date = datetime.now().date()
    today_time = datetime.now().time()

    @api.depends('date_from')
    def _compute_date_to(self):
        for record in self:
            if record.date_from:
                # Calculate the end date based on the start date
                last_day = calendar.monthrange(record.date_from.year, record.date_from.month)[1]
                record.date_to = record.date_from.replace(day=last_day)
            else:
                record.date_to = False


    def lic_payroll_report(self):
        report_data = {
            # 'docs': self,  # Pass the current object or data
            # 'current_datetime': current_datetime,

        }
        # Generate and return the PDF report using the report_action method
        return self.env.ref('payroll_summary.action_lic_report_in_pdf').report_action(self, data=report_data)

    def policy_details(self):
        policy_data = []
        grand_total = 0
        for unit in self.unit_lic:
            records = self.env['hr.payslip'].search([
                ('date_from', '=', self.date_from),
                ('date_to', '=', self.date_to),
                ('employee_id.unit_name_hr', '=', unit.id)
            ])

            unit_policy_data = []  # Store policy data for each unit
            unit_total_amount = 0  # Initialize the total amount for the unit

            for record in records:
                policy = self.env['insurance.policy'].search([
                    ('employee_code', '=', record.employee_id.id)
                ])

                for policy_item in policy.insurance_policy_master:
                    if (
                            policy_item.service_company.id == self.service_master.id and
                            policy_item.insurance_applicable == True
                    ):
                        policy_amount = policy_item.premium_amt
                        unit_total_amount += policy_amount
                        unit_policy_data.append({
                            'serial_number': len(unit_policy_data) + 1,
                            'service_company_name': policy_item.service_company.service_provider_name,
                            'policy_no': policy_item.policy_no,
                            'employee_name': policy.employee_code.name,
                            'employee_code': policy.employee_name,
                            'policy_amount': policy_amount,
                            # Add more fields as needed
                        })

            policy_data.append({
                'unit_name': unit.name,
                'policies': unit_policy_data,
                'unit_total_amount': unit_total_amount,
            })

            grand_total = sum(unit['unit_total_amount'] for unit in policy_data)

        return {'policy_data': policy_data, 'grand_total': grand_total}

    @api.onchange('date_from')
    def onchange_unit(self):
        unit = self.env['unit.master'].search([])
        self.unit_lic = unit
        # print(self.unit_lic,'unit')



class PolicyInfo(models.Model):
    _name = 'policy.model.info'
    _description = 'Policy Model'

    sl_no = fields.Integer('Sl. No.')
    policy_no = fields.Char('Policy No.')
    name = fields.Char('Name')
    emp_cd = fields.Char('EMP CD')
    amount = fields.Float('Amount')


