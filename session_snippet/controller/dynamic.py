from odoo import http
from odoo.http import request


class Event(http.Controller):
    @http.route('/get_total_sold', auth='public', type='json')
    def events(self):
        product = request.env('product.template').sudo().search_read([],
                                                                     ['name',
                                                                      'list_price'],
                                                                     limit=10)
        return product
