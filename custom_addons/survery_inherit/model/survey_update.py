import base64
import binascii
from odoo import fields, models, api,_
from odoo.http import request


class HrFormUpdate(models.Model):
    _inherit = "survey.survey"

    candidate_details_applicable = fields.Boolean(string="Candidate details applicable")


class SurveyFormApplication(models.Model):
    _inherit = 'survey.user_input'

    @api.constrains('state')
    def button_data(self):
        checkbox = self.env['survey.survey'].search([])
        if self.user_input_line_ids.attachment_ids:
            attachment = self.user_input_line_ids.attachment_ids
            print(attachment,'grrrrryt')
        for rec in checkbox:
            if rec.candidate_details_applicable == True:
                if self.state == 'done':
                    result_list = []
                    for val in self.user_input_line_ids:
                        result_list.append(val.display_name)
                    print(result_list, "res")
                    applicant = self.env['hr.applicant'].create({
                        'name': result_list[0],
                        'partner_name': result_list[1],
                        'email_from': result_list[2],
                        'partner_mobile': result_list[3],
                        'location': result_list[4],
                        'attachement_id1': attachment,
                        'no_of_rounds': 0,
                    })
                    return applicant


class HrApplicantAttachmentField(models.Model):
    _inherit = "hr.applicant"

    attachement_id1 = fields.Many2many('ir.attachment',string='Attachment ID', required=True)


