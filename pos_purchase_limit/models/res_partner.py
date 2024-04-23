from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    purchase_limit = fields.Boolean(string="Purchase Limit")
    limit_amount = fields.Float("Limit Amount")
