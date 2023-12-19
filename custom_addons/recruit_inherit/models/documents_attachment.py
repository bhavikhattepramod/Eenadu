from odoo import fields,models,_


class Documentsattach(models.Model):
    _name = 'document.attachment'

    name = fields.Char(string="Name of Document")
    file_attach = fields.Binary(string="Attach the File")
    doc_attach_emp = fields.Many2one('hr.employee',string='Employee Name')


class Certificatesattach(models.Model):
    _inherit = 'hr.employee'

    doc_emp = fields.One2many('document.attachment', 'doc_attach_emp')
