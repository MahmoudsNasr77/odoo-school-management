from odoo import models, fields


class CourseWeizerd(models.TransientModel):
    _name = "course.weizerd"

    course_id = fields.Many2one("course_id", "school.course", ondelete="cascade")
    state = fields.Selection(
        [("new", "New"), ("confirmed", "Confirmed"), ("closed", "Closed")],
        default="new",
    )

    reason = fields.Text(string="Reasons For Open")
    date = fields.Datetime(string="Date When Open")

    def action_confirm(self):
        self.course_id.state = self.state
