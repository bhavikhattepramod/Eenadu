from odoo import api, fields, models
from datetime import datetime,date,timedelta
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta



class AdsType(models.Model):
    _name = 'ads.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Repetitive Ads Notifications"

    ad_name = fields.Many2one('product.template', string='Ads Name', readonly='1')
    name = fields.Many2one('res.partner', string='Customer Name', readonly='1')
    agent_name = fields.Many2one('res.partner', string='Agent Name', readonly='1',)
    category_name = fields.Many2one('category.discount', string='Category Name', readonly='1')
    category_type = fields.Selection([('repetitive', 'Repetitive'),
                                      ('non_repetitive', 'Non-Repetitive')], readonly='1')
    published_date = fields.Date(string='Published Date', readonly='1')
    remainder_duration = fields.Integer(string='Remainder Duration', default=30)
    date_extract = fields.Date(string='Date Extract', compute="_compute_published_date")
    # current_date = fields.Date(string='Current Date', default=fields.Datetime.now, readonly=True)

    notification_date = fields.Date(string='Notification Date', compute="compute_notification_datee")
    duration = fields.Char(string='Duration', compute='_compute_duration')

    def compute_agent_name(self):

        print("welcome")
        # for res in self:
        #     agent = self.env['sale.order'].search([('name', '=', res.invoice_origin)])
        #     if agent:
        #         res.agent_name = agent.agent_name.id
        #         res.reta_bool_field = agent.reta_bool_field
        #     if not res.agent_name and res.reta_bool_field:
        #         continue



    def get_repetitive_details(self):
        repetitive_ids = self.env['category.discount'].search([('category_type', '=', 'repetitive')])
        repetitive_records = self.env['sale.order.line'].search([('special_discount', '=', repetitive_ids.ids)])
        ads_type_obj = self.env['ads.type']
        if repetitive_records:
            for line in repetitive_records:
                ads_type_obj.create({

                        'ad_name':line.product_template_id.id,
                        'name' :line.order_id.partner_id.id,
                        'agent_name':line.order_id.agent_name.id,
                        'category_type':line.special_discount.category_type,
                        'published_date':line.order_id.specific_date,
                        'category_name' :line.special_discount.id,

                         })

    @api.depends('notification_date')
    def _compute_duration(self):
        for rec in self:
            if rec.notification_date:
                duration = rec.notification_date - date.today()
                rec.duration = duration.days
            else:
                rec.duration = 0

    @api.constrains('remainder_duration')
    def _check_remainder_duration(self):
        for record in self:
            if record.remainder_duration == 0:
                raise ValidationError("Remainder Duration must be greater than 0.")

    def create_activities(self):
        model_id = self.env['ir.model'].search([('model', '=', 'ads.type')])
        remainder_records = self.env['ads.type'].search([])
        for record in remainder_records:
            notification_date = fields.Date.from_string(record.notification_date)
            current_date = date.today()

            if notification_date == current_date:
                self.env['mail.activity'].sudo().create({
                    'date_deadline': record.notification_date,
                    'res_model_id': model_id.id,
                    'user_id': record.agent_name.id,
                    'res_id': record.id
                })
                self._compute_published_date()

    @api.depends('published_date')
    def _compute_published_date(self):
        for rec in self:
            if rec.published_date:
                next_year = (rec.published_date + relativedelta(years=1)).replace(year=rec.published_date.year + 1)
                rec.date_extract = next_year

    @api.depends('date_extract', 'remainder_duration')
    def compute_notification_datee(self):
        for rec in self:
            if rec.date_extract and rec.remainder_duration:
                rec.notification_date = rec.date_extract - timedelta(days=rec.remainder_duration)
            else:
                rec.notification_date = False







