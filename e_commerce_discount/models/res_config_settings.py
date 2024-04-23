# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo import Command



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    e_commerce_discount = fields.Integer(string="E-Commerce Discount")
    is_e_commerce_discount = fields.Boolean(string="Set E-commerce discount")
    is_e_commerce_discount_change = fields.Boolean(string="compute",
                                                   compute="compute_is_e_commerce_discount_change")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'ec.is_e_commerce_discount', self.is_e_commerce_discount
        )
        self.env['ir.config_parameter'].set_param(
            'ec.e_commerce_discount', self.e_commerce_discount
        )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            is_e_commerce_discount=params.get_param(
                'ec.is_e_commerce_discount'),
            e_commerce_discount=params.get_param('ec.e_commerce_discount')
        )
        return res

    def compute_is_e_commerce_discount_change(self):
        if self.is_e_commerce_discount:
            self.is_e_commerce_discount_change = True

            discount_program = self.env.ref(
                'e_commerce_discount.e_commerce_discount_promotion')
            id = discount_program.reward_ids.id
            discount_program.update({
                'active': True,
                'reward_ids': [(Command.update(id,{
                    'discount': self.e_commerce_discount,
                }))]
            })
        else:
            self.is_e_commerce_discount_change = False
            discount_program = self.env.ref(
                'e_commerce_discount.e_commerce_discount_promotion')
            discount_program.update({
                'active': False})
