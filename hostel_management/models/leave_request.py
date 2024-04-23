from odoo import models, fields, api
from datetime import datetime, timedelta


class LeaveRequest(models.Model):
    """class for model leaverequest"""
    _name = "leave.request"
    _description = "model cntains leave requests"
    _rec_name = "student"

    student = fields.Many2one("student",
                              string="student",
                              required=True)
    l_date = fields.Date(string="Leave date",
                         required=True,
                         default=datetime.today(),
                         )
    a_date = fields.Date(string="Arrival Date",
                         required=True,
                         default=datetime.today() + timedelta(1)
                         )
    company_id = fields.Many2one("res.company",
                                 string="Company",
                                 default=lambda self: self.env.company)
    status = fields.Selection(string="state",
                              selection=[('new', 'New'),
                                         ('approved', 'Approved')],
                              default="new")
    duration = fields.Char("Duration",
                           compute="_compute_duration",
                           store=True)
    room_id = fields.Many2one("room", "Room",
                              related="student.roomnum_id")

    def action_approve(self):
        """funtion for approve button"""
        self.student.write({'active': False})
        for record in self:
            record.status = "approved"
            room_count = self.env['student'].search_count(
                [('roomnum_id.id', '=', record.student.roomnum_id.id)])
            if room_count == 0:
                cleaning_request_values = {
                    'clean_room': record.student.roomnum_id.id
                }
                self.env['cleaning.service'].create(cleaning_request_values)
                self.student.roomnum_id.update({'state': 'cleaning'})

    def action_cancel(self):
        """function for cancel button"""
        for record in self:
            record.status = "new"
            self.student.write({'active': True})

    @api.depends("l_date", "a_date")
    def _compute_duration(self):
        """compute the duration of leave"""
        ld = datetime.strptime(str(self.l_date), '%Y-%m-%d')
        ad = datetime.strptime(str(self.a_date), '%Y-%m-%d')
        dr = (ad - ld).days
        self.duration = str(dr)
