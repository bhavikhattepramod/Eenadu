from odoo import fields,models,api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Empdetails(models.Model):
    _inherit = 'hr.employee'

    native_place = fields.Many2one('employ.place',string="Native Place", tracking=True)
    native_district = fields.Many2one('employ.district',string="Native District", tracking=True)
    date_joining = fields.Date(string="Date Of Joining (Company)", tracking=True, compute='_compute_date_joining')
    emp_cat = fields.Many2one('general.category', string="General Category", tracking=True)
    handi_caps = fields.Selection([('yes', 'YES'), ('no', 'NO')], string='Handicap', default='no', tracking=True)
    mother_tongue = fields.Many2one('native.language',string="Mother Tongue", tracking=True)
    place_id = fields.Many2one("employ.place",string="Place of Birth", tracking=True)
    retired_age = fields.Date(string="Retirement Date" ,compute='_compute_retired_age', store=True, tracking=True)
    pf_number = fields.Char(string="PF Number", tracking=True)
    emp_nationality = fields.Char(string="Nationality",default='INDIAN', tracking=True)

    @api.depends('contract_ids.state', 'contract_ids.date_of_join_company')
    def _compute_date_joining(self):
        for employee in self:
            contracts = employee._get_first_contracts()
            if contracts:
                employee.date_joining = min(contracts.mapped('date_of_join_company'))
            else:
                employee.date_joining = False


    # Retirement age
    @api.depends('birthday')
    def _compute_retired_age(self):
        for rec in self:
            if rec.birthday:
                r_age = self.env['res.company'].search([])
                retirement_age = r_age.retire_age
                birth_date = datetime.strptime(str(rec.birthday), "%Y-%m-%d").date()
                retired_aged = birth_date + relativedelta(years=+retirement_age)
                retired_age = retired_aged + relativedelta(day=31)
                rec.retired_age = retired_age.strftime("%Y-%m-%d")
            else:
                rec.retired_age = False


class Empqualification(models.Model):
    _inherit = 'res.background'

    qualification_id = fields.Many2one('educate.qualification', string="Qualification", tracking=True)
    qualification_type = fields.Selection([('academic','Academic'),('technical','Technical'),
                                          ('professional','Professional'),('certification','Certification')],string="Qualification Type", tracking=True)
    year_passing = fields.Char(string="Year of Passing", tracking=True)
    percent = fields.Float(string="% of Marks", tracking=True)


class Nativeplace(models.Model):
    _name = "employ.place"

    name = fields.Char(string="Name")

class Nativedistrict(models.Model):
    _name = "employ.district"

    name = fields.Char(string="Name")


class Nativelang(models.Model):
    _name = 'native.language'

    name = fields.Char(string="Name")



