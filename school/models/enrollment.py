from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Enrollment(models.Model):
    _name = 'school.enrollment'
    _description = 'Enrollment'

    student_id = fields.Many2one(
        'school.student', string='Student', required=True,ondelete='cascade')
    course_id = fields.Many2one(
        'school.course', string='Course', required=True,ondelete='cascade')
    enrollment_date = fields.Date(
        string='Enrollment Date', default=fields.Date.context_today, required=True)
    status = fields.Selection(
        [('active', 'Active'), ('completed', 'Completed'), ('dropped', 'Dropped')],
        string='Status',
        default='active',
        required=True
    )

    @api.constrains('student_id', 'course_id')
    def _check_credit_hour_limit(self):
        for rec in self:
            # كل الكورسات اللي الطالب مشترك فيها وحالتها active
            enrollments = self.env['school.enrollment'].search([
                ('student_id', '=', rec.student_id.id),
                ('status', '=', 'active')
            ])

            total_hours = sum(e.course_id.credit_hour for e in enrollments)

            if total_hours > 18:
                raise ValidationError(
                    f"Student {rec.student_id.name} exceeds the maximum allowed credit hours (18). Total: {total_hours}"
                )

    @api.constrains('student_id', 'course_id')
    def _check_duplicate_enrollment(self):
        for rec in self:
            duplicates = self.env['school.enrollment'].search([
                ('id', '!=', rec.id),
                ('student_id', '=', rec.student_id.id),
                ('course_id', '=', rec.course_id.id),
                # لو عايز تمنع التكرار في الكورسات النشطة فقط
                ('status', '=', 'active'),
            ])
            if duplicates:
                raise ValidationError(
                    f"Student {rec.student_id.name} is already enrolled in the course '{rec.course_id.name}'."
                )

    @api.model
    def create(self, vals_list):
        enrollment = super().create(vals_list)
        self.env['school.attendance'].create(
            {
                'student_id':vals_list['student_id'],
                'course_id':vals_list['course_id']
                
                }
        )
        self.env['school.grade'].create(
            {
                'student_id':vals_list['student_id'],
                'course_id':vals_list['course_id'],
                'grade':0
                
                }
        )
   
        if enrollment.student_id and enrollment.course_id:
            student = enrollment.student_id
            course = enrollment.course_id
            if student.credit_hour < course.credit_hour:
                raise ValidationError(
                    f"{student.name} does not have enough credit hours. Remaining: {student.credit_hour}, Required: {course.credit_hour}")
            student.credit_hour -= course.credit_hour
            return enrollment

    def unlink(self):
        for rec in self:
            if rec.student_id and rec.course_id:
                rec.student_id.credit_hour += rec.course_id.credit_hour
        return super().unlink()
