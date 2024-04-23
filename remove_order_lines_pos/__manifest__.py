{
    'name': 'remove_order_lines_pos',
    'version': '17.0.1.0.0',
    'depends': ['point_of_sale'],
    'author': 'ABD',
    'description': 'Add button to clear cart in pos and add button in each order lines',
    'assets': {
        'point_of_sale._assets_pos': [
            'remove_order_lines_pos/static/src/xml/clear_Cart.xml',
            'remove_order_lines_pos/static/src/xml/clear_order_line.xml',
            'remove_order_lines_pos/static/src/js/clear_order_line.js',
            'remove_order_lines_pos/static/src/js/clear_cart.js',
        ],
    },
}
