from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = "school.course"
    _description = "Course"

    name = fields.Char(string="Course Name", required=True)
    course_code = fields.Char(string="Course Code", default="New", readonly=True)
    description = fields.Text(string="Description")
    instructor_id = fields.Many2one(
        "school.instructor", string="Instructor", required=True
    )

    enrollment_ids = fields.One2many(
        "school.enrollment", "course_id", string="Enrollments"
    )
    credit_hour = fields.Integer(string="Credit Hour")
    max_capacity = fields.Integer(string="Max Capacity")
    active = fields.Boolean(string="Active", default=True)

    state = fields.Selection(
        [("new", "New"), ("confirmed", "Confirmed"), ("closed", "Closed")],
        default="new",
    )

    @api.model_create_multi
    def create(self, vals):
        res = super(Course, self).create(vals)
        if res.course_code == "New":
            res.course_code = self.env["ir.sequence"].next_by_code("course_squence")
        return res

    @api.constrains("credit_hour")
    def _check_credit_hour(self):
        for rec in self:
            if rec.credit_hour < 2 or rec.credit_hour > 4:
                raise ValidationError("Credit hour must be between 2 and 4.")

    @api.constrains("student_id", "course_id")
    def _check_course_capacity(self):
        for rec in self:
            if rec.course_id.max_capacity:
                enrollment_count = self.env["school.enrollment"].search_count(
                    [
                        ("course_id", "=", rec.course_id.id),
                        ("status", "=", "active"),
                    ]
                )
                if enrollment_count > rec.course_id.max_capacity:
                    raise ValidationError(
                        f"The course '{rec.course_id.name}' has reached its maximum capacity of {rec.course_id.max_capacity} students."
                    )

    @api.constrains("instructor_id")
    def check_max_number_of_courses(self):
        for rec in self:
            if rec.instructor_id and rec.instructor_id.max_number_of_course:
                courses_count = self.search_count(
                    [("instructor_id", "=", rec.instructor_id.id)]
                )
                if courses_count > rec.instructor_id.max_number_of_course:
                    raise ValidationError(
                        f"Instructor {rec.instructor_id.name} is assigned to {courses_count} courses, "
                        f"which exceeds the maximum allowed ({rec.instructor_id.max_number_of_course})."
                    )

    def new_course_action(self):
        for rec in self:
            rec.state = "new"

    def confirmed_course_action(self):
        for rec in self:
            rec.state = "confirmed"

    def closed_course_action(self):
        for rec in self:
            rec.state = "closed"

    def action_confirm_waizerd(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "school.course_change_state_wizard_action"
        )
        action["context"] = {
            "default_course_id": self.id,
            "default_state": self.state,
        }
        return action
