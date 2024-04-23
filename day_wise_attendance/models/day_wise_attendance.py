"""model for view of absentees"""
from odoo import models, fields


class DayWiseAttendance(models.Model):
    _name = "day.wise.attendance"
    _description = "Model for daily Attendance"
    _rec_name = "employee_id"

    employee_id = fields.Many2one("hr.employee", string="Employee")
    ab_date = fields.Date(string="Date")

    def absentees_creation(self):
        """method for creating records of absent employee"""
        present = self.env['hr.attendance'].search([
            ('check_in', '<=', fields.date.today()),
            ('check_out', '>=', fields.date.today())
        ]).mapped('employee_id.id')
        absentees = self.env['hr.employee'].search([
            ('id', 'not in', present)
        ])
        for employee in absentees:
            self.env['day.wise.attendance'].create({
                'employee_id': employee.id,
                'ab_date': fields.date.today()
            })
