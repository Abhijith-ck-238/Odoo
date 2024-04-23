from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_quantity = fields.Integer('quantity',
                                      compute="_compute_product_quantity",
                                      store=True)

    @api.depends('qty_available')
    def _compute_product_quantity(self):
        for product in self:
            product.product_quantity = product.qty_available



