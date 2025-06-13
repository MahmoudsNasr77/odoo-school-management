from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Grade(models.Model):
    _name = 'school.grade'
    _description = 'Grade'

    student_id = fields.Many2one('school.student', string='Student', required=True)
    course_id = fields.Many2one('school.course', string='Course', required=True)
    exam_type = fields.Selection(
        [('midterm', 'Midterm'), ('final', 'Final'), ('quiz', 'Quiz')],
        string='Exam Type',
        required=True,
        default='midterm'
    )
    grade = fields.Float(string='Grade', required=True)
    date_recorded = fields.Date(string='Date Recorded', default=fields.Date.context_today, required=True)
    final_grade = fields.Char(
        string='Final Grade',
        compute='_compute_final_grade',
        store=True
    )


    @api.constrains('grade')
    def _check_grade_range(self):
        for record in self:
            if not (0 <= record.grade <= 100):
                raise ValidationError("Grade must be between 0 and 100.")

    @api.depends('grade')
    def _compute_final_grade(self):
        for record in self:
            if record.grade >= 90:
                record.final_grade = 'A'
            elif record.grade >= 80:
                record.final_grade = 'B'
            elif record.grade >= 70:
                record.final_grade = 'C'
            elif record.grade >= 60:
                record.final_grade = 'D'
            else:
                record.final_grade = 'F'
    @api.model
    def create(self, vals):
        res = super(Grade, self).create(vals)
        if res.student_id and res.course_id:
            res.check_if_student_enrolled()
        return res
    def check_if_student_enrolled(self):
        for record in self:
            enrollments = self.env['school.enrollment'].search([
                ('student_id', '=', record.student_id.id),
                ('course_id', '=', record.course_id.id)
            ])
            if not enrollments:
                raise ValidationError("The student is not enrolled in this course.")
