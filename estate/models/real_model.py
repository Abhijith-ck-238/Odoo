from odoo import models,fields

class RealModel(models.Model):
    _name = "real"
    _description = "This is the description of  real_estate"



    name = fields.Char(string="Estate Name", required=True)
    p_name = fields.Many2one("propertytype",string="Property type")
    owner = fields.Many2one("res.partner", string="Partner")
    description = fields.Char(string="Desc")
    postcode = fields.Char(string="Postal code")
    date_availability = fields.Date(string="Available From",copy=False)
    expected_price = fields.Float(string="Expected price")
    selling_price = fields.Float(string="Selling price",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default="2")
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer(string="Fecades")
    active = fields.Boolean(string="Active",default=True)
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(string="Garden Orientation",selection=[('north','North'),('south','South'),('east','East'),('west','West')])
    state = fields.Selection(string="State",selection=[('new','New'),('offer_received','Offer_received'),('sold','Sold'),('cancel','Cancel')])

