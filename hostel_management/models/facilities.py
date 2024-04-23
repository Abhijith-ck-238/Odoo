"""model of facilities"""
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Facilities(models.Model):
    """ class/table name of facilities model"""
    _name = "facilities"
    _description = "All Facilities are here"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Facility", required=True)
    company_id = fields.Many2one('res.company', store=True,
                                 copy=False, string="Company",
                                 default=lambda self:
                                 self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id')
    charge = fields.Monetary(string="Charge", required=True)

    @api.constrains('charge')
    def _check_charge(self):
        """function to check the charge is zero or negative"""
        if self.charge <= 0:
            raise ValidationError("Purchase price must be greater than 0.")
