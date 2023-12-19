from odoo import fields, models, api, _

class ResUsersInherit(models.Model):
    _inherit = 'res.users'
    
    purchase_document_access = fields.Selection([
        ('own', 'Own Document'),
        ('all', 'All Document'),
        ('admin', 'Administrator')
    ], string='Purchase Document Access')