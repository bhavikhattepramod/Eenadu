from odoo import fields,models

class Familydetails(models.Model):
    _inherit = 'res.family'

    occupation = fields.Char(string='Occupation')
    monthly_income = fields.Float(string='Monthly Income')


class Emprelation(models.Model):
    _name = 'employee.relation'

    name = fields.Char(string='Name')
    designation = fields.Char(string='Designation')
    type = fields.Selection([('relation','Relation'),('friend','Friend')],string='Type')
    organization_relation = fields.Many2one('hr.employee',string='Organization')


class Addrelation(models.Model):
    _inherit = 'hr.employee'


    family_relation = fields.One2many('employee.relation','organization_relation',string='Organisation')