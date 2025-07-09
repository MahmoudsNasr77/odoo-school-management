from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Attendance(models.Model):
    _name = "school.attendance"
    _description = "Attendance"

    student_id = fields.Many2one("school.student", string="Student", required=True)
    course_id = fields.Many2one("school.course", string="Course", required=True)
    instructor_id = fields.Many2one("school.instructor", string="Instructor", required=True)
    attendance_date = fields.Date(
        string="Attendance Date", 
        default=fields.Date.context_today, 
        required=True
    )
    status = fields.Selection(
        [("present", "Present"), ("absent", "Absent")],
        string="Status",
        default="present",
        required=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec.check_if_student_enrolled()
            rec.check_if_instructor_enrolled()
        return records

    def check_if_student_enrolled(self):
        for record in self:
            enrollments = self.env["school.enrollment"].search([
                ("student_id", "=", record.student_id.id),
                ("course_id", "=", record.course_id.id),
            ])
            if not enrollments:
                raise ValidationError("The student is not enrolled in this course.")

    def check_if_instructor_enrolled(self):
        for record in self:
            if record.course_id.id not in record.instructor_id.courses_list.ids:
                raise ValidationError("The instructor is not assigned to this course.")
