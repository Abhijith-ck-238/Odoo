{

    'name': 'Daily Attendance',
    'version': '17.0.1.0.0',
    'depends': ['hr_attendance'],
    'author': 'ABD',
    'description': 'This module shows the absentees list as tree view',
    'category': 'Human Resources',
    'application':True,
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_absentees.xml',
        'views/day_wise_attendance_views.xml',
        'views/day_wise_attendance_menu.xml',
    ]

}
