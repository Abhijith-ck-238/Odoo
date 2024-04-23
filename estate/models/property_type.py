from odoo import models,fields

class propertype(models.Model):
    _name = 'propertytype'
    _description = 'description of Property'

    name = fields.Char(string='Property Type')
