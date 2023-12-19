from odoo import fields, models, api, _


class NewspaperPageDetails(models.Model):
    _name = 'newspaper.page.details'

    page_name = fields.Char('Page Name')
    name = fields.Integer('Page No')
    length = fields.Integer('Paper Length')
    width = fields.Integer('Paper Width')
    size = fields.Integer('Total Size(Sq.cm)', compute='_compute_paper_size')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    base_price = fields.Monetary('Amount', currency_field='currency_id')
    default_page_creation = fields.Boolean(string="Default Page Creation")

    def name_get(self):
        result = []
        for record in self:
            if record.page_name:
                display_name = "{} - {}".format(record.name, record.page_name)
            else:
                display_name = str(record.name)
            result.append((record.id, display_name))
        return result

    @api.depends('length','width')
    def _compute_paper_size(self):
        for rec in self:
            rec.size = rec.length * rec.width

    @api.model
    def update_page_info(self):
        info_records = self.env['newspaper.page.details'].search([])
        page_master_info = self.env['page.master.info']
        for info_record in info_records:
            vals = {
                'page_no': info_record.name,
                'length': info_record.length,
                'width': info_record.width,
                'date': fields.Date.today(),
                'total_size': info_record.size,
                'page_name_id': info_record.id,
            }
            if info_record.default_page_creation == True:
                page_master_info.create(vals)
