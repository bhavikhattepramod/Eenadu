import time
from odoo import fields, models,_
import random,requests
from odoo.exceptions import ValidationError


class SendCustomSMS(models.Model):
    _inherit = 'res.company'

    sms_username = fields.Char(string="Username")
    sms_password = fields.Char(string="Password")
    from_number = fields.Char(string="From Number")


class SMSReta(models.Model):
    _inherit = 'sale.order'

    generated_otp = fields.Char("Generated Otp")

    def generate_otp(self):

        otp_generated = str(random.randint(100000, 999999))
        self.generated_otp = otp_generated

        sms_user_name = self.env.user.company_id.sms_username
        sms_password = self.env.user.company_id.sms_password
        from_number = self.env.user.company_id.from_number
        to_number = self.partner_id.mobile

        message_body = "One Time Password for EENADU (Advertisements) Online Booking to Update Mobile is "+ str(otp_generated)  +". Please use this OTP to Update Mobile.Regards EENADU"

        if self.reta_bool_field or self.classified_bool_field or self.nap_bool_field:
            if not self.is_terms_and_conditions and not self.is_consent_form:
                raise ValidationError('Please Accept the Consent Form and Terms&conditions')

            url = "https://www.smsstriker.com/API/sms.php?username=" + str(sms_user_name) + "&password=" + str(
                sms_password) + "&from=" + str(from_number) + "&to=" + str(to_number) + "&msg=" + str(
                message_body) + "&type=1&template_id=1407169114591748105"
            response = requests.post(url)
        ctx = dict()
        ctx = ({
            'default_customer_number': self.partner_id.mobile,
        })

        form_id = self.env.ref('eenadu_reta_sms.view_otp_verification_wizard').id

        return {
            'name': _('Otp Verification Wizard'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'otp.verification.wizard',
            'views_id': False,
            'views': [(form_id or False, 'form')],
            'target': 'new',
            'context': ctx,
        }


