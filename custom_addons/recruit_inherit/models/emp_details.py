from odoo import models,fields,api


class Empdetails(models.Model):
    _inherit = 'hr.employee'


    height = fields.Float(string='Height (Cms)', tracking=True)
    weight = fields.Float(string='Weight (Kgs)', tracking=True)
    left_eye = fields.Char(string='Left Eye (Sight)', tracking=True)
    right_eye = fields.Char(string="Right Eye (Sight)", tracking=True)
    identification_mark1 = fields.Text(string="Identification Marks 1", tracking=True)
    identification_mark2 = fields.Text(string="Identification Marks 2", tracking=True)
    unit_name_hr = fields.Many2many('unit.master',string='Unit Name', tracking=True)
    section_name_hr = fields.Many2many('section.master',string='Section Name', tracking=True)

    @api.onchange('state_id_emp')
    def _onchange_state_id_emp(self):
        if self.state_id_emp.country_id:
            self.country_id_emp = self.state_id_emp.country_id

    @api.onchange('state_id_permanent')
    def _onchange_state_id_permanent(self):
        if self.state_id_permanent.country_id:
            self.country_id_permanent = self.state_id_permanent.country_id


class Department(models.Model):
    _inherit = "hr.department"

    dep_code = fields.Char(string="Department Code")
