# -*- coding: utf-8 -*-

from odoo import _, api, fields, tools, models

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    depth_of_cut = fields.Float('Depth of Cut')
    damage_qty = fields.Float('Damage QTY', compute="compute_damage_qty")
    net_qty = fields.Float("Net QTY", compute="_compute_net_qty")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    reel_price_unit = fields.Monetary("Unit Rate", currency_field="currency_id")
    reel_price_total = fields.Monetary("Amount", currency_field="currency_id", compute="_compute_reel_price_total")
    container_no = fields.Char("Container #")
    lot_id = fields.Many2one('stock.lot', 'Lot/Serial Number', check_company=True)

    @api.depends('depth_of_cut')
    def compute_damage_qty(self):
        for rec in self:
            damage_qty = (((4.00 * rec.depth_of_cut) * (40.00 - rec.depth_of_cut))/((40.00 + 4.00)*(40.00 - 4.00)))*rec.qty_done
            rec.damage_qty = damage_qty

    @api.onchange('qty_done', 'product_uom_id')
    def _onchange_qty_done(self):
        """ When the user is encoding a move line for a tracked product, we apply some logic to
        help him. This onchange will warn him if he set `qty_done` to a non-supported value.
        """
        res = {}
        if self.qty_done and self.product_id.tracking == 'serial':
            qty_done = self.product_uom_id._compute_quantity(self.qty_done, self.product_id.uom_id)
            if float_compare(qty_done, 1.0, precision_rounding=self.product_id.uom_id.rounding) != 0:
                message = _('You can only process 1.0 %s of products with unique serial number.', self.product_id.uom_id.name)
                res['warning'] = {'title': _('Warning'), 'message': message}
        return res

    @api.onchange('lot_id')
    def _onchange_lot_id(self):
        self.depth_of_cut = self.lot_id.depth_of_cut
        self.qty_done = self.lot_id.product_qty
        self.damage_qty = self.lot_id.damage_qty

    @api.depends('reel_price_unit')
    def _compute_reel_price_total(self):
        for rec in self:
            rec.reel_price_total = rec.net_qty * rec.reel_price_unit


    @api.depends('qty_done','damage_qty')
    def _compute_net_qty(self):
        for rec in self:
            rec.net_qty = rec.qty_done - rec.damage_qty


    def _get_value_production_lot(self):
        self.ensure_one()
        return {
            'company_id': self.company_id.id,
            'name': self.lot_name,
            'product_id': self.product_id.id,
            'depth_of_cut': self.depth_of_cut,
            'damage_qty': self.damage_qty,
            'reel_price_unit': self.reel_price_unit,
            'picking_id': self.picking_id.id,
            'container_no': self.container_no,
        }