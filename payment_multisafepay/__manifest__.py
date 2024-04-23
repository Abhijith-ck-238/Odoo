{
    'name': 'multisafepay_payment',
    'version': '17.0.1.0.0',
    'depends': ['base', 'account', 'website_sale'],
    'author': 'ABD',
    'category': 'Human Resources',
    'description': "This module contains details multysafepay payment",
    'data': [

        'views/payment_provider.xml',
        'views/payment_multisafepay_templates.xml',

        'data/payment_method_data.xml',
        'data/payment_provider_data.xml',

    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3',
}
