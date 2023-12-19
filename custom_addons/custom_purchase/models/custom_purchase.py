from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _compute_international_insurance_claim_count(self):
        claim_insurance_obj = self.env['claim.international.insurance'].search([('purchase_order_id', '=', self.id)])

        self.international_insurance_claim_count = len(claim_insurance_obj)

    def _compute_ship_onboard_count(self):
        ship_onboard_obj = self.env['ship.onboard'].search([('purchase_order_id', '=', self.id)])
        
        self.ship_onboard_count = len(ship_onboard_obj)


    international_insurance_claim_count = fields.Integer(string = 'Claim Count', compute='_compute_international_insurance_claim_count')

    ship_onboard_count = fields.Integer(string = 'Ship On-Board Count', compute='_compute_ship_onboard_count')

    supporting_documents_line_ids = fields.One2many('supporting.documents', 'supporting_documents_line_id', string = 'Supporting Documents')

    agent_partner_id = fields.Many2one('res.partner', string = "Agent")
    manufacturer_id = fields.Many2one('newsprint.manufacturer', string = "Manufacturer")

    delivery_date_from = fields.Date('From Date')
    delivery_date_to = fields.Date('To Date')

    product_uom_category_ids = fields.Many2many('product.category',string="Product Category", compute="compute_product_uom_category_ids", store=True)

    #Computaion of Product categery for filters
    @api.depends('order_line')
    def compute_product_uom_category_ids(self):
        for rec in self:
            product_category_list = []
            for line in rec.order_line:
                if line.product_id.categ_id:
                    if line.product_id.categ_id.id not in product_category_list:
                        product_category_list.append(line.product_id.categ_id.id)
                    else:
                        product_category_list = product_category_list
                else:
                    product_category_list = product_category_list

            rec.product_uom_category_ids = product_category_list


    def action_create_ship_onboard(self):
        ctx = dict()

        ctx = ({
            'default_purchase_order_id': self.id,
            'default_vendor_partner_id': self.partner_id.id,
        })

        form_id = self.env.ref('custom_purchase.ship_onboard_form_view').id

        return {
            'name': _('Ship On-Board Details'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ship.onboard',
            'views_id': False,
            'views': [(form_id or False, 'form')],
            'target': 'new',
            'context': ctx,
        }

    def action_view_ship_onboard(self):

        return {
            'name': _('Ship On-Board Details'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'ship.onboard',
            'domain': [('purchase_order_id', '=', self[0].id)],
            'views_id': False,
            'views': [(self.env.ref('custom_purchase.ship_onboard_tree_view').id or False, 'tree'),
                      (self.env.ref('custom_purchase.ship_onboard_form_view').id or False, 'form')],
        }


    def action_create_international_insurance_claim(self):
        ctx = dict()

        ctx = ({
            'default_purchase_order_id': self.id,
            'default_vendor_partner_id': self.partner_id.id,
        })

        form_id = self.env.ref('custom_purchase.claim_international_insurance_form_view').id

        return {
            'name': _('Claim International Insurance'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'claim.international.insurance',
            'views_id': False,
            'views': [(form_id or False, 'form')],
            'target': 'new',
            'context': ctx,
        }

    def action_view_international_insurance_claim(self):

        return {
            'name': _('International Insurance Claim'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'claim.international.insurance',
            'domain': [('purchase_order_id', '=', self[0].id)],
            'views_id': False,
            'views': [(self.env.ref('custom_purchase.claim_international_insurance_tree_view').id or False, 'tree'),
                      (self.env.ref('custom_purchase.claim_international_insurance_form_view').id or False, 'form')],
        }

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     if self.env.user.purchase_document_access == 'own':
    #         args += [('user_id', '=', self.env.user.id)]
    #     elif self.env.user.purchase_document_access == 'all':
    #         if self.env.user.has_group('base.group_erp_manager'):
    #             return super(PurchaseOrder, self).search(args, offset=offset, limit=limit, order=order,
    #                                                             count=count)
    #         else:
    #             user_groups = self.env.user.groups_id.ids
    #             args += ['|', ('user_id', '=', self.env.user.id), ('user_id', 'in', user_groups)]
    #     return super(PurchaseOrder, self).search(args, offset=offset, limit=limit, order=order, count=count)

class SupportingDocuments(models.Model):
    _name = 'supporting.documents'

    name = fields.Char('Name of Document')
    document_attached = fields.Binary("Attachment", attachment=True)
    supporting_documents_line_id = fields.Many2one('purchase.order', string = 'Supporting Documents Line Ref')