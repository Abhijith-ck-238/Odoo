{
    'name': "Real_estate",
    'version': '17.0.1.0.0',
    'depends': ['base'],
    'author': "Author Name",
    'category': 'category',
    'application': True,
    'description': """
    Contains all features of real estate    
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_views.xml',
        'views/estate_menus.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [

    ],
}