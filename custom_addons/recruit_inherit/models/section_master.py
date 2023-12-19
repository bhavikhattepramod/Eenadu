from odoo import fields,models

class Sectionmaster(models.Model):
    _name = "section.master"

    section_code = fields.Char(string="Section Code")
    name = fields.Char(string="Section Name")
    section_incharge1 = fields.Many2one('hr.employee.public',string="Section Incharge 1")
    section_incharge2 = fields.Many2one('hr.employee.public',string="Section Incharge 2")