from odoo import models, fields


class AgentType(models.Model):
    _name = 'agent.type'

    name = fields.Char('Name')
