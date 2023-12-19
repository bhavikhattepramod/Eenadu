from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    personal_name = fields.Char('Name')
    personal_mobile_num = fields.Char('Mobile No.')
    personal_mail = fields.Char('EMail')
    cast = fields.Char('Caste')
    sub_cast = fields.Char('Sub Caste')
    religion = fields.Char('Religion')
    date_reg = fields.Date('Date Of Registration')
    age = fields.Integer('Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Gender')
    profile_id = fields.Char('Profile Id')
    marital_status = fields.Selection([('yes', 'Yes'), ('no', 'No')], 'Marital status')
    register_by = fields.Char('Register By')
    location = fields.Char('Location')
    designation = fields.Char('Designation')
