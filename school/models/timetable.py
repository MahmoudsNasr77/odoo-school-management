from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class TimeTable(models.Model):
    _name = "school.timetable"
    _rec_name = "grade_year"

    course_id = fields.Many2one(
        'school.course', string="Course", required=True,ondelete='cascade')
    instructor_id = fields.Many2one(
        'school.instructor', string="Instructor", required=True,ondelete='cascade')

    years = fields.Char(size=4, string="Year Of TimeTable",default=2025)
    student_group = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D')
    ])

    academic_terms = fields.Selection(
        [
            ('fall', 'Fall'),
            ('winter', 'Winter'),
            ('spring', 'Spring'),
            ('summer', 'Summer'),
        ], string="Academic Term"
    )
    # The `grade_year` field in the `TimeTable` model is a selection field that allows the user to
    # choose the grade year associated with the timetable entry. It provides options such as 'First
    # Grade', 'Second Grade', 'Third Grade', and 'Fourth Grade'. This field is required, meaning that
    # the user must select a grade year when creating a new timetable entry.
    grade_year = fields.Selection(
        [
            ('first', 'First Grade'),
            ('second', 'Second Grade'),
            ('third', 'Third Grade'),
            ('fourth', 'Fourth Grade'),
        ],
        string="Grade Year",
        required=True
    )
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)

    room = fields.Char(string="Room")

    @api.constrains("start_time", "end_time")
    def validetime(self):
        for rec in self:
            if rec.end_time < rec.start_time:
                raise ValidationError(
                    "End Time Must Be Grater Than Start Time")
    @api.constrains('start_time', 'end_time', 'instructor_id', 'student_group', 'grade_year')
    def _check_no_overlap(self):
        for rec in self:
            overlaps = self.env['school.timetable'].search([
                ('id', '!=', rec.id),
                '|',
                ('instructor_id', '=', rec.instructor_id.id),
                '&',
                ('student_group', '=', rec.student_group),
                ('grade_year', '=', rec.grade_year),
            ])
            for other in overlaps:
                if (rec.start_time < other.end_time and rec.end_time > other.start_time):
                    raise ValidationError(f"Conflict: The timeslot {rec.start_time}-{rec.end_time} overlaps with an existing entry for the same instructor or student group.")
    @api.model
    def send_reminders_for_upcoming_classes(self):
            now = fields.Datetime.now()
            upcoming_classes = self.search([
                ('start_time', '>=', now),
                ('start_time', '<=', now + timedelta(hours=1))
            ])
            for cls in upcoming_classes:
                template = self.env.ref('school.email_template_upcoming_class')
                for enrollment in cls.course_id.enrollment_ids:
                    student_email = enrollment.student_id.email
                    if student_email:
                        template.sudo().with_context(email_to=student_email).send_mail(cls.id, force_send=True)