from odoo import fields, models,_
import random,requests
from odoo.exceptions import ValidationError


class OTPVerification(models.TransientModel):
    _name = 'otp.verification.wizard'
    _description = 'Otp Verification Wizard'

    customer_number = fields.Char('Customer Number')
    otp_number = fields.Char("Enter OTP")

    def confirm_and_send_sms(self):
        active_id = self._context.get('active_id')
        sale_order_obj = self.env['sale.order'].search([('id', '=', int(active_id))])
        sms_user_name = self.env.user.company_id.sms_username
        sms_password = self.env.user.company_id.sms_password
        from_number = self.env.user.company_id.from_number
        customer_name = sale_order_obj.partner_id.name
        to_number = sale_order_obj.partner_id.mobile
        message_body = "Dear " + str(customer_name) + ",Thanks for placing an order. Your advertisement will be published as scheduled.Regards EENADU"
        if self.otp_number == False:
            raise ValidationError("Please Enter OTP")
        elif self.otp_number != sale_order_obj.generated_otp:
            raise ValidationError("Please Enter Valid OTP")
        elif self.otp_number == sale_order_obj.generated_otp:
            sale_order_obj.sudo().send_for_scheduling()

            url = "https://www.smsstriker.com/API/sms.php?username=" + str(sms_user_name) + "&password=" + str(
                sms_password) + "&from=" + str(from_number) + "&to=" + str(to_number) + "&msg=" + str(
                message_body) + "&type=1&template_id=1407169095670840304"
            response = requests.post(url)

        return

    def resend_otp(self):

        otp_generated = str(random.randint(100000, 999999))
        active_id = self._context.get('active_id')
        sale_order_obj = self.env['sale.order'].search([('id', '=', int(active_id))])
        sale_order_obj.generated_otp = otp_generated
        to_number = sale_order_obj.partner_id.mobile
        sms_user_name = self.env.user.company_id.sms_username
        sms_password = self.env.user.company_id.sms_password
        from_number = sale_order_obj.partner_id.mobile

        message_body = "One Time Password for EENADU (Advertisements) Online Booking to Update Mobile is "+ str(otp_generated)  +". Please use this OTP to Update Mobile.Regards EENADU"
        url = "https://www.smsstriker.com/API/sms.php?username=" + str(sms_user_name) + "&password=" + str(
            sms_password) + "&from=" + str(from_number) + "&to=" + str(to_number) + "&msg=" + str(
            message_body) + "&type=1&template_id=1407169114591748105"
        response = requests.post(url)

        ctx = dict()

        ctx = ({
            'default_customer_number': sale_order_obj.partner_id.mobile,
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