from odoo import fields, models, api
from odoo.exceptions import UserError
import io
import json
import xlsxwriter
from odoo.tools import date_utils


class LeaveRequestReportWizard(models.TransientModel):
    """class for leave request report wizard"""
    _name = "leave.request.report.wizard"
    _description = "wizard for printing leave request"

    room_id = fields.Many2one("room",
                              string="Room")
    student_ids = fields.Many2many("leave.request",
                                   string="Student",
                                   )
    start_date = fields.Date("Start Date")
    arrival_date = fields.Date("Arrival Date")
    students_ids = fields.Many2many("leave.request",
                                    string="students_ids",
                                    compute="_compute_students_ids")

    @api.depends('room_id')
    def _compute_students_ids(self):
        for rec in self:
            rec.students_ids = rec.student_ids.search([])
            if rec.room_id:
                st = rec.room_id.students
                for req in st:
                    students_id = rec.room_id.students.ids
                    requests = (req.env['leave.request']
                                .search([('student.id', 'in', students_id)]))
                rec.students_ids = requests

    def action_leave_request_report(self):
        """method for creating query of our needs in pdf and print it"""
        query = """select s.name,r.number,lr.l_date,lr.a_date,lr.duration,s.id
                           from leave_request as lr
                           inner join student as s on s.id = lr.student
                           inner join room as r on r.id = s.roomnum_id
                           where True"""
        sid = tuple(self.student_ids.student.mapped('id'))
        if self.room_id:
            query += (""" and r.number = '%s'""" % self.room_id.number)
        if len(sid) == 1:
            # if student field has atleast 1 value
            query += (""" and s.id = %s""" % str(sid[0]))
        elif self.student_ids:
            query += (""" and s.id in %s""" % str(sid))
        if self.start_date:
            query += (""" and lr.l_date = '%s'""" % self.start_date)
        if self.arrival_date:
            query += (""" and lr.a_date =  '%s'""" % self.arrival_date)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        rooms = []
        for student in report:
            if student['number'] not in rooms:
                rooms.append(student['number'])
        data = {'report': report}
        docids = self.student_ids.ids
        if len(report) > 0:
            return (self.env.
                    ref('hostel_management.action_leave_request_record')
                    .report_action(docids, data))
        else:
            raise UserError("No data to Print")

    def action_leave_request_xlsx_report(self):
        """method for creating query of our needs in pdf and print it"""
        query = """select s.name,r.number,lr.l_date,lr.a_date,lr.duration,s.id
                                  from leave_request as lr
                                  inner join student as s on s.id = lr.student
                                  inner join room as r on r.id = s.roomnum_id
                                  where True"""
        sid = tuple(self.student_ids.student.ids)
        print(sid)
        if self.room_id:
            query += (""" and r.number = '%s'""" % self.room_id.number)
        if len(sid) == 1:
            query += (""" and s.id = %s""" % str(sid[0]))
        elif self.student_ids:
            query += (""" and s.id in %s""" % str(sid))
        if self.start_date:
            query += (""" and lr.l_date >= '%s'""" % self.start_date)
        if self.arrival_date:
            query += (""" and lr.a_date <=  '%s'""" % self.arrival_date)
        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        rooms = []
        for student in report:
            if student['number'] not in rooms:
                rooms.append(student['number'])
        data = {'report': report,
                "rooms": rooms,
                "company": self.env.user.company_id.name,
                "company_street": self.env.user.company_id.street,
                "company_state": self.env.user.company_id.state_id.name,
                "company_country": self.env.user.company_id.country_id.name,
                "company_zip": self.env.user.company_id.zip
                }
        if len(data.get('report', False)) > 0:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'leave.request.report.wizard',
                         'options': json.dumps(data,
                                               default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Leave Request Excel Report',
                         },
                'report_type': 'xlsx',
            }

        else:
            raise UserError("No data to Print")

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bg_color': 'ACA8A8'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px',
             'bg_color': '#F7F7F7', 'font_name': 'Times New Roman'})
        heading_b = workbook.add_format(
            {'font_size': '10px', 'align': 'left', 'bold': True
             })
        room_font = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True
             })
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('A5:E6', 'Leave Request Report', head)
        sheet.set_column('A:F', 18)
        student = data['report'][0]
        sheet.merge_range('A1:B1', f'{data.get("company")}',
                          heading_b)
        sheet.merge_range('A2:B2', f'{data.get("company_street")}', heading_b)
        sheet.merge_range('A3:B3',
                          f'{data.get("company_state")},{data.get("company_zip")}',
                          heading_b)
        sheet.merge_range('A4:B4', f'{data.get("company_country")}', heading_b)
        rooms = data.get("rooms", False)
        row = 10
        for room in rooms:
            row1, row2 = row, row + 2
            sheet.write(f'A{row2}', 'SL.NO', cell_format)
            sheet.write(f'B{row2}', 'Name', cell_format)
            sheet.write(f'C{row2}', 'Start date', cell_format)
            sheet.write(f'D{row2}', 'Arrival Date', cell_format)
            sheet.write(f'E{row2}', 'Duration', cell_format)

            i = row2 + 1

            serial_number = 1
            for student in data['report']:  # Start at row 16 for Students
                if student.get('number') == room:
                    sheet.merge_range(f'B{row1}:D{row1}', f'Room : {room}',
                                      room_font)
                    sheet.write(f'A{i}', serial_number, txt)
                    sheet.write(f'B{i}', student['name'], txt)
                    sheet.write(f'C{i}', student['l_date'], txt)
                    sheet.write(f'D{i}', student['a_date'], txt)
                    sheet.write(f'E{i}', student['duration'], txt)
                    serial_number += 1
                    i += 1
                    row = i + 2
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
