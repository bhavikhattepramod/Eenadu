from datetime import timedelta

from odoo import models, fields, _, api
import math


class SalaryRuleInherit(models.Model):
    _inherit = 'hr.salary.rule'

    pf_applicable = fields.Boolean(string="PF Applicable")
    esi_applicable = fields.Boolean(string="ESI Applicable")
    esi_compute = fields.Boolean(string="ESI Compute")
    pf_compute = fields.Boolean(string="PF Compute")
    eps_compute = fields.Boolean(string="EPS Compute")
    is_professional = fields.Boolean(string='PT Applicable')
    prorate = fields.Boolean(string="Prorate Applicable")
    lop_field = fields.Boolean(string="LoP Applicable", default=True)
    lop_arrears = fields.Boolean(string='LoP Arrears Applicable')
    ot_hours_applicable = fields.Boolean(string='OT Applicable')
    company_notice_period = fields.Boolean(string='Company Notice Period Applicable')
    employee_notice_period = fields.Boolean(string='Employee Notice Period Applicable')
    gratuity_rule_check = fields.Boolean(string='Gratuity Applicable')
    leave_encashment_rule_check = fields.Boolean(string='Leave Encashment Applicable')

    @api.onchange('prorate')
    def _onchange_prorate_field(self):
        record = self.env['hr.contract'].search([])
        prorate = self.env['hr.contract.line'].search([])
        struct_prorate = self.env['hr.payroll.structure'].search([])
        for val in self:
            for st_pro in struct_prorate:
                for rec in record:
                    for line in prorate:
                        if rec.struct_id.id == st_pro.id:
                            if val.name == line.salary_line_component.name:
                                line.prorate_field = val.prorate
                                # print('mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')

    @api.onchange('lop_field')
    def _onchange_lop_field(self):
        lop = self.env['hr.contract'].search([])
        lop_days = self.env['hr.contract.line'].search([])
        struct_lop_field = self.env['hr.payroll.structure'].search([])
        for value in self:
            for st_lop in struct_lop_field:
                for rec in lop:
                    for line in lop_days:
                        if rec.struct_id.id == st_lop.id:
                            if value.name == line.salary_line_component.name:
                                line.lop_applicable = value.lop_field

    @api.onchange('lop_arrears')
    def _onchange_lop_arrears(self):
        lop_arr = self.env['hr.contract'].search([])
        var = self.env['hr.payslip.line'].search([])
        struct_lop_arrear = self.env['hr.payroll.structure'].search([])
        for rec in self:
            for st_lop_arr in struct_lop_arrear:
                for record in lop_arr:
                    for val in var:
                        if record.struct_id.id == st_lop_arr.id:
                            if rec.name == val.name:
                                val.lop_applicable_field = rec.lop_arrears
                            # print('gggg')

    @api.constrains('pf_applicable')
    def onchange_pf_app(self):
        search_rules_pf = self.env['hr.salary.rule'].search([('code', 'in', ['EPFEMP', 'EPFEMPLR'])])
        for rec in search_rules_pf:
            if rec.pf_applicable:
                rec.pf_compute = True

    @api.constrains('esi_applicable')
    def onchange_esi_comp(self):
        search_rules_esi = self.env['hr.salary.rule'].search([('code', 'in', ['ESIEMP', 'ESIEMPLR'])])
        for rec in search_rules_esi:
            if rec.esi_applicable:
                rec.esi_compute = True


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip.line'

    structure_id = fields.Many2one('hr.payroll.structure', string='Structure')
    esi_com = fields.Boolean(string='ESI compute')
    esi_applicable = fields.Boolean(string="ESI Applicable")
    pf_applicable_payslip = fields.Boolean(string="PF Applicable")
    pf_com = fields.Boolean(string="PF Compute")
    eps_com = fields.Boolean(string="EPS Compute")
    lop_applicable_field = fields.Boolean(string="Applicable for LoP Arrear")
    ot_applicable = fields.Boolean(string='OT Applicable')
    salary_master = fields.Float(string="Salary Master", store=True, readonly=True)

    contract_id = fields.Many2one("hr.contract", string="Contract")


class InheritStructid(models.Model):
    _inherit = "hr.payslip"

    amount_da = fields.Float()

    def esi_calculation(self):
        esi = self.env['pf.esi.settings'].search([], limit=1)
        # esi_inherit = self.env['hr.payslip.line'].search([])
        emp_contribution = self.env['hr.salary.rule'].search([('name', '=', 'ESI Employee Contribution')])
        empr_contribution = self.env['hr.salary.rule'].search([('name', '=', 'ESI Employer Contribution')])
        exe_payroll = self.env['hr.payroll.structure'].search([('name', '=', 'Journalists')])
        pf_check_box = self.env['hr.employee'].search([])
        exe_payroll_struct = self.env['hr.payroll.structure'].search([])
        # print(emp_contribution, exe_payroll)

        record = self
        esi_not_value = 0.0
        for rec in record:
            for esi_struct in exe_payroll_struct:
                for rule in rec.struct_id.rule_ids:
                    for line in rec.line_ids:
                        line.structure_id = rec.struct_id
                        # print(line.structure_id.name, "ggggggggggggggggg")
                        if rule.name == line.name:
                            if rule.esi_applicable == True:
                                line.esi_applicable = True
                                # print(line.esi_applicable, 'rrrrrrrr')
                            if rule.esi_compute == True:
                                line.esi_com = True

                        # if rule.name == line.name:
                        #     if rule.esi_applicable:
                        #         line.write({'esi_applicable': True})
                        #         print(line.esi_applicable, 'rrrrrrrr')
                        #     if rule.esi_compute:
                        #         line.write({'esi_com': True})

                    line_list = []
                    total = 0.0
                    for line_val in rec.line_ids:
                        if line_val.esi_applicable and not (line_val.esi_com and line_val.esi_applicable):
                            line_list.append(line_val.total)
                            print(line_val,'linelist')

                    if len(line_list) != 0:
                        # esi_total = 0
                        for i in line_list:
                            print("DDDDDDDDDDDdesi", i)
                            total = total + i
                            print(total, 'hhhhhhhhhhhesi')
                            a = total * esi.esi_employee_contribution / 100
                            esi_emp_total = round(a)
                            b = total * esi.esi_employer_contribution / 100
                            esi_empr_total = round(b)
                        # print(total, "111111111111111111111111111")
                        # print(esi_emp_total, a, "88888888888888888888888888")
                        # print(esi_empr_total, b, "ooooooooooooooooooo")

                        for vals in pf_check_box:
                            if rule.esi_compute == True and line.esi_com == True:
                                # line.esi_com = rule.esi_compute
                                print('in first if')
                                # print(rec.struct_id.name)
                            if rec.employee_id.name == vals.name:
                                if vals.esi_applicable_check_box == True:
                                    if rec.struct_id.id == esi_struct.id:
                                        if emp_contribution and exe_payroll and empr_contribution and emp_contribution.amount_select == 'code':
                                            emp_contribution.amount_python_compute = 'result = ' + str(esi_emp_total)
                                            empr_contribution.amount_python_compute = 'result = ' + str(esi_empr_total)
                                            # print(emp_contribution.amount_python_compute, "llllllllllljjjjkkkk")
                                            # print(empr_contribution.amount_python_compute, "ddddddddddllllllllllljjjjkkkk")

                                else:
                                    emp_contribution.amount_python_compute = 'result = ' + str(esi_not_value)
                                    empr_contribution.amount_python_compute = 'result = ' + str(esi_not_value)
                                    # print(emp_contribution.amount_python_compute, "llllpooooooppppppppppppppp")
                                    # print(empr_contribution.amount_python_compute, "daaaaaaaaaaaaaaaaaaaadkkkk")

        return emp_contribution.amount_python_compute, empr_contribution.amount_python_compute

    # def compute_sheet(self):
    #     for rec in self:
    #         super(InheritStructid, rec).compute_sheet()
    #         rec.pf_calculation()
    #         rec.esi_calculation()
    #         super(InheritStructid, rec).compute_sheet()
    #     return

    def pf_calculation(self):
        pf = self.env['pf.esi.settings'].search([], limit=1)
        # esi_inherit = self.env['hr.payslip.line'].search([])
        pf_emp_contribution = self.env['hr.salary.rule'].search([('name', '=', 'EPF Employee Contribution')])
        pf_empr_contribution = self.env['hr.salary.rule'].search([('name', '=', 'EPF Employer Contribution')])
        eps_empr_contribution = self.env['hr.salary.rule'].search([('name', '=', 'EPS Employer Contribution')])
        line_payroll = self.env['hr.payroll.structure'].search([('name', '=', 'Journalists')])
        line_payroll_struct = self.env['hr.payroll.structure'].search([])
        check_box_pf = self.env['hr.employee'].search([])
        # print(pf_emp_contribution, line_payroll)

        record = self
        pf_not_value = 0.0
        for rec in record:
           for pf_struct in line_payroll_struct:
                for rule in rec.struct_id.rule_ids:
                    for line in rec.line_ids:
                        line.structure_id = rec.struct_id
                        if rule.name == line.name:
                            if rule.pf_applicable == True:
                                line.pf_applicable = True
                            if rule.pf_compute == True:
                                line.pf_com = True

                    line_list = []
                    total = 0.0
                    for line_val in rec.line_ids:
                        if line_val.pf_applicable and not (line_val.pf_com and line_val.pf_applicable):
                            line_list.append(line_val.total)

                    if len(line_list) != 0:
                        # esi_total = 0
                        for i in line_list:
                            print("DDDDDDDDDDDd", i)
                            total = total + i
                            print(total, 'hhhhhhhhhhh')
                            a = total * pf.employee_contribution / 100
                            pf_emp_total = round(a)
                            b = total * pf.employer_contribution / 100
                            pf_empr_total = round(b)
                            c = total * pf.employee_pension_scheme / 100
                            eps_total = round(c)
                            # print(eps_total, 'wwwwwwwwwwwwwwwwww')

                        for vals in check_box_pf:
                            pf_sal_limit = 0.0
                            if rule.pf_compute == True and line.pf_com == True:
                                # line.esi_com = rule.esi_compute
                                print('in first if')
                                # print(rec.struct_id.name)
                            if rec.employee_id.name == vals.name:
                                if vals.pf_applicable_check_box == True:
                                    if rec.struct_id.id == pf_struct.id:
                                        if pf_emp_contribution and line_payroll and eps_empr_contribution and pf_empr_contribution and pf_emp_contribution.amount_select == 'code':
                                            if total > pf.pf_salary_limit:
                                                epf_1 = (pf.pf_salary_limit * pf.employee_contribution) / 100
                                                emprpf_1 = (pf.pf_salary_limit * pf.employer_contribution) / 100
                                                eps_1 = (pf.pf_salary_limit * pf.employee_pension_scheme) / 100
                                                print(epf_1,emprpf_1,eps_1,'epfepseprmpf')
                                                x1 = round(epf_1)
                                                y1= round(emprpf_1)
                                                z1 = round(eps_1)
                                                print('x1y1z1')
                                                pf_emp_contribution.amount_python_compute = 'result = ' + str(x1)
                                                pf_empr_contribution.amount_python_compute = 'result = ' + str(y1)
                                                eps_empr_contribution.amount_python_compute = 'result = ' + str(z1)
                                            elif total < pf.pf_salary_limit:
                                                epf_2 = (total * pf.employee_contribution) /100
                                                empr_2 = (total * pf.employer_contribution) /100
                                                eps_2 = (total * pf.employee_pension_scheme) /100
                                                if eps_2 < pf.eps_limit:
                                                    x2 = round(epf_2)
                                                    y2 = round(empr_2)
                                                    z2 = round(eps_2)
                                                    print(x2,y2,z2,'x2y2z2')
                                                    pf_emp_contribution.amount_python_compute = 'result = ' + str(x2)
                                                    pf_empr_contribution.amount_python_compute = 'result = ' + str(y2)
                                                    eps_empr_contribution.amount_python_compute = 'result = ' + str(z2)
                                            # elif total < 9999999:
                                                elif eps_2 >= pf.eps_limit:
                                                    d = total * pf.employee_pension_scheme / 100
                                                    pf_sal_limit = round(d)
                                                    e = (pf_sal_limit - pf.eps_limit) + pf_empr_total
                                                    print(pf_sal_limit, pf.eps_limit, pf_empr_total, 'calculationeps')
                                                    print(e, 'calculation eeeeeeee')
                                                    empr_total = round(e)
                                                    eps_empr_contribution.amount_python_compute = 'result = ' + str(pf.eps_limit)
                                                    pf_empr_contribution.amount_python_compute = 'result = ' + str(empr_total)
                                                    pf_emp_contribution.amount_python_compute = 'result = ' + str(pf_emp_total)
                                                    # print(pf_sal_limit,'ddlllllllloooopppplllllllllllllllllllllllllllllllllllllllllllllllllllllllllll')

                                            # else:
                                            #     pf_empr_contribution.amount_python_compute = 'result = ' + str(pf_empr_total)
                                            #     eps_empr_contribution.amount_python_compute = 'result = ' + str(pf_sal_limit)
                                            #     print(eps_empr_contribution.amount_python_compute,'eps_empr_contribution')
                                else:
                                    pf_emp_contribution.amount_python_compute = 'result = ' + str(pf_not_value)
                                    pf_empr_contribution.amount_python_compute = 'result = ' + str(pf_not_value)
                                    eps_empr_contribution.amount_python_compute = 'result = ' + str(pf_not_value)

        return pf_emp_contribution.amount_python_compute, pf_empr_contribution.amount_python_compute, eps_empr_contribution.amount_python_compute

    ##############################################################

    def get_sum_salary_master(self):
        sum_salary_master = 0
        sum_cal_salary = 0
        lop_arr = self.env['hr.salary.rule'].search([])
        struct_sal_mast = self.env['hr.payroll.structure'].search([])
        for struct_sal in struct_sal_mast:
            for record in lop_arr:
                var = self.env['hr.payslip.line'].search([('name', '=', record.name)])
                for val in var:
                    if self.struct_id.id == struct_sal.id:
                        if record.name == val.name:
                            val.lop_applicable_field = record.lop_arrears

        for line in self.line_ids:
            if line.lop_applicable_field == True:
                print(f"Adding salary_master {line.salary_master} for line: {line.name}")
                sum_salary_master += line.salary_master
                sum_cal_salary = (sum_salary_master / self.struct_id.structure_days) * self.lop_arrear_field
                self.lop_arrear_total_amount = round(sum_cal_salary)

                print("Total sum_salary_master:", sum_salary_master)
                print("Total :", sum_cal_salary)
                print("Total amount:", self.lop_arrear_total_amount)
        return sum_salary_master

    # Making the tax components should be true
    def taxable_true(self):
        lop_arrr = self.env['hr.salary.rule'].search([])
        struct_emp_tax = self.env['hr.payroll.structure'].search([])
        for st_tax in struct_emp_tax:
            for records in lop_arrr:
                var = self.env['hr.payslip.line'].search([('name', '=', records.name)])
                for vall in var:
                    if self.struct_id.id == st_tax.id:
                        if records.name == vall.name:
                            vall.tax_bool = records.is_taxable

    def prep_salary_master(self):
        # Create a dictionary to store the salary_master values for each line
        salary_master_dict = {}
        vpay = 0
        for payslip in self:
            if not payslip.contract_id:
                continue

            contract = payslip.contract_id
            component_lines = contract.salary_rule_master

            for payslip_line in payslip.line_ids:
                code = payslip_line.code
                component = component_lines.filtered(lambda line: line.salary_code == code)

                if component:
                    # Store the salary_master value for each line in the dictionary
                    salary_master_dict[payslip_line.id] = component.salary_amount

        # After processing, set the salary_master values for each line from the dictionary
        for payslip_line in self.line_ids:
            if payslip_line.id in salary_master_dict:
                payslip_line.salary_master = salary_master_dict[payslip_line.id]
            for payslip in self:
                contract = self.env['hr.contract'].search([('employee_id', '=', payslip.employee_id.id),
                                                           ('name', '=', payslip.contract_id.name)])
                cpi = self.env['cpi.points'].search([])
                for da in contract:
                    for cpi_val in cpi:
                        for cpi_val_line in cpi_val.cpi_point_lines:
                            for line in payslip.line_ids:
                                for val in contract.salary_rule_master:
                                    if val.salary_code == 'BASIC':
                                        value = val.salary_amount
                                        if line.code == 'VPAY':
                                            vpay = line.salary_master = round(value * 35 / 100)
                                        if line.code == 'DA' and not cpi_val_line.effective_date_to:
                                            da.amount_da = round((value / 189) * cpi_val_line.cpi_points_payroll)
                                            line.salary_master = round(da.amount_da)
                                        if line.code == 'HRA':
                                            line.salary_master = round((value + vpay) * 10 / 100)
                                        if line.code == 'TA':
                                            line.salary_master = round((value + vpay) * 10 / 100)
                                # print(value, 'ffff')

    def overtime_payment(self):
        sum_overtime = 0
        sum_cal_overtime = 0
        ot_pay = self.env['hr.salary.rule'].search([])
        emp_struct_ot = self.env['hr.payroll.structure'].search([])
        for struct in emp_struct_ot:
            for rec in ot_pay:
                var = self.env['hr.payslip.line'].search([('name', '=', rec.name)])
                for val in var:
                    if self.struct_id.id == struct.id:
                        if rec.name == val.name:
                            val.ot_applicable = rec.ot_hours_applicable

        for line in self.line_ids:
            if line.ot_applicable == True:
                print(f"Adding overtime payment {line.salary_master} for line: {line.name}")
                sum_overtime += line.salary_master
                print(sum_overtime, 'sum overtime')
                sum_cal_overtime = ((sum_overtime / (self.struct_id.structure_days * 8)) * self.ot_hours * 2)
                self.ot_amount = round(sum_cal_overtime)
                print(sum_cal_overtime, 'sum cal overtime')

    # DA Calculation
    # def da_calculation(self):
    #     cpi = self.env['cpi.points'].search([])
    #     for cpi_val in cpi:
    #         for cpi_val_line in cpi_val.cpi_point_lines:
    #             for rec in self:
    #                 for line in rec.line_ids:
    #                     if line.code == 'BASIC':
    #                         amount_basic = line.total
    #                         print('amount basic')
    #                         if not cpi_val_line.effective_date_to:
    #                             rec.amount_da = (amount_basic / 189) * cpi_val_line.cpi_points_payroll
    #                             print(rec.amount_da,'amount da')




    def compute_sheet(self):
        print("computeeeeeeee")
        # Call the prep_salary_master method before computation
        self.prep_salary_master()

        # Temporarily disable recomputation of payslip lines during the computation
        with self.env.norecompute():
            # Call super to perform the default computation process
            super(InheritStructid, self).compute_sheet()

        # Recalculate PF and ESI after the computation process
        self.pf_calculation()
        self.esi_calculation()

        # Ensure the salary_master values are retained after computation
        self.prep_salary_master()
        self.get_sum_salary_master()
        self.overtime_payment()
        self.taxable_true()
        self.onchange_total_days()
        self.onchange_employee_insurance()

        # lop arrears calculation
    # @api.constrains('employee_id')
    # def get_sum_salary_master(self):
    #     payslip_lines = self.env['hr.payslip.line'].search([])
    #     sum_salary_master = 0
    #
    #     for line in payslip_lines:
    #         if line.lop_applicable_field:
    #             sum_salary_master += line.salary_master
    #             print(sum_salary_master, 'summmm')
    #
    #     return sum_salary_master

# getting total days in salary structure
#     @api.onchange('date_from', 'date_to')
    def onchange_total_days(self):
        structure = self.env['hr.payroll.structure'].search([('name','=','Journalists')])
        for rec in self:
            structure.structure_days = rec.total_days


        # getting lic value

    def onchange_employee_insurance(self):
        for rec in self:
            amount = self.env['insurance.policy'].search([('employee_code', '=', rec.employee_id.id)])
            rec.insurance_field = amount.total_sum_values
