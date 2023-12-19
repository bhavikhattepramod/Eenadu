from odoo import fields,models

class Unitmaster(models.Model):
    _name = "unit.master"

    unit_code = fields.Char(string="Unit Code")
    name = fields.Char(string="Unit Name")
    unit_address = fields.Text(string="Unit Address")
    pincode = fields.Char(string="Pincode")
    unit_incharge1 = fields.Many2one('hr.employee.public',string="Unit Incharge 1")
    unit_incharge2 = fields.Many2one('hr.employee.public',string="Unit Incharge 2")
