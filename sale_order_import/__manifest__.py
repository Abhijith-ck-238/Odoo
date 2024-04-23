{
    'name': 'Sale_order_import',
    'version':'17.0.1.0.0',
    'depends':['sale_management'],
    'author':'ABD',
    'category':'Sales',
    'description':"This module contains add a button-'import lines' in sales module",
    'data':[
        'security/ir.model.access.csv',
        'wizard/file_wizard.xml',
        'views/sale_order_inherited.xml',
    ]
}