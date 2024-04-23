{
    'name': 'Pos_Show_Owner',
    'version': '17.0.1.0.0',
    'depends': ['point_of_sale'],
    'author': 'ABD',
    'description': 'This module will shows the owner name in the pos orderline',
    'data': [
        'views/inherit_product.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_show_owner/static/xml/inherit_pos.xml',
            'pos_show_owner/static/src/js/pos_owner.js'
        ],
    },

}
