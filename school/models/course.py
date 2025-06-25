from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'school.course'
    _description = 'Course'

    name = fields.Char(string='Course Name', required=True)
    course_code = fields.Char(string='Course Code',
                              default='New', readonly=True, unique=True)
    description = fields.Text(string='Description')
    instructor_id = fields.Many2one(
        'school.instructor', string='Instructor', required=True,ondelete='cascade')

    enrollment_ids = fields.One2many(
        'school.enrollment', 'course_id', string='Enrollments',ondelete='cascade')
    credit_hour = fields.Integer(string="Credit Hour")
    max_capacity = fields.Integer(string="Max Capacity")

    @api.model
    def create(self, vals):
        res = super(Course, self).create(vals)
        if res.course_code == 'New':
            res.course_code = self.env['ir.sequence'].next_by_code(
                'course_squence')
        return res

    @api.constrains('credit_hour')
    def _check_credit_hour(self):
        for rec in self:
            if rec.credit_hour < 2 or rec.credit_hour > 4:
                raise ValidationError("Credit hour must be between 2 and 4.")
    @api.constrains('student_id', 'course_id')
    def _check_course_capacity(self):
        for rec in self:
            if rec.course_id.max_capacity:
                enrollment_count = self.env['school.enrollment'].search_count([
                    ('course_id', '=', rec.course_id.id),
                    ('status', '=', 'active'),
                ])
                if enrollment_count > rec.course_id.max_capacity:
                    raise ValidationError(f"The course '{rec.course_id.name}' has reached its maximum capacity of {rec.course_id.max_capacity} students.")
