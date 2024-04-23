from odoo import models, api


class StockReport(models.AbstractModel):
    """abstract class for student report"""
    _name = 'report.stock_report.stock_report_template'

    @api.model
    def _get_report_values(self, docids=None, data=None):
        """method for passing student values as data"""
        docs = self.env['product.template'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'data': data,
            'docs': docs,
        }
