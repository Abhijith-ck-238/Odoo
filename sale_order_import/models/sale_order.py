"""model to create a button 'import lines' in the sales form view"""
from odoo import models


class SaleOrder(models.Model):
    """class ro inherit sale order"""
    _inherit = "sale.order"


    def action_sale_order_import_lines(self):
        """Action for adding products in the sale order line"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import product to order lines',
            'res_model': 'file.wizard',
            'view_mode': 'form',
            'target': 'new',
        }
