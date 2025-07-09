from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError
import requests

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student'
    _rec_name='user_id'

    user_id = fields.Many2one('res.users', string="User", required=True,ondelete='cascade')

    student_id = fields.Char(
        string='Student ID', default='New', readonly=True)
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')],
        string="Gender",
        required=True,
    )
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone', required=True)
    email = fields.Char(string='Email', required=True)

    student_group = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D')
    ])

    grade_year = fields.Selection([
        ('first', 'First Grade'),
        ('second', 'Second Grade'),
        ('third', 'Third Grade'),
        ('fourth', 'Fourth Grade'),
        ('graduated','Graduated')],
                                  
        string="Grade Year",default='first'
       
    )
    grade = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F')],
        string='Grade'
    )
    credit_hour = fields.Integer(string="Credit Hour")
    
    status=fields.Selection([
        ('success','Success'),
        ('fail','Fail')
    ],string="Status",compute="_compute_student_status",store=True)

    image = fields.Binary(string='Image', attachment=True)

    enrollemet_sheet = fields.One2many(
        'school.enrollment', 'student_id', string='Enrollment Sheet')
    attendence_sheet = fields.One2many(
        'school.attendance', 'student_id', string='Attendance Records')
    timetable_sheet = fields.Many2many(
        'school.timetable',
        string='Time Table',
        compute='_compute_timetable'
    )
    is_fail=fields.Boolean(default=False)

    @api.depends("grade_year", "student_group")
    def _compute_timetable(self):
        for rec in self:
            rec.timetable_sheet = self.env["school.timetable"].search([
                ("grade_year", "=", rec.grade_year),
                ("student_group", "=", rec.student_group),
            ])

    @api.model
    def create(self, vals):
        res = super(Student, self).create(vals)
        if res.student_id == 'New':
            res.student_id = self.env['ir.sequence'].next_by_code(
                'student_squence')
        return res
    @api.depends('grade')
    def _compute_student_status(self):
        for rec in self:
            if rec.grade == 'F':
                rec.status = 'fail'
            else:
                rec.status = 'success'

        
    def second_grade_action(self):
        for rec in self:
            if rec.grade_year=='first' and rec.grade in ('A','B','C','D'):
                rec.grade_year="second"
            else:
                raise UserError(f'{rec.user_id} Can Not Move Forward Next Level\n His/Her Grade is {rec.grade}')
    def third_grade_action(self):
        for rec in self:
            if rec.grade_year=='second' and rec.grade in ('A','B','C','D'):
                rec.grade_year="third"
            else:
                raise UserError(f'{rec.user_id} Can Not Move Forward Next Level\n His/Her Grade is {rec.grade}')
    def fourth_grade_action(self):
        for rec in self:
            if rec.grade_year=='third' and rec.grade in ('A','B','C','D'):
                 rec.grade_year="fourth"
            else:
                raise UserError(f'{rec.user_id} Can Not Move Forward Next Level\n His/Her Grade is {rec.grade}')
    def graduated_grade_action(self):
        for rec in self:
            if rec.grade_year=='fourth' and rec.grade in ('A','B','C','D'):
                 rec.grade_year="graduated"
            else:
                raise UserError(f'{rec.user_id} Can Not Move Forward Next Level\n His/Her Grade is {rec.grade}')

    
             
    def excel_report(self):
        return {
            'type':"ir.actions.act_url",
            'url':f'/student/report/excel/{self.env.context.get("active_ids")}',
            'target':'new'
        }
    def Check_Fail(self):
        """Check failed students and mark is_fail accordingly."""
        students = self.search([])
        for student in students:
            student.is_fail = (student.grade == 'F')
                
    def send_whatsapp_bulk(self):
        """Send WhatsApp messages to failing students."""
        fail_students = self.search([("status", "=", "fail")])
        if not fail_students:
            raise UserError("No failing students found.")

        phone_number_id = self.env["ir.config_parameter"].sudo().get_param("whatsapp.phone_number_id")
        token = self.env["ir.config_parameter"].sudo().get_param("whatsapp.token")
        if not phone_number_id or not token:
            raise UserError("Please configure 'whatsapp.phone_number_id' and 'whatsapp.token' in System Parameters.")

        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        for student in fail_students:
            if student.phone:
                payload = {
                    "messaging_product": "whatsapp",
                    "to": student.phone,
                    "type": "text",
                    "text": {
                        "body": f"Hello {student.user_id}, your current status is FAIL. Please contact the administration."
                    },
                }
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code != 200:
                    # لو حصل خطأ على رقم، يتم إظهاره
                    raise UserError(f"Error sending message to {student.user_id}: {response.content}")

        return True
    
