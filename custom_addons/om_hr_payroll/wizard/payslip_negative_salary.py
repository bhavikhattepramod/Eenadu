from odoo import fields, models, api
import calendar


class PayslipNegativeSalary(models.TransientModel):
    _name = 'payslip.negative.salary'

    date_from_payslip = fields.Date(string='Date From')
    date_to_payslip = fields.Date(string='Date To',compute='_compute_date_to')

    @api.depends('date_from_payslip')
    def _compute_date_to(self):
        for record in self:
            if record.date_from_payslip:
                # Calculate the end date based on the start date
                last_day = calendar.monthrange(record.date_from_payslip.year, record.date_from_payslip.month)[1]
                record.date_to_payslip = record.date_from_payslip.replace(day=last_day)
            else:
                record.date_to_payslip = False

    def generate_payroll_negative_summary(self):
        payslip_negative = self.env['hr.payslip'].search([('date_from', '=', self.date_from_payslip),
                                                          ('date_to', '=', self.date_to_payslip)])
        results = []
        for rec in payslip_negative:
            net_line = rec.line_ids.filtered(lambda line: line.code == 'NET')
            if net_line and net_line.total < 0:
                emp_name = rec.employee_id.name
                rule_name = net_line.name
                rule_total = net_line.total
                # print(emp_name, rule_name, rule_total)
                results.append({
                    'emp_name': emp_name,
                    'rule_name': rule_name,
                    'rule_total': rule_total,
                })
        return results

    def print_list(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('om_hr_payroll.report_negative_salary_employee_payslip').report_action(self, data=data)


class PayslipNegativeSalaryFinal(models.TransientModel):
    _name = 'payslip.negative.salary.final'

    date_from_payslip_final = fields.Date(string='Date From')
    date_to_payslip_final = fields.Date(string='Date To', compute='_compute_end_date')
    company_id = fields.Many2one('res.company', string='Company')

    @api.depends('date_from_payslip_final')
    def _compute_end_date(self):
        for record in self:
            if record.date_from_payslip_final:
                # Calculate the end date based on the start date
                last_day = calendar.monthrange(record.date_from_payslip_final.year, record.date_from_payslip_final.month)[1]
                record.date_to_payslip_final = record.date_from_payslip_final.replace(day=last_day)
            else:
                record.date_to_payslip_final = False

    def generate_cal_final(self):
        payslip_ded = self.env['hr.payslip'].search([('date_from', '=', self.date_from_payslip_final),
                                                     ('date_to', '=', self.date_to_payslip_final)])
        employee_deductions = []
        for rec in payslip_ded:
            deduction_data = {
                'employee_id': rec.employee_id.name,
                'deductions': []
            }
            total_net = 0
            deductions = []
            for col in rec.line_ids:
                if col.category_id.name == 'Deduction':
                    deduction = {
                        'name': col.name,
                        'code': col.code,
                        'payslip_ded_priority': col.payslip_ded_priority,
                        'total': col.total,
                    }
                    deductions.append(deduction)
                elif col.code == 'NET':
                    total_net = col.total

            if total_net < 0:
                deductions = sorted(deductions, key=lambda x: x['payslip_ded_priority'], reverse=True)
                for deduction in deductions:
                    total_net += deduction['total']
                    deduction_data['deductions'].append(deduction)
                    if total_net >= 0:
                        deduction_data['total_net'] = total_net
                        break

                employee_deductions.append(deduction_data)
                print(employee_deductions, 'employee_deductions')
        return employee_deductions

    def print_final_list(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('om_hr_payroll.report_positive_salary_employee_payslip').report_action(self, data=data)


