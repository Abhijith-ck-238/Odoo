{
    'name': 'Range slider field widget',
    'version': '17.0.1.0.0',
    'author': 'ABD',
    'depends':['sale_management'],
    'category': 'Human Resources',
    'description': "This module contains range slider widget",
    'data': [
        'views/sale_order.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'range_slider_field_widget/static/src/css/range_slider_widget.css',
            'range_slider_field_widget/static/src/xml/range_slider_widget.xml',
            'range_slider_field_widget/static/src/js/range_slider_widget.js',

        ],

    },
}
