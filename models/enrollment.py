from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class Enrollment(models.Model):
    _name = "school.enrollment"
    _description = "Enrollment"

    student_id = fields.Many2one(
        "school.student", string="Student", required=True, ondelete="cascade"
    )
    course_id = fields.Many2one(
        "school.course", string="Course", required=True, ondelete="cascade"
    )
    enrollment_date = fields.Date(
        string="Enrollment Date", default=fields.Date.context_today, required=True
    )
    status = fields.Selection(
        [("active", "Active"), ("completed", "Completed"), ("dropped", "Dropped")],
        string="Status",
        default="active",
        required=True,
    )

    @api.constrains("student_id", "course_id")
    def _check_credit_hour_limit(self):
        for rec in self:
            enrollments = self.env["school.enrollment"].search(
                [("student_id", "=", rec.student_id.id), ("status", "=", "active")]
            )

            total_hours = sum(e.course_id.credit_hour for e in enrollments)

            if total_hours > 18:
                raise ValidationError(
                    f"Student {rec.student_id.name} exceeds the maximum allowed credit hours (18). Total: {total_hours}"
                )

    @api.constrains("student_id", "course_id")
    def _check_duplicate_enrollment(self):
        for rec in self:
            duplicates = self.env["school.enrollment"].search(
                [
                    ("id", "!=", rec.id),
                    ("student_id", "=", rec.student_id.id),
                    ("course_id", "=", rec.course_id.id),
                    ("status", "=", "active"),
                ]
            )
            if duplicates:
                raise ValidationError(
                    f"Student {rec.student_id.name} is already enrolled in the course '{rec.course_id.name}'."
                )

    @api.model_create_multi
    def create(self, vals_list):
        enrollment = super().create(vals_list)

        if enrollment.student_id and enrollment.course_id:
            student = enrollment.student_id
            course = enrollment.course_id
            if student.credit_hour < course.credit_hour:
                raise ValidationError(
                    f"{student.name} does not have enough credit hours. Remaining: {student.credit_hour}, Required: {course.credit_hour}"
                )
            student.credit_hour -= course.credit_hour
            return enrollment

    def unlink(self):
        for rec in self:
            if rec.student_id and rec.course_id:
                rec.student_id.credit_hour += rec.course_id.credit_hour
        return super().unlink()
    def take_attendance(self):
        today = date.today()
        if today.weekday() == 4:  
            return 
        for rec in self:
            # Optional: Avoid duplicate entries for the same date
            exists = self.env['school.attendance'].search([
                ('student_id', '=', rec.student_id.id),
                ('course_id', '=', rec.course_id.id),
                ('attendance_date', '=', fields.Date.context_today(self)),
            ], limit=1)

            if not exists:
                self.env['school.attendance'].create({
                    'student_id': rec.student_id.id,
                    'course_id': rec.course_id.id,
                    'instructor_id': rec.course_id.instructor_id.id,  # assumes course has instructor
                    'attendance_date': fields.Date.context_today(self),
                    'status': 'present',
                })
