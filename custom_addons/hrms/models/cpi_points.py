from odoo import models, fields, _, api


class CPIPoints(models.Model):
    _name = 'cpi.points'

    cpi_point_lines = fields.One2many('cpi.points.line','cpi_point_many')
    sequence = fields.Char()


class CpiPointsLine(models.Model):
    _name = 'cpi.points.line'

    cpi_point_many = fields.Many2one('cpi.points')
    effective_date_from = fields.Date(string='Effective Date From')
    effective_date_to = fields.Date(string='Effective Date To')
    cpi_points_payroll = fields.Float(string='CPI Points')