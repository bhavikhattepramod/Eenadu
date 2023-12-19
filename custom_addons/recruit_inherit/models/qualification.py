from odoo import fields,models

class Qualification(models.Model):
    _name = "educate.qualification"

    name = fields.Char(string="Qualification")