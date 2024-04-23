"""model inherited from invoice to add new field"""
from odoo import models, fields, api


class AccountMove(models.Model):
    """class of model inherited from invoice"""
    _inherit = 'account.move'

    student_id = fields.Many2one('student', string="Student")

    def send_email(self, record):
        """send invoice to students"""
        template = (self.env.
                    ref("hostel_management.student_invoice_email_template"))
        template.send_mail(record.id, force_send=True)

    def action_post(self):
        sup = super(AccountMove, self).action_post()
        for record in self:
            self.send_email(record)
        return sup
