""" model of room menu"""
from odoo import Command
from odoo import models, fields, api


class HostelRoom(models.Model):
    """ class for hostel room"""
    _name = "room"
    _description = "Room of this hostel"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "number"

    number = fields.Char(string="Room Number",
                         readonly=True,
                         tracking=True,
                         default="New",
                         index=True
                         )
    type = fields.Selection(required=True,
                            string="Room Type",
                            selection=[('non_ac', 'NON_AC'),
                                       ('ac', 'AC'),
                                       ('gold', 'GOLD')])
    image = fields.Image(string="Image")
    bedno = fields.Integer(string="Number of Beds",
                           default="1",
                           tracking=True)
    occupied_bedno = fields.Integer(string="occupied",
                                    readonly=True,
                                    store=True,
                                    compute="_compute_occupied_bedno")
    available_bed = fields.Integer(string="Available Beds",
                                   compute="_compute_available_bed",
                                   store=True)
    students = fields.One2many("student",
                               'roomnum_id',
                               string="Students")
    company_id = fields.Many2one('res.company',
                                 store=True,
                                 copy=False,
                                 string="Company",
                                 default=lambda self:
                                 self.env.user.company_id.id)

    currency_id = fields.Many2one('res.currency',
                                  string="Currency",
                                  related='company_id.currency_id',
                                  required=True)
    rent = fields.Float(string="Rent",
                        tracking=True)
    state = fields.Selection(string="State",
                             selection=[('empty', 'Empty'),
                                        ('partial', 'Partial'),
                                        ('full', 'Full'),
                                        ('cleaning', 'Cleaning')],
                             default="empty")
    facilities_ids = fields.Many2many('facilities',
                                      string="facility")
    pending_amount = fields.Float(string="Pending Amount",
                                  default=0,
                                  compute="_compute_pending_amount")
    total_rent = fields.Float(string="Total Rent",
                              compute="compute_total_rent")
    monthly_amount = fields.Integer(string="Monthly Amount",
                                    compute="_compute_monthly_amount",
                                    store=True)


    def create(self, vals):
        """ function to set automatic room number"""
        vals['number'] = self.env['ir.sequence'].next_by_code('hostel.room')
        return super(HostelRoom, self).create(vals)

    @api.depends('students')
    def _compute_occupied_bedno(self):
        """ function to count booked rooms and change state"""
        for record in self:
            record.occupied_bedno = len(record.students.ids)
            cleaning_service_count = (record.env
            ['cleaning.service'].search_count([
                ('clean_room', '=', record.number),
                ('state', 'not in', ['done'])
            ]))
            if cleaning_service_count != 0:
                record.update({'state': 'cleaning'})
            else:
                if record.occupied_bedno == 0:
                    record.update({'state': 'empty'})
                else:
                    pass
                if 0 < record.occupied_bedno < record.bedno:
                    record.update({'state': 'partial'})
                else:
                    pass
                if record.occupied_bedno >= record.bedno:
                    record.update({'state': 'full'})
                else:
                    pass

    def _compute_pending_amount(self):
        """method to calculate pending amount of all students in room"""
        # students = self.students.search([])
        room_total_pending = 0
        # print("students", students[1])
        # std1 = students[1]
        for student in self.students:
            invoices = self.env['account.move'].search([
                ('partner_id', '=', student.partner_id.id),
                ('payment_state', 'not in', ['paid']),
                ('move_type', '=', 'out_invoice')
            ])
            # invoices = student.invoice_ids.filtered(lambda x:
            # x.payment_state != 'paid')
            for invoice in invoices:
                total = invoice.amount_total_signed
                room_total_pending += total
        self.pending_amount = room_total_pending

    @api.depends('rent', 'facilities_ids')
    def compute_total_rent(self):
        for record in self:
            facilities_price = 0
            for facility in record.facilities_ids:
                facilities_price += facility.charge
            record.total_rent = record.rent + facilities_price

    def send_email(self, rec):
        """function to send invoice to students in the room"""
        template = self.env.ref("hostel_management.student_rent_email_template")
        template.send_mail(rec.id, force_send=True)

    def action_monthly_invoice(self):
        """function to create invoice for students in room"""
        students = self.students
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

    @api.depends('bedno','total_rent')
    def _compute_monthly_amount(self):
        for rec in self:
            rec.monthly_amount = rec.total_rent/rec.bedno

    @api.depends('occupied_bedno','bedno')
    def _compute_available_bed(self):
        for rec in self:
            rec.available_bed = rec.bedno- rec.occupied_bedno