from odoo import models, fields, api
from datetime import date


class SchoolDashboard(models.Model):
    _name = "school.dashboard"
    _description = "School Dashboard"

    date = fields.Date(string="Date", required=True, index=True)

    student_count = fields.Integer(
        string="Students", compute="_compute_counts", store=True
    )
    instructor_count = fields.Integer(
        string="Instructors", compute="_compute_counts", store=True
    )
    course_count = fields.Integer(
        string="Courses", compute="_compute_counts", store=True
    )

    @api.depends()
    def _compute_counts(self):
        for rec in self:
            rec.student_count = self.env["school.student"].search_count([])
            rec.instructor_count = self.env["school.instructor"].search_count([])
            rec.course_count = self.env["school.course"].search_count([])

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._compute_counts()
        return record

    def create_daily_record(self):
        """Create a daily record of counts."""
        self.create(
            {
                "date": date.today(),
            }
        )
