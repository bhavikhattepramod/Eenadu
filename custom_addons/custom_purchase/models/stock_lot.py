# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class StockLot(models.Model):
    _inherit = 'stock.lot'

    depth_of_cut = fields.Float('Depth of Cut')
    damage_qty = fields.Float('Damage QTY', compute="compute_damage_qty")
    net_qty = fields.Float("Net QTY", compute="_compute_net_qty")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    reel_price_unit = fields.Monetary("Unit Rate", currency_field="currency_id")
    reel_price_total = fields.Monetary("Amount", currency_field="currency_id", compute="_compute_reel_price_total")
    picking_id = fields.Many2one('stock.picking', string="Shipment Name")
    container_no = fields.Char('Container #')

    @api.depends('depth_of_cut')
    def compute_damage_qty(self):
        for rec in self:
            damage_qty = (((4.00 * rec.depth_of_cut) * (40.00 - rec.depth_of_cut))/((40.00 + 4.00)*(40.00 - 4.00)))*rec.product_qty
            rec.damage_qty = damage_qty

    @api.depends('reel_price_unit')
    def _compute_reel_price_total(self):
        for rec in self:
            rec.reel_price_total = rec.net_qty * rec.reel_price_unit


    @api.depends('product_qty','damage_qty')
    def _compute_net_qty(self):
        for rec in self:
            rec.net_qty = rec.product_qty - rec.damage_qty