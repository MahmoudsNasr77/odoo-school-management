{
    'name': 'School Management System',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage school operations including students, teachers, and classes',
    'description': "",
    'depends': ['base', 'mail', 'web','auth_signup'],
    'author': 'Mahmoud Nasr',
    'data': [
        'security/groups.xml',
                'security/Enrollment_Secuirty.xml',

        'security/ir.model.access.csv',
        
        'data/sequence.xml',
        'data/email_templates.xml',

        'views/base.xml',
        'views/students_view.xml',
        'views/courses_view.xml',
        'views/instructor_view.xml',
        'views/enrollment_view.xml',
        'views/attendance_view.xml',
        'views/grade_view.xml',
        'views/timetable_view.xml',
        'views/auth_signup_inherit.xml',
        'views/login_inherit.xml',
        'reports/timetable.xml',
        'reports/student.xml',
        'reports/attendance.xml',
    ],

    'application': True,
    'installable': True,
}


