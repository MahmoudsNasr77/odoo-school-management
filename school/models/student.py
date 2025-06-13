from odoo import models, fields, api
class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'
    user_id = fields.Many2one('res.users', string="User", required=True)


    name = fields.Char(string='Name', required=True,unique=True)
    student_id = fields.Char(string='Student ID', default='New', readonly=True,unique=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True)
    gender= fields.Selection(
        [('male','Male'),
         
         ('female','Female')],  
        string="Gender",
        required=True,
    )    
    address = fields.Text(string='Address', required=True)
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email', required=True)

    image= fields.Binary(string='Image', attachment=True)
    grade= fields.Selection(
        
        [
            ('A', 'A'),
         ('B', 'B'),
         ('C', 'C'),
         ('D', 'D'),
         ('F', 'F')],
        string='Grade',
        
    
    )
    enrollemet_sheet=fields.One2many('school.enrollment', 'student_id', string='Enrollment Sheet')
    attendence_sheet=fields.One2many('school.attendance', 'student_id', string='Attendance Records')

    @api.model
    def create(self, vals):
          res=super(Student, self).create(vals)
          if res.student_id =='New':
              res.student_id=self.env['ir.sequence'].next_by_code('student_squence')
          return res
              
              
              
