from odoo import models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_bom_overview(self):
        """Shows the current BOM details"""
        bom = {
            'type': 'ir.actions.act_window',
            'name': 'BOM Overview',
            'view_mode': 'form',
            'res_model': 'mrp.bom',
            'res_id': self.bom_id.id,
        }
        return bom
