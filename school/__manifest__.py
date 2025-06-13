
{
    'name': 'School Management System',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage school operations including students, teachers, and classes',
    'description': "",
    'depends': ['base','mail','web'],
    'author': 'Mahmoud Nasr',
    'data':[
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base.xml',
        'views/students_view.xml',
        'views/courses_view.xml',
        'views/instructor_view.xml',
        'views/enrollment_view.xml',
        'views/attendance_view.xml',
        'views/grade_view.xml',
        
    ]
    ,
    'application': True,
    'installable': True,
}