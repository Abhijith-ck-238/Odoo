import base64
from odoo import models, Command


class StockReport(models.Model):
    """model for sending email to inventory manager,
    each day with stock report"""
    _name = "stock.report"

    def send_stock_report_email(self):
        invoice_report = self.env.ref('stock_report.action_stock_report')
        query = """select p.name,p.product_quantity,p.type,p.id
                                           from product_template as p
                                           where True 
                                           and p.type = 'product'"""
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()

        data = {
            'report': report
        }
        data_record = base64.b64encode(
            self.env['ir.actions.report'].sudo()._render_qweb_pdf(
                invoice_report, data=data)[0])
        ir_values = {
            'name': 'Stock Report pdf',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'stock.report',
        }
        stock_report_attachment_id = self.env[
            'ir.attachment'].sudo().create(
            ir_values)
        if stock_report_attachment_id:
            email_template = self.env.ref(
                'stock_report.stock_report_email_template')
            partner = self.env['hr.employee'].search(
                [('department_id.name', '=', 'Inventory Manager')])

            if partner.work_email:
                email = partner.work_email
            else:
                email = 'customer098765432@gmail.com'
            if email_template and email:
                email_values = {
                    'email_to': email,
                    'email_cc': False,
                    'scheduled_date': False,
                    'recipient_ids': [],
                    'partner_ids': [],
                    'auto_delete': True,
                }
                email_template.attachment_ids = [
                    (Command.link(stock_report_attachment_id.id))]
                email_template.with_context(partner=partner).send_mail(
                    False, email_values=email_values, force_send=True)
                email_template.attachment_ids = [
                    (Command.unlink(stock_report_attachment_id.id))]
