"""model for cleaning service"""

from odoo import models, fields
from datetime import datetime


class CleaningService(models.Model):
    """class for cleaning service model"""
    _name = "cleaning.service"
    _description = "This is a model For hostal cleaning"
    _rec_name = "clean_room"

    clean_room = fields.Many2one("room", string="Room",
                                 required=True)
    start_time = fields.Date(string="Start Time",
                             default=datetime.today())
    cleaning_staff_id = fields.Many2one("res.users",
                                        string="Cleaning Staff")
    cleaning_staff_id_count = fields.Integer("staff count",
                                             compute=
                                             "_compute_cleaning_staff_id")
    company_id = fields.Many2one("res.company",
                                 string="Company",
                                 default=lambda self: self.env.company)
    state = fields.Selection(string="state",
                             selection=[('new', 'New'),
                                        ('assigned', 'Assigned'),
                                        ('done', 'Done')],
                             default='new')

    def action_assign_cleaning_staff(self):
        """Method to assign current user as cleaning staff while
        clicking assigning button"""
        current_user = self.env.user
        self.write({'cleaning_staff_id': current_user})
        self.update({'state': 'assigned'})
        self.clean_room.update({'state': 'cleaning'})

    def action_complete(self):
        """method for changing the state to completed
        while clicking the button"""
        self.update({'state': 'done'})
        self.clean_room.update({'state': 'empty'})

    def _compute_cleaning_staff_id(self):
        """function to check wether the cleaning staff is assigned or not"""
        self.cleaning_staff_id_count = len(self.cleaning_staff_id)
