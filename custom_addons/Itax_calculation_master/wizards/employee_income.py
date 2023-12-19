from odoo import fields, models, api
from datetime import datetime, date
from dateutil import relativedelta
from dateutil.relativedelta import relativedelta
from odoo.tools.misc import format_date


class EmployeeIncome(models.TransientModel):
    _name = 'employee.income'

    # employee_name = fields.Many2one('hr.employee', string="Employee Name")
    # employee_code = fields.Char(related="employee_name.identification_id", string="Employee Code")
    tds_computation_month_batch = fields.Selection(selection='list_all_months_batch', string='TDS Month',
                                                   default=datetime.today().strftime("%b-%Y"), required=1)

    def list_all_months_batch(self):
        data_list = []
        # Getting the financial start and end dates from the res.company model
        company_batch = self.env['res.company'].browse(self.env.company.id)
        financial_start_date_batch = company_batch.fiscal_year_start_date
        financial_end_date_batch = company_batch.fiscal_year_last_date
        current_date = financial_start_date_batch

        while current_date <= financial_end_date_batch:
            month_year = current_date.strftime("%b-%Y")
            month_name = current_date.strftime("%b")
            data_list.append((month_year, month_name))
            current_date += relativedelta(months=1)
        return data_list


    def generate_income_tax(self):
        emp_pay = self.env['hr.payslip'].search([])
        print(emp_pay, 'testinggggggggggggg')
        for emp in emp_pay:
            for emp_res in emp.employee_id:
                it_returns = self.env['it.returns'].search([('employee_id', '=', emp_res.id)])
                if it_returns:
                    it_returns.update({
                        'tds_computation_month': self.tds_computation_month_batch,
                    })
                    it_returns.compute_tax_sheet()
                else:
                    gross = self.env['taxable.income'].search([('is_gross_total_income', '=', True)])
                    vals_list = {
                        'gross_annual_income': gross.id
                    }
                    vals = {'employee_id': emp_res.id,
                            'employee_code': emp_res.identification_id,
                            'pan_no': emp_res.employee_pan_no,
                            'birthday': emp_res.birthday,
                            'tds_computation_month': self.tds_computation_month_batch,
                            'tax_resign_type': emp_res.tax_regim_type.id,
                            # 'payslip_run_id': batch.id,
                            'gross_line_ids': [(0, 0, vals_list)]
                            }

                    self.env['it.returns'].create(vals).compute_tax_sheet()
