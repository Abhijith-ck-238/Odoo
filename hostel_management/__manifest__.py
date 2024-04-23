{
    'name': 'Hostel_management',
    'version': '17.0.1.0.0',
    'depends': ['base', 'product', 'mail', 'contacts', 'account',
                'sale_management', 'website'],
    'author': 'ABD',
    'category': 'Human Resources',
    'description': "This module contains all of our Hostel details",
    'data': [
        'security/hostel_management_security.xml',
        'security/ir.model.access.csv',

        'report/student_report_template.xml',
        'report/hostel_management_report.xml',
        'report/leave_request_report_template.xml',
        'report/leave_request_report.xml',

        'data/room_service_product.xml',
        'data/room_sequence.xml',
        'data/student_id_sequence.xml',
        'data/facilities_data.xml',
        'data/student_automatic_invoice.xml',
        'data/student_email_template.xml',
        'data/automatic_user_creation.xml',
        'data/student_invoice_email.xml',

        'wizard/student_report_wizard.xml',
        'wizard/leave_request_report_wizard.xml',

        'views/room_views.xml',
        'views/student_views.xml',
        'views/facilities_view.xml',
        'views/leave_request_view.xml',
        'views/cleaning_service_views.xml',
        'views/hostel_menu.xml',
        'views/invoice_inherited.xml',
        'views/website_hostel_management_menu_action.xml',

        'views/website_student_thanks.xml',
        'views/website_student_registration.xml',
        'views/website_room.xml',
        'views/website_show_room.xml',
        'views/snippets/snippet.xml',
        'views/website_cart_inherit_button.xml'
    ],
    'assets': {
        "web.assets_backend": [
            'hostel_management/static/src/js/action_manager.js',
        ],
        "web.assets_frontend": [
            'hostel_management/static/src/js/snippet.js',
            'hostel_management/static/xml/website_room_dynamic.xml',
        ]
    }
}
