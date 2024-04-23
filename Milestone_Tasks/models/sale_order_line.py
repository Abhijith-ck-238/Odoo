"""inherit sale order line and field in the sale order line """
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    milestone = fields.Integer(string="Mile stone")
