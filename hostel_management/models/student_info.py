"""model of student menu"""
from odoo import Command
from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class Student(models.Model):
    """class for student menu and fields"""
    _name = "student"
    _description = "contains Students information"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'base']

    name = fields.Char(string="Name",
                       required=True)
    active = fields.Boolean(default=True)
    sid = fields.Char(string="Student ID",
                      readonly=True,
                      index=True, default="ID")
    partner_id = fields.Many2one("res.partner",
                                 string="Partner",
                                 readonly=True)
    user_id = fields.Many2one("res.users",
                              string="user",
                              readonly=True)
    d_o_b = fields.Date(string="D.O.B")
    roomnum_id = fields.Many2one("room",
                                 string="Room",
                                 tracking=True,
                                 readonly=True)
    roomnum_id_count = fields.Integer("roomnumber count",
                                      compute="_compute_roomnum_id")
    company_id = fields.Many2one("res.company",
                                 string="Company",
                                 default=lambda self: self.env.company)
    age = fields.Integer(string="Age",
                         readonly=True,
                         compute="_compute_age",
                         store=True
                         )
    email = fields.Char(string="Email",
                        required=True)
    image = fields.Image(string="Image")
    receive_email = fields.Boolean(string="Receive Email")
    street = fields.Char(string="Street")
    street2 = fields.Char(string='street2')
    city = fields.Char(string='City')
    country_id = fields.Many2one('res.country',
                                 string="Country")
    state_id = fields.Many2one('res.country.state',
                               string="State",
                               store=True)
    monthly_amount = fields.Float("Monthly amount",
                                  compute="_compute_monthly_amount")
    invoice_status = fields.Selection(string="Invoice",
                                      selection=[('pending', 'Pending'),
                                                 ('done', 'Done')],
                                      default='done',
                                      compute='_compute_invoice_status',
                                      store=True
                                      )
    invoice_count = fields.Integer(readonly=True,
                                   compute='_compute_invoice_count')
    leave_request_ids = fields.One2many("leave.request",
                                        "student")
    pending_amount = fields.Float(string="Pending amount",
                                  compute="_compute_pending_amount",
                                  store=True)
    invoiced = fields.Boolean("invoiced")

    @api.model
    def create(self, values):
        """function to create sequence number for student id and  a partner
        record in contact module"""
        values['sid'] = self.env['ir.sequence'].next_by_code('student.info')
        student = super(Student, self).create(values)
        partner_values = {
            'name': student.name,
            'email': student.email,
            'street': student.street,
            'street2': student.street2,
            'city': student.city,
            'state_id': student.state_id.id,
            'country_id': student.country_id.id,
        }

        partner = self.env['res.partner'].create(partner_values)

        student.write({'partner_id': partner.id})

        return student

    @api.depends('d_o_b')
    def _compute_age(self):
        """Calculate AGE"""
        today = date.today()
        if self.d_o_b:
            self.age = today.year - self.d_o_b.year - (
                    (today.month, today.day) < (self.d_o_b.month,
                                                self.d_o_b.day))
            if self.age < 0:
                raise ValidationError('Age Must Be Positive')

    def _compute_roomnum_id(self):
        """count the length of roomnum_id to check if it is filled"""
        self.roomnum_id_count = len(self.roomnum_id)

    def action_alot_room(self):
        """allocate Rooms that are not full"""
        rooms = self.env['room'].search([])
        empty_room = []
        for room in rooms:
            if room.occupied_bedno < room.bedno:
                empty_room.append(room)
                self.update({'invoice_status': 'pending'})
        if len(empty_room) == 0:
            raise ValidationError("Rooms are booked")
        else:
            self.roomnum_id = empty_room[0]

    def action_vacate_student(self):
        """function to archive students while clicking vacate button"""
        for record in self:
            record.write({'active': False})
            room_count = self.env['student'].search_count(
                [('roomnum_id.id', '=', record.roomnum_id.id)])
            if room_count == 0:
                cleaning_request_values = {
                    'clean_room': record.roomnum_id.id
                }
                self.env['cleaning.service'].create(cleaning_request_values)
                self.roomnum_id.update({'state': 'cleaning'})
            record.roomnum_id.write({
                'students': [(fields.Command.unlink(record.id))]
            })

    def action_unarchive_student(self):
        """function to unarchice the archived student"""
        self.write({'active': True})

    def _compute_monthly_amount(self):
        """method to calculate monthly amount of room .The amount must be sum of
        room rent ,facilities and this sum must
         be divided by room's bed number"""
        for rec in self:
            rent = rec.roomnum_id.rent
            bed = rec.roomnum_id.bedno
            if bed != 0:
                facilities_price = 0
                for facility in rec.roomnum_id.facilities_ids:
                    facilities_price += facility.charge
                rec.monthly_amount = (rent + facilities_price) / bed
            else:
                rec.monthly_amount = 0

    def send_email(self, rec):
        """send invoice to students"""
        template = self.env.ref("hostel_management.student_rent_email_template")
        template.send_mail(rec.id, force_send=True)

    def invoice_creation(self):
        """function to create invoice for students"""
        students = self.search([('active', '=', True)])
        for rec in students:
            invoice = rec.env['account.move']
            invoice.create({
                'move_type': 'out_invoice',
                'partner_id': rec.partner_id.id,
                'student_id': rec.id,
                'invoice_line_ids': [
                    Command.create({
                        'product_id': rec.env.
                        ref('hostel_management.room_rent_product11').
                        product_variant_id.id,
                        'quantity': 1,
                        'tax_ids': False,
                        'price_unit': rec.monthly_amount
                    })
                ]
            })
            self.send_email(rec)
            if rec.invoiced:
                rec.write({
                    'invoiced': False
                })
            else:
                rec.write({
                    'invoiced': True
                })

    @api.depends('invoiced')
    def _compute_invoice_status(self):
        """method to change state in student form when all invoices are paid"""
        for rec in self:
            non_paid_invoices = rec.env['account.move'].search_count([
                ('payment_state', 'not in', ['paid']),
                ('move_type', '=', 'out_invoice'),
                ('partner_id', '=', rec.partner_id.id)
            ])
            if non_paid_invoices == 0:
                rec.update({'invoice_status': 'done'})
            else:
                rec.update({'invoice_status': 'pending'})

    def student_user_creation(self):
        """function in the automation rule for creation of user"""
        user_values = {
            'name': self.name,
            'login': self.email,
            'partner_id': self.partner_id.id
        }
        user = self.env['res.users'].create(user_values)
        self.write({'user_id': user.id})

    def _compute_invoice_count(self):
        """to get the count of the invoice"""
        for rec in self:
            invoice_count = rec.env['account.move'].search_count([
                ('move_type', '=', 'out_invoice'),
                ('partner_id', '=', rec.partner_id.id)
            ])
            rec.invoice_count = invoice_count
            if invoice_count == 0:
                rec.update({
                    'invoice_status': 'done',
                    'pending_amount': 0
                })

    def action_invoices(self):
        """ to get invoice smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('partner_id', '=', self.partner_id.id),
                       ('move_type', '=', 'out_invoice')],
            'context': {'create': False, 'default_move_type': 'out_invoice'}
        }

    def unlink(self):
        """delete the leave requests created for the student"""
        self.leave_request_ids.unlink()
        return super(Student, self).unlink()

    @api.depends('invoiced')
    def _compute_pending_amount(self):
        """calculate the total pending amount of students"""
        for rec in self:
            invoiced_amount = rec.env['account.move'].search([
                ('partner_id', '=', rec.partner_id.id),
                ('move_type', '=', 'out_invoice'),
                ('payment_state', 'not in', ['paid'])
            ]).mapped('amount_total_signed')
            rec.pending_amount = sum(invoiced_amount)
