{
    'name': 'pos_purchase_limit',
    'version': '17.0.1.0.0',
    'depends': ['point_of_sale'],
    'author': 'ABD',
    'description': 'user can set limit to customers and show pop up when limit exceeds',
    'data': [
        'views/res_partner_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_purchase_limit/static/src/js/purchase_limit.js',
        ],
    }
}
