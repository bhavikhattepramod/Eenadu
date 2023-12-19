# Copyright 2018-2019 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_STATES = [
    ("draft", "Draft"),
    ("to_approve", "To be approved"),
    ("approved", "Approved"),
    # ("accounts_approved", "Accounts Manager Approved"),
    # ("unit_manager_approved", "Unit Manager Approved"),
    # ("manager_approved", "Purchase Manager Approved"),
    ("rejected", "Rejected"),
    ("done", "Done"),
]


class PurchaseRequest(models.Model):

    _name = "purchase.request"
    _description = "Purchase Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    @api.model
    def _company_get(self):
        return self.env["res.company"].browse(self.env.company.id)

    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)

    @api.model
    def _get_default_name(self):
        return self.env["ir.sequence"].next_by_code("purchase.request")

    @api.model
    def _default_picking_type(self):
        type_obj = self.env["stock.picking.type"]
        company_id = self.env.context.get("company_id") or self.env.company.id
        types = type_obj.search(
            [("code", "=", "incoming"), ("warehouse_id.company_id", "=", company_id)]
        )
        if not types:
            types = type_obj.search(
                [("code", "=", "incoming"), ("warehouse_id", "=", False)]
            )
        return types[:1]

    # @api.depends("state")
    # def _compute_is_editable(self):
    #     for rec in self:
    #         if rec.state in ("to_approve", "approved", "rejected", "done"):
    #             rec.is_editable = False
    #         else:
    #             rec.is_editable = True

    name = fields.Char(
        string="Request Reference",
        required=True,
        default=lambda self: _("New"),
        tracking=True,
    )
    is_name_editable = fields.Boolean(
        default=lambda self: self.env.user.has_group("base.group_no_one"),
    )
    origin = fields.Char(string="Source Document")
    date_start = fields.Date(
        string="Creation date",
        help="Date when the user initiated the request.",
        default=fields.Date.context_today,
        tracking=True,
    )
    requested_by = fields.Many2one(
        comodel_name="res.users",
        required=True,
        copy=False,
        tracking=True,
        default=_get_default_requested_by,
        index=True,
    )
    assigned_accounts_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Accounts Manager",
        tracking=True,
        domain=lambda self: [
            (
                "groups_id",
                "in",
                self.env.ref("purchase_request.group_purchase_accounting_manager").id,
            )
        ],
        index=True,
    )
    assigned_unit_manager_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Unit Manager",
        tracking=True,
        domain=lambda self: [
            (
                "groups_id",
                "in",
                self.env.ref("purchase_request.group_purchase_unit_manager").id,
            )
        ],
        index=True,
    )
    assigned_manager_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Purchase Manager",
        tracking=True,
        domain=lambda self: [
            (
                "groups_id",
                "in",
                self.env.ref("purchase_request.group_purchase_request_manager").id,
            )
        ],
        index=True,
    )
    description = fields.Text()
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=False,
        default=_company_get,
        tracking=True,
    )
    line_ids = fields.One2many(
        comodel_name="purchase.request.line",
        inverse_name="request_id",
        string="Products to Purchase",
        readonly=False,
        copy=True,
        tracking=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        related="line_ids.product_id",
        string="Product",
        readonly=True,
    )
    state = fields.Selection(
        selection=_STATES,
        string="Status",
        index=True,
        tracking=True,
        required=True,
        copy=False,
        default="draft",
    )
    is_editable = fields.Boolean('Is Editable?', default=True, readonly=True)
    # is_editable = fields.Boolean(compute="_compute_is_editable", readonly=True)
    to_approve_allowed = fields.Boolean(compute="_compute_to_approve_allowed")
    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Picking Type",
        required=True,
        default=_default_picking_type,
    )
    group_id = fields.Many2one(
        comodel_name="procurement.group",
        string="Procurement Group",
        copy=False,
        index=True,
    )
    line_count = fields.Integer(
        string="Purchase Request Line count",
        compute="_compute_line_count",
        readonly=True,
    )
    move_count = fields.Integer(
        string="Stock Move count", compute="_compute_move_count", readonly=True
    )
    purchase_count = fields.Integer(
        string="Purchases count", compute="_compute_purchase_count", readonly=True
    )
    currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)
    estimated_cost = fields.Monetary(
        compute="_compute_estimated_cost",
        string="Total Estimated Cost",
        store=True,
    )

    is_accounts_manager_approval_required = fields.Boolean('Is Accounts Manager Approval Required?')
    is_unit_manager_approval_required = fields.Boolean('Is Unit Manager Approval Required?')
    is_purchase_manager_approval_required = fields.Boolean('Is Purchase Manager Approval Required?')


    is_accounts_manager_approved = fields.Boolean('Is Accounts Manager Approved?')
    is_unit_manager_approved = fields.Boolean('Is Unit Manager Approved?')
    is_purchase_manager_approved = fields.Boolean('Is Purchase Manager Approved?')
    is_all_approved = fields.Boolean("Is all approved?", compute='_compute_all_manager_approved')


    @api.depends('is_accounts_manager_approval_required','is_unit_manager_approval_required','is_purchase_manager_approval_required','is_accounts_manager_approved','is_unit_manager_approved','is_purchase_manager_approved')
    def _compute_all_manager_approved(self):
        for rec in self:
            print(rec)
            if rec.is_accounts_manager_approval_required == True and rec.is_unit_manager_approval_required == True and rec.is_purchase_manager_approval_required == True and rec.is_accounts_manager_approved == True and rec.is_unit_manager_approved == True and rec.is_purchase_manager_approved == True:
                rec.is_all_approved = True
                rec.state = 'approved'
            elif rec.is_unit_manager_approval_required == True and rec.is_purchase_manager_approval_required == True and rec.is_unit_manager_approved == True and rec.is_purchase_manager_approved == True:
                rec.is_all_approved = True
                rec.state = 'approved'
            elif rec.is_purchase_manager_approval_required == True and rec.is_purchase_manager_approved == True:
                rec.is_all_approved = True
                rec.state = 'approved'
            else:
                rec.is_all_approved = False
                rec.state = 'to_approve'

    @api.onchange('is_all_approved')
    def onchage_is_all_approved(self):
        if self.is_all_approved == True:
            self.state = 'approved'

    def action_create_purchase_quotation(self):
        ctx = dict()

        for rec in self:
            purchase_request_lines_list = []
            for record in rec.line_ids:
                print(record.rfq_created,'----rfq_created----')
                if record.rfq_created == True:
                    create_rfq = True
                else:
                    create_rfq = False
                print(create_rfq,'---create_rfq---')
                purchase_request_lines_list.append((0, 0, {
                    'purchase_request_id': rec.id,
                    'product_id': record.product_id.id,
                    'name': record.name,
                    'product_qty': record.product_qty,
                    'product_uom_id': record.product_uom_id.id,
                    'purchase_request_line_id': record.id,
                    'rfq_created' : record.rfq_created,
                    'create_rfq' : create_rfq,
                }))

        ctx = ({
            'default_create_rfq_line_ids': purchase_request_lines_list,
            'default_purchase_request_id': self.id
        })

        form_id = self.env.ref('purchase_request.create_rfq_form_view').id

        return {
            'name': _('Create RFQ'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.rfq.wizard',
            'views_id': False,
            'views': [(form_id or False, 'form')],
            'target': 'new',
            'context': ctx,
        }

    @api.depends("line_ids", "line_ids.estimated_cost")
    def _compute_estimated_cost(self):
        for rec in self:
            rec.estimated_cost = sum(rec.line_ids.mapped("estimated_cost"))

    # @api.depends("line_ids")
    def _compute_purchase_count(self):
        for rec in self:
            rec.purchase_count = len(self.env['purchase.order'].search([('purchase_request_id', '=', rec.id)]))
            # rec.purchase_count = len(rec.mapped("line_ids.purchase_lines.order_id"))

    def action_view_purchase_order(self):
        return {
            'name': _('Purchase Order'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'domain': [('purchase_request_id', '=', self[0].id)],
            'views_id': False,
            'views': [(self.env.ref('purchase.purchase_order_kpis_tree').id or False, 'tree'),
                      (self.env.ref('purchase.purchase_order_form').id or False, 'form')],
        }
        # action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        # lines = self.mapped("line_ids.purchase_lines.order_id")
        # if len(lines) > 1:
        #     action["domain"] = [("id", "in", lines.ids)]
        # elif lines:
        #     action["views"] = [
        #         (self.env.ref("purchase.purchase_order_form").id, "form")
        #     ]
        #     action["res_id"] = lines.id
        # return action

    @api.depends("line_ids")
    def _compute_move_count(self):
        for rec in self:
            rec.move_count = len(
                rec.mapped("line_ids.purchase_request_allocation_ids.stock_move_id")
            )

    def action_view_stock_picking(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.action_picking_tree_all"
        )
        # remove default filters
        action["context"] = {}
        lines = self.mapped(
            "line_ids.purchase_request_allocation_ids.stock_move_id.picking_id"
        )
        if len(lines) > 1:
            action["domain"] = [("id", "in", lines.ids)]
        elif lines:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = lines.id
        return action

    @api.depends("line_ids")
    def _compute_line_count(self):
        for rec in self:
            rec.line_count = len(rec.mapped("line_ids"))

    def action_view_purchase_request_line(self):
        action = (
            self.env.ref("purchase_request.purchase_request_line_form_action")
            .sudo()
            .read()[0]
        )
        lines = self.mapped("line_ids")
        if len(lines) > 1:
            action["domain"] = [("id", "in", lines.ids)]
        elif lines:
            action["views"] = [
                (self.env.ref("purchase_request.purchase_request_line_form").id, "form")
            ]
            action["res_id"] = lines.ids[0]
        return action

    @api.depends("state", "line_ids.product_qty", "line_ids.cancelled")
    def _compute_to_approve_allowed(self):
        for rec in self:
            rec.to_approve_allowed = rec.state == "draft" and any(
                not line.cancelled and line.product_qty for line in rec.line_ids
            )

    def copy(self, default=None):
        default = dict(default or {})
        self.ensure_one()
        default.update({"state": "draft", "name": self._get_default_name()})
        return super(PurchaseRequest, self).copy(default)

    @api.model
    def _get_partner_id(self, request):
        user_id = request.assigned_accounts_user_id or self.env.user
        return user_id.partner_id.id
        unit_manager_user_id = request.assigned_unit_manager_user_id or self.env.user
        return unit_manager_user_id.partner_id.id
        manager_user_id = request.assigned_manager_user_id or self.env.user
        return manager_user_id.partner_id.id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self._get_default_name()
        requests = super(PurchaseRequest, self).create(vals_list)

        if self.env.user.has_group('purchase_request.group_purchase_request_user'):
            requests.is_accounts_manager_approval_required = True
            requests.is_unit_manager_approval_required = True
            requests.is_purchase_manager_approval_required = True
        elif self.env.user.has_group('purchase_request.group_purchase_accounting_manager'):
            requests.is_unit_manager_approval_required = True
            requests.is_purchase_manager_approval_required = True
        elif self.env.user.has_group('purchase_request.group_purchase_unit_manager'):
            requests.is_purchase_manager_approval_required = True
        elif self.env.user.has_group('purchase_request.group_purchase_request_manager'):
            requests.state = 'approved'
        else:
            requests.is_accounts_manager_approval_required = False
            requests.is_unit_manager_approval_required = False
            requests.is_purchase_manager_approval_required = False        

        for vals, request in zip(vals_list, requests):
            if vals.get("assigned_accounts_user_id"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
            if vals.get("assigned_unit_manager_user_id"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
            if vals.get("assigned_manager_user_id"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
        return requests

    def write(self, vals):
        res = super(PurchaseRequest, self).write(vals)
        for request in self:
            if vals.get("assigned_accounts_user_id"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
            if vals.get("assigned_unit_manager_user_id"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
            if vals.get("assigned_manager_user_id"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
        return res

    def _can_be_deleted(self):
        self.ensure_one()
        return self.state == "draft"

    def unlink(self):
        for request in self:
            if not request._can_be_deleted():
                raise UserError(
                    _("You cannot delete a purchase request which is not draft.")
                )
        return super(PurchaseRequest, self).unlink()

    def button_draft(self):
        self.mapped("line_ids").do_uncancel()
        return self.write({"state": "draft"})

    def button_to_approve(self):
        self.to_approve_allowed_check()
        return self.write({"state": "to_approve"})

    def button_accounts_approved(self):
        self.is_accounts_manager_approved = True
        # return self.write({"state": "accounts_approved"})

    def button_unit_manager_approved(self):
        self.is_unit_manager_approved = True
        # return self.write({"state": "unit_manager_approved"})

    def button_manager_approved(self):
        self.is_purchase_manager_approved = True
        # return self.write({"state": "manager_approved"})

    def button_rejected(self):
        self.mapped("line_ids").do_cancel()
        return self.write({"state": "rejected"})

    def button_done(self):
        return self.write({"state": "done"})

    def check_auto_reject(self):
        """When all lines are cancelled the purchase request should be
        auto-rejected."""
        for pr in self:
            if not pr.line_ids.filtered(lambda l: l.cancelled is False):
                pr.write({"state": "rejected"})

    def to_approve_allowed_check(self):
        for rec in self:
            if not rec.to_approve_allowed:
                raise UserError(
                    _(
                        "You can't request an approval for a purchase request "
                        "which is empty. (%s)"
                    )
                    % rec.name
                )
