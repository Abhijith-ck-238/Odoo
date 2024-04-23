from odoo import models, api


class StudentReport(models.AbstractModel):
    """abstract class for student report"""
    _name = 'report.hostel_management.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        """method for passing student values as data"""
        docs = self.env['student'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'student',
            'docs': docs,
            'data': data,
        }
