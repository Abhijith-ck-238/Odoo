from odoo import fields, models, api
from odoo.exceptions import UserError
import io
import json
import xlsxwriter
from odoo.tools import date_utils


class StudentWizard(models.TransientModel):
    """class for student report wizard"""
    _name = "student.report.wizard"
    _description = "wizard for printing student report"

    room_id = fields.Many2one("room",
                              string="Room",
                              )
    student_ids = fields.Many2many("student",
                                   string="Student"
                                   )
    students_ids = fields.Many2many("student",
                                    string="students_ids",
                                    compute="_compute_students_ids")

    @api.depends('room_id')
    def _compute_students_ids(self):
        for rec in self:
            rec.students_ids = rec.env['student'].search([])
            if rec.room_id:
                st = rec.room_id.students
                rec.students_ids = st

    def action_report(self):
        """method for creating query of our needs in pdf and print it"""
        query = """select s.name,s.pending_amount,r.number,s.invoice_status,s.id
                           from student as s
                           inner join room as r on r.id = s.roomnum_id
                           where True"""
        if self.room_id:
            query += (""" and r.number = '%s'""" % self.room_id.number)
        if self.student_ids:
            sid = tuple(self.student_ids.ids)
            if len(sid) == 1:
                query += (""" and s.id = %s""" % str(sid[0]))
            elif len(sid) != 0:
                query += (""" and s.id in %s""" % str(sid))
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        std = []
        s_count = 0
        rm = []
        r_count = 0
        for stud in report:
            student = stud['name']
            room = stud['number']
            if room not in rm:
                rm.append(room)
            if student not in std:
                std.append(student)
        if len(std) > 0:
            s_count = len(std)
            if len(rm) > 0:
                r_count = len(rm)
        data = {'report': report,
                's_count': s_count,
                'r_count': r_count}
        docids = self.student_ids.ids
        if len(data['report']) > 0:
            return (self.env.ref('hostel_management.action_student_report')
                    .report_action(docids, data))
        else:
            raise UserError("No data to Print")

    def action_student_xlsx_report(self):
        """method for creating query of our needs in pdf and print it"""
        query = """select s.name,s.pending_amount,r.number,s.invoice_status,s.id
                                   from student as s
                                   inner join room as r on r.id = s.roomnum_id
                                   where True"""
        if self.room_id:
            query += (""" and r.number = '%s'""" % self.room_id.number)
        if self.student_ids:
            sid = tuple(self.student_ids.ids)
            if len(sid) == 1:
                query += (""" and s.id = %s""" % str(sid[0]))
            elif len(sid) != 0:
                query += (""" and s.id in %s""" % str(sid))
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        std, rm = [], []
        for stud in report:
            room = stud['number']
            if room not in rm:
                rm.append(room)
        data = {'report': report,
                'room': rm,
                "company": self.env.user.company_id.name,
                "company_street": self.env.user.company_id.street,
                "company_state": self.env.user.company_id.state_id.name,
                "company_country": self.env.user.company_id.country_id.name,
                "company_zip": self.env.user.company_id.zip
                }
        if len(data.get('report', False)) > 0:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'student.report.wizard',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Student Excel Report',
                         },
                'report_type': 'xlsx',
            }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bg_color': 'ACA8A8',
             'border': 1})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px',
             'bg_color': '#F7F7F7', 'font_name': 'Times New Roman'})
        room_font = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True
             })
        heading_b = workbook.add_format(
            {'font_size': '10px', 'align': 'left', 'bold': True
             })
        txt = workbook.add_format(
            {'font_size': '10px', 'align': 'center', 'border': 1})
        sheet.merge_range('A5:D6', 'Student Report', head)
        sheet.set_column('A:D', 18)
        sheet.merge_range('A1:B1', f'{data.get("company")}',
                          heading_b)
        sheet.merge_range('A2:B2', f'{data.get("company_street")}', heading_b)
        sheet.merge_range('A3:B3',
                          f'{data.get("company_state")},'
                          f'{data.get("company_zip")}',
                          heading_b)
        sheet.merge_range('A4:B4', f'{data.get("company_country")}', heading_b)

        row = 8
        rooms = data.get('room', False)
        for room in rooms:
            row1, row2 = row, row + 2
            # Table heading
            sheet.write(f'A{row2}', 'SL.NO', cell_format)
            sheet.write(f'B{row2}', 'Name', cell_format)
            sheet.write(f'C{row2}', 'Pending Amount', cell_format)
            sheet.write(f'D{row2}', 'Invoice Status', cell_format)
            i = row2 + 1
            # student details
            serial_number = 1
            for rec in data.get('report', False):
                if rec.get('invoice_status', False) == 'pending':
                    status = 'Pending'
                else:
                    status = 'Done'
                if rec.get('number') == room:
                    sheet.merge_range(f'B{row1}:C{row1}', f'Room : {room}',
                                      room_font)
                    sheet.write(f'A{i}', serial_number, txt)
                    sheet.write(f'B{i}', rec.get('name', False), txt)
                    sheet.write(f'C{i}', rec.get('pending_amount', False),
                                txt)
                    sheet.write(f'D{i}', status,
                                txt)
                    serial_number += 1
                    i += 1
                    row = i + 2
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
