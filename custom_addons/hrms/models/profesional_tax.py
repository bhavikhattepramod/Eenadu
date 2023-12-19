from odoo import fields, models


class ProfessionalTax(models.Model):
    _name = 'professional.tax'

    name = fields.Many2one('res.country.state', string='Name of State')
    gross_line_ids = fields.One2many('res.state.line', 'gross_amount_id')


class StateTax(models.Model):
    _name = 'res.state.line'

    gross_min = fields.Float('Gross Min')
    gross_max = fields.Float('Gross Max')
    gross_value = fields.Float('PT Tax')
    gross_amount_id = fields.Many2one('professional.tax')


class HrPaySlipPT(models.Model):
    _inherit = 'hr.payslip'

    pt_amount = fields.Float(string='PT Amount')

    # Getting the gross from the pre-processing payslip and  compare the gross state wise from that PT amount
    def get_gross(self):
        for rec in self:
            state_val = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
            structure_emp = self.env['hr.payroll.structure'].search([])
            from_state = self.env['professional.tax'].search([('name', '=', state_val.state_id_emp.id)])
            emp_pt = self.env['hr.salary.rule'].search([('code', '=', 'PT')])
            for struct in structure_emp:
                for amt in from_state.gross_line_ids:
                    if state_val.state_id_emp.id == from_state.name.id:
                        for val in rec.line_ids:
                            if val.name == 'Gross':
                                if amt.gross_min < val.total < amt.gross_max:
                                    # rec.pt_amount = amt.gross_value
                                    if rec.struct_id.id == struct.id:
                                        if emp_pt.is_professional:
                                            # got = self.env['hr.payslip.line'].search(
                                            #     [('name', '=', 'Profession Tax'), ('slip_id', '=', self.id)])
                                            emp_pt.amount_python_compute = 'result = ' + str(amt.gross_value)
                                            # got.update({'total': rec.pt_amount})
            return emp_pt.amount_python_compute

    def compute_sheet(self):
        for recs in self:
            super(HrPaySlipPT, recs).compute_sheet()
            recs.get_gross()
            super(HrPaySlipPT, recs).compute_sheet()
        return
