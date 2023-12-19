from odoo import api, fields, models


class MrpPages(models.Model):
    _inherit = 'res.partner'

    edition_page_details = fields.Many2one('mrp.production')
    district_page_details = fields.Many2one('mrp.production')
    zone_page_details = fields.Many2one('mrp.production')


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    partner_id = fields.Many2one('res.partner', string='Newsprint Unit', readonly=True)
    order_qty = fields.Integer(string='Order Quantity', readonly=True)
    newspaper_date = fields.Date('Newspaper Date', readonly=True)  # newsly add
    damage_qty = fields.Float(string='Damage Quantity')
    buffer_percentage = fields.Integer(string='Buffer(%)')
    region_zones = fields.Many2one('res.partner', string='Region')
    # res_regions = fields.Many2one('res.partner', 'Res Regions')
    region_res = fields.Char('Regions')
    active = fields.Boolean('Active', default=True, tracking=True)


    # page_details = fields.One2many('page.details', 'm2o_id')
    # district_page_details = fields.One2many('page.details', 'm2o_district_id')
    # zone_page_details = fields.One2many('page.details', 'm2o_zone_id')
    district_page_details = fields.Many2many('res.partner', 'district_page_details', string='District',
                                             compute='compute_districts_parent_id')
    edition_page_details = fields.Many2many('res.partner', 'edition_page_details', string='Editions',
                                            compute='compute_edition_parent_id')
    zone_page_details = fields.Many2many('res.partner', 'zone_page_details', string='Zones')

    def action_generate_serial(self):
        self.ensure_one()
        ir_seq = self.env['ir.sequence'].search([('category_id', '=', self.product_id.categ_id.id)])
        lot_no = self.env['ir.sequence'].next_by_code(ir_seq.code)
        self.lot_producing_id = self.env['stock.lot'].create({
            'product_id': self.product_id.id,
            'company_id': self.company_id.id,
            'name': lot_no,
            'newspaper_date': self.newspaper_date,
            'order_qty': self.order_qty,
            'damage_qty': self.damage_qty,
        })
        if self.move_finished_ids.filtered(lambda m: m.product_id == self.product_id).move_line_ids:
            self.move_finished_ids.filtered(
                lambda m: m.product_id == self.product_id).move_line_ids.lot_id = self.lot_producing_id
        if self.product_id.tracking == 'serial':
            self._set_qty_producing()

    def compute_districts_parent_id(self):
        district_parents = []
        search_edition = self.env['res.partner'].search([]).district_o2m
        for dis in search_edition:
            for rec in dis.zone_o2m:
                if rec == self.region_zones:
                    district_parents.append(dis.id)
        self.district_page_details = district_parents

    def compute_edition_parent_id(self):
        parent = []
        search_edition = self.env['res.partner'].search([])
        for rec in search_edition:
            for dis in rec.district_o2m:
                if dis in self.district_page_details:
                    parent.append(rec.id)
        self.edition_page_details = parent

    def mrp_confirm(self):
        for confirm in self:
            confirm.action_confirm()

    def buffer_copies_percentage(self):
        self.product_qty += round(self.buffer_percentage/100 * self.product_qty)
        return True


class MrpConfirm(models.Model):
    _inherit = 'sale.order'

    active = fields.Boolean('Active', default=True, tracking=True)

    # creating mrp order from agent sale page
    def action_confirm(self):
        for rec in self:
            for add in rec.add_new_product:
                for line in rec.order_line:
                    if line.add_new_product_ids.id == add.id:
                        manufacturing_route = self.env.ref('mrp.route_warehouse0_manufacture')
                        mo = self.env['mrp.production'].search(
                            [('region_zones', '=', line.contact_name.id), ('state', '=', 'draft'),
                             ('product_id', '=', line.product_id.id), ('newspaper_date', '=', line.newspaper_date),
                             ('partner_id', '=', line.printing_unit.id), ('sale_order_id', '=', self.id)])
                        if mo:
                            # raise UserError("{} is in the draft state. Please confirm the order first.".format(mo.name))
                            qtys = mo.product_qty + line.product_uom_qty
                            mo.update({
                                'product_qty': qtys
                            })
                        elif line.product_id.type == 'product' and line.product_id.bom_ids and manufacturing_route in line.product_id.route_ids:
                            manufacturing_order = {
                                'product_id': line.product_id.id,
                                'region_zones': line.contact_name.id,
                                'product_qty': line.product_uom_qty,
                                'origin': self.name,
                                'picking_type_id': line.product_template_id.bom_ids.picking_type_id.id,
                                'sale_order_id': self.id,
                                'partner_id': line.printing_unit.id,
                                'order_qty': add.qty,  # newadd
                                'newspaper_date': line.newspaper_date,
                                'zone_page_details': [(line.contact_name.id)],
                            }
                            rec.env['mrp.production'].create(manufacturing_order)
        super(MrpConfirm, self).action_confirm()


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    active = fields.Boolean('Active', default=True, tracking=True)


class MrpPages(models.Model):
    _name = 'page.details'

    name = fields.Many2one('res.partner')
    no_page = fields.Integer('No of pages')
    m2o_id = fields.Many2one('mrp.production')
    m2o_district_id = fields.Many2one('mrp.production')
    m2o_zone_id = fields.Many2one('mrp.production')
