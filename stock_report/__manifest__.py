{

    'name': 'Stock Report',
    'version': '17.0.1.0.0',
    'depends': ['sale'],
    'author': 'ABD',
    'description': 'This module will send the stock report to the inventory manager each day',
    'category': 'Inventory',
    'application': True,
    'data': [

        'report/stock_report_template.xml',
        'report/stock_report_report.xml',

        'views/product_template.xml',

        'data/stock_report_email_template.xml',
        'data/ir_cron.xml',
    ]

}
