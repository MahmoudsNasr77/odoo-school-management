from odoo import models, fields, api
from odoo.exceptions import ValidationError
class Attendance(models.Model):
    _name = 'school.attendance'
    _description = 'Attendance'

    student_id = fields.Many2one('school.student', string='Student', required=True,ondelete='cascade')
    course_id = fields.Many2one('school.course', string='Course', required=True,ondelete='cascade')
    attendance_date = fields.Date(string='Attendance Date', default=fields.Date.context_today, required=True)
    status = fields.Selection(
        [('present', 'Present'), ('absent', 'Absent')],
        string='Status',
        default='present',
        required=True
    )
    
    @api.model
    def create(self, vals):
        res = super(Attendance, self).create(vals)
        if res.student_id and res.course_id:
            res.check_if_student_enrolled()
        return res
    
    def check_if_student_enrolled(self):
        for record in self:
            enrollments = self.env['school.enrollment'].search([
                ('student_id', '=', record.student_id.id),
                ('course_id', '=', record.course_id.id)
            ])
            if not enrollments:
                raise ValidationError("The student is not enrolled in this course.")


