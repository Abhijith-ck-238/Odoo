"""inherit pos and add my field th the fields of pos"""
from odoo import models, api


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'] += ['owner_id']
        return result

