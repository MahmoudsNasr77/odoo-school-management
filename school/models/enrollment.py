from odoo import models, fields, api
class Enrollment(models.Model):
    _name = 'school.enrollment'
    _description = 'Enrollment'

    student_id = fields.Many2one('school.student', string='Student', required=True)
    course_id = fields.Many2one('school.course', string='Course', required=True)
    enrollment_date = fields.Date(string='Enrollment Date', default=fields.Date.context_today, required=True)
    status = fields.Selection(
        [('active', 'Active'), ('completed', 'Completed'), ('dropped', 'Dropped')],
        string='Status',
        default='active',
        required=True
    )
    
