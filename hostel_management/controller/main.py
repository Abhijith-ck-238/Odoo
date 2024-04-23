
import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.http import serialize_exception as _serialize_exception
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    """XlsxReport generating controller"""

    @http.route('/xlsx_reports', type='http',
                auth='user',
                methods=['POST'],
                csrf=False)
    def get_report_xlsx(self, model, options, output_format):
        """
        Generate an XLSX report based on the provided data and return it as a
        response.
        """
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition',
                         content_disposition('Excel Report' + '.xlsx'))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))


class StudentRegistration(http.Controller):
    @http.route(['/registration'], type='http', auth='public',
                website=True)
    def service_request(self):
        """method to open url while clicking corresponding menu in website"""
        rooms = request.env['room'].search(
            [('state', 'not in', ["full", "cleaning"])])
        values = {
            'rooms': rooms,
        }
        return request.render("hostel_management.request_form",
                              values)

    @http.route(['/registration/create_student/'], type='http',
                auth="public", website=True)
    def student_creation(self, **kw):
        """method to create user if user with same email does not exist"""
        user_emails = request.env['res.users'].search([]).mapped('login')
        name = kw.get('name')
        email = kw.get('email')
        room = kw.get('room_id')
        dob = kw.get('dob')
        rooms = request.env['room'].search(
            [('state', 'not in', ["full", "cleaning"])])

        if email in user_emails:
            values = {
                'name': name,
                'rooms': rooms,
                'user_email_exist': True
            }
            return request.render("hostel_management.request_form",
                                  values)

        else:
            request.env['student'].create({
                'name': name,
                'email': email,
                'roomnum_id': room,
                'd_o_b': dob,

            })
            return request.render("hostel_management.thanks_form")

    @http.route(['/room'], type='http',
                auth="public", website=True)
    def room_menu(self):
        rooms = request.env['room'].search([], order='create_date desc',
                                           limit=4)
        values = {
            'rooms': rooms,
        }
        return request.render("hostel_management.room_form", values)

    @http.route('/room/<int:room>', type='http',
                auth="public", website=True)
    def show_room(self, room):
        room = request.env['room'].browse(room)
        values = {
            'room': room
        }
        return request.render("hostel_management.show_room", values)

    @http.route('/dynamic_rooms', type="json", auth="public")
    def room_dynamic(self):
        rooms = request.env['room'].search_read([])
        rooms_list = [rooms[i:i + 4] for i in range(0, len(rooms), 4)]
        return rooms_list

    @http.route('/shop/cart/clear_cart', type='json', auth="public",
                website=True)
    def clear_cart(self):
        order = request.website.sale_get_order()
        for line in order.order_line:
            line.unlink()
