from odoo import fields, models


class NapSequenceTracker(models.Model):
    _name = 'nap.sequence.tracker'

    partner_id = fields.Many2one('res.partner', string='Agent')
    sequence_number = fields.Integer(string='Current Sequence Number')
    source = fields.Selection([('reta', 'RETA'), ('nap', 'NAP'),])


