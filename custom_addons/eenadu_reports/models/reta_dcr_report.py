from datetime import datetime

from odoo import models, fields, tools,api


class RetaDCRReport(models.Model):
    _name = 'reta.dcr.report'
    _auto = False

    id = fields.Id()
    rcp_no = fields.Char('RCP No')
    ro_cio_no = fields.Char('RO/CIO No')
    ref = fields.Many2one('sale.order', string='Ref')
    pu_name = fields.Char('Publication')
    no_of_lines = fields.Integer('SIZE')
    amount_total = fields.Float('RATE')
    agent_commission_amount = fields.Float('CAMM')
    final_amount = fields.Float('NETAMT')
    cio_paid_amount = fields.Float('COLLAMT')
    # payment_info = fields.Text('Payment Information')
    payment_mode = fields.Char('Mode')
    payee_mobile = fields.Char('Mobile')
    payment_amount = fields.Float('Amount')
    payment_datetime = fields.Datetime('Datetime')
    date = fields.Date('Date')


    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW reta_dcr_report AS
            (
                SELECT
                    row_number() OVER () AS id,
                    pd.name as pu_name,
                    so.custom_classified_cio_seq as rcp_no,
                    so.custom_sale_seq as ro_cio_no, 
                    so.id AS ref,
                    sol.product_uom_qty as no_of_lines,
                    so.amount_total,
                    (so.amount_total*rp.agent_commission/100) as agent_commission_amount,
                    so.amount_total - (so.amount_total*rp.agent_commission/100) as final_amount,
                    so.cio_paid_amount,
					UPPER(pi.payment_mode) as payment_mode,
					pi.payee_mobile,
					pi.payment_amount,
					pi.payment_datetime,
					pi.payment_datetime::timestamp::date as date
                FROM
                    sale_order so, payment_informations pi, 
					publication_details pd, sale_order_line sol, res_partner rp
                    WHERE so.id = pi.payment_information_id
                    AND so.publication_id = pd.id
					AND sol.order_id = so.id
					AND rp.id = so.agent_name
                );
            """)
