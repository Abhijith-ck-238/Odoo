from odoo import models, api


class LeaveRequestReport(models.AbstractModel):
    """abstract class for leave request report"""
    _name = 'report.hostel_management.report_leave_request'

    @api.model
    def _get_report_values(self, docids, data=None):
        """method for passing leave request values as data"""
        docs = self.env['leave.request'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'leave.request',
            'docs': docs,
            'data': data,
        }
