from odoo import models, fields,api
class Course(models.Model):
    _name = 'school.course'
    _description = 'Course'

    name = fields.Char(string='Course Name', required=True)
    course_code = fields.Char(string='Course Code',default='New', readonly=True,unique=True)
    description = fields.Text(string='Description')
    instructor_id = fields.Many2one('school.instructor', string='Instructor', required=True)
    
    enrollment_ids = fields.One2many('school.enrollment', 'course_id', string='Enrollments')
    
    @api.model
    def create(self, vals):
          res=super(Course, self).create(vals)
          if res.course_code =='New':
              res.course_code=self.env['ir.sequence'].next_by_code('course_squence')
          return res


