from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class Instructor(models.Model):
    _name = 'school.instructor'
    _description = 'Instructor'

    name = fields.Char(string='Name', required=True)
    instructor_id = fields.Char(
        string='Instructor ID', 
        default='New', 
        readonly=True, 
        copy=False
    )
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email', required=True)
    address = fields.Text(string='Address', required=True)
    image = fields.Binary(string='Image', attachment=True)
    courses_list = fields.One2many('school.course', 'instructor_id', string='Courses List')
    working_hours = fields.Float(string='Working Hours', required=True, default=0.0)
    salary = fields.Float(string='Salary', compute='_compute_salary', store=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name must be unique!'),
        ('unique_phone', 'UNIQUE(phone)', 'Phone must be unique!'),
        ('unique_email', 'UNIQUE(email)', 'Email must be unique!'),
        ('positive_working_hours', 'CHECK(working_hours >= 0)', 'Working hours must be non-negative!'),
    ]

    @api.model
    def create(self, vals):
        if vals.get('instructor_id', 'New') == 'New':
            vals['instructor_id'] = self.env['ir.sequence'].next_by_code('instructor_squence') or 'New'
        return super().create(vals)

    @api.onchange('working_hours')
    def _onchange_working_hours(self):
        if self.working_hours < 0:
            return {
                'warning': {
                    'title': "Invalid Working Hours",
                    'message': "Working hours cannot be negative.",
                }
            }

    @api.constrains('working_hours')
    def _check_working_hours(self):
        for rec in self:
            if rec.working_hours < 0:
                raise ValidationError("Working hours must be non-negative.")

    @api.depends('working_hours')
    def _compute_salary(self):
        for instructor in self:
            instructor.salary = instructor.working_hours * 100  # Assuming fixed rate
