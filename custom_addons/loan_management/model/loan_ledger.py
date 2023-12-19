from datetime import date
from odoo import fields, models, api
from odoo.exceptions import ValidationError


class EmployeeLoanLedger(models.Model):
    _name = 'employee.loan.ledger'
    _rec_name = 'employee_code_loan'

    employee_code_loan = fields.Many2one('hr.employee', string='Employee Name')
    employee_name_loan = fields.Many2one('employee.loan', string='Loan Name')
    employee_ledger_track_ids = fields.One2many('employee.loan.ledger.line', 'loan_tracking_id')

    @api.onchange('employee_code_loan')
    def _onchange_employee_code_loan(self):
        employee_loan_ids = [record.id for record in
                             self.env['employee.loan'].search([('employee_code', '=', self.employee_code_loan.id)])]
        print(employee_loan_ids, 'emp name')
        return {'domain': {'employee_name_loan': [('id', 'in', employee_loan_ids)]}}


class EmployeeLoanLedgerLine(models.Model):
    _name = 'employee.loan.ledger.line'

    process_month = fields.Date(string='Processing Month')
    opening_balance = fields.Float('Opening Balance')
    recovery_amount = fields.Float('Recovery Amount')
    closing_balance = fields.Float('Closing Balance')
    loan_tracking_id = fields.Many2one('employee.loan.ledger')


class HrPayslipChanges(models.Model):
    _inherit = 'hr.payslip'

    # Getting the values from computed payslip and post into the loan ledger
    def get_loan_amount(self):
        amounts = self.env['employee.loan.ledger'].search([('employee_code_loan', '=', self.employee_id.id)])
        for rec in self:
            for vals in rec.line_ids:
                for ttal in amounts:
                    if ttal.employee_name_loan.loan_name_id.name == vals.name:
                        print('pppppppppppppppppppppppppppppppppppppppppppppppppppp')
                        existing_track = ttal.employee_ledger_track_ids.filtered(lambda x: x.process_month == rec.date_to)
                        if existing_track:
                            existing_track.write({'recovery_amount': vals.total})
                            print('lllllllllllllllllllllllllllllllllllllllllllllllllll')
                        else:
                            loan = self.env['employee.loan'].search([('loan_name_id', '=', vals.name)], limit=1)
                            if loan:
                                loan_amount = loan.loan_amount
                                if loan_amount > 0.00:
                                    if len(ttal.employee_ledger_track_ids.ids) == 0:
                                        balance = loan_amount - vals.total
                                        updating_vals = {
                                            'recovery_amount': vals.total,
                                            'opening_balance': loan_amount,
                                            'closing_balance': balance,
                                            'process_month': rec.date_to,
                                        }
                                        # if ttal_index == 0:
                                        #     updating_vals['month'] = rec.date_to
                                        updating = ttal.employee_ledger_track_ids.create(updating_vals)
                                        if vals.total > 0.00:
                                            ttal.employee_ledger_track_ids += updating
                                    else:
                                        print(ttal.employee_ledger_track_ids.ids, ttal.employee_ledger_track_ids[-1])
                                        first_rec = ttal.employee_ledger_track_ids[-1]
                                        print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
                                        updating_vals = {
                                            'recovery_amount': vals.total,
                                            'opening_balance': first_rec.closing_balance,
                                            'closing_balance': first_rec.closing_balance - vals.total,
                                            'process_month': rec.date_to,
                                        }
                                        # if ttal_index == 0:
                                        #     updating_vals['month'] = rec.date_to
                                        updating = ttal.employee_ledger_track_ids.create(updating_vals)
                                        if first_rec.closing_balance > 0.00:
                                            print('ffffffffffffffffffffffffffffffffffffffffffffffff')
                                            ttal.employee_ledger_track_ids += updating
                                        else:
                                            loan.loan_closed_date = date.today()
                                            loan.loan_closed = True
                                            print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
                                            loan.active = False
                                else:
                                    raise ValidationError("The loan amount is not valid for the selected loan.")
                            else:
                                raise ValidationError("No loan record found for the selected loan.")



                # print(vals.name, 'vals')
                # amounts = self.env['employee.loan.ledger'].search([('employee_code_loan', '=', rec.employee_id.id), (
                #     'employee_name_loan.loan_name_id.name', '=', vals.name)])
            # for ttal in amounts:
            #     # if ttal.employee_name_loan.loan_name_id.name == vals.name:
            #     #     print('am in')
            #     # if vals.total > 0.00:
            #     updating = ttal.employee_ledger_track_ids.create({
            #         'month': rec.date_to,
            #         'recovery_amount': vals.total,
            #     })
            #     print(updating, 'updated')
            #     ttal.employee_ledger_track_ids += updating

                # print(ttal.employee_name_loan.loan_name_id.name,'hhh',vals.name)
                # if ttal.employee_name_loan.loan_name_id.name == vals.name and ttal.employee_code_loan == rec.employee_id:
                #     print(ttal.employee_name_loan.loan_name_id.name,'Loan Name')
                #     print(vals.total, 'total')
                #     print(rec.date_to, 'date to')
                #     updating = ttal.employee_ledger_track_ids.create({
                #         'month': rec.date_to,
                #         'recovery_amount': vals.total,
                #     })
                #     print(updating,'updated')
                #     ttal.employee_ledger_track_ids += updating

# lis = [var.name for var in rec.line_ids]
# print(lis)
