from odoo import models,fields,api
from odoo.exceptions import ValidationError, UserError

class Grade(models.Model):
    _name = 'school.grade'
    _description = 'Grade'
    
    student_id = fields.Many2one('school.student', string='Student', required=True)
    course_id = fields.Many2one('school.course', string='Course', required=True)
    exam_type = fields.Selection([
        ('Monthly1', 'Monthly 1'),
        ('Monthly2', 'Monthly 2'),
        ('Monthly3', 'Monthly 3'),
        ('Monthly4', 'Monthly 4'),
        ('practical', 'Practical'),
        ('final', 'Final Exam')
    ], string='Exam Type', required=True)
    exam_grade = fields.Float(string= 'Exam Grade', compute='_compute_exam_grade', store=True,readonly=True)
    grade = fields.Float(string='Grade', required=True)  # ✅ أضف ده

    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    notes = fields.Text(string='Notes')
    _sql_constraints = [
        ('unique_student_course_exam', 'UNIQUE(student_id, course_id, exam_type)', 
         'A student can only have one grade per course and exam type.')
    ]
    @api.constrains('grade')
    def _check_grade_range(self):
        for record in self:
            if not (0 <= record.grade <= 100):
                raise ValidationError("Grade must be between 0 and 100.")    
    @api.constrains('date')
    def _check_date(self):
        for record in self:
            if record.date > fields.Date.context_today(self):
                raise ValidationError("Date cannot be in the future.")
    @api.constrains('student_id', 'course_id')
    def _check_student_enrollment(self):
        for record in self:
            enrolled_courses = record.student_id.enrollemet_sheet.mapped('course_id')
            if record.course_id not in enrolled_courses:
                raise ValidationError(
                    f"The student '{record.student_id.user_id.name}' is not enrolled in the course '{record.course_id.name}'."
                )

    @api.depends('exam_type')
    def _compute_exam_grade(self):
        for record in self:
            if record.exam_type == 'final':
                record.exam_grade = 50
            elif record.exam_type == 'practical':
                record.exam_grade = 30
            else:
                record.exam_grade = 20
