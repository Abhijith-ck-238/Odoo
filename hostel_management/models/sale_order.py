from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_delete(self):
        if self.state != 'sale':
            self.unlink()
