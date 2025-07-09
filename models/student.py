from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging
from datetime import date


_logger = logging.getLogger(__name__)


class Student(models.Model):
    _name = "school.student"
    _description = "Student"
    _rec_name = "user_id"

    user_id = fields.Many2one(
        "res.partner", string="User", required=True, ondelete="cascade"
    )
    student_id = fields.Char(string="Student ID", default="New", readonly=True)
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")],
        string="Gender",
        required=True,
    )
    address = fields.Text(string="Address")
    phone = fields.Char(string="Parent Phone", required=True)
    email = fields.Char(string="Email")

    student_group = fields.Selection([("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")])

    grade_year = fields.Selection(
        [
            ("first", "First Grade"),
            ("second", "Second Grade"),
            ("third", "Third Grade"),
            ("fourth", "Fourth Grade"),
            ("graduated", "Graduated"),
        ],
        string="Grade Year",
        default="first",
    )
    grade = fields.Selection(
        [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("F", "F")], string="Grade",compute="_compute_student_grade", store=True,readonly=True
    )


    credit_hour = fields.Integer(string="Credit Hour")

    status = fields.Selection(
        [("success", "Success"), ("fail", "Fail")],
        string="Status",
        compute="_compute_student_status",
        store=True,
    )

    image = fields.Binary(string="Image", attachment=True)

    enrollemet_sheet = fields.One2many(
        "school.enrollment", "student_id", string="Enrollment Sheet"
    )
    attendence_sheet = fields.One2many(
        "school.attendance", "student_id", string="Attendance Records"
    )
    timetable_sheet = fields.Many2many(
        "school.timetable", string="Time Table", compute="_compute_timetable"
    )
    is_fail = fields.Boolean(default=False)
    final_results = fields.Text(string="Courses Grades", compute="_compute_final_results")
    grade_ids = fields.One2many('school.grade', 'student_id', string='Grades')

    _sql_constraints = [
        (
            "user_id_uniq",
            "unique(user_id)",
            "Each user can be linked to only one student.",
        ),
    ]

    @api.constrains("user_id")
    def check_user_id_unique(self):
        for rec in self:
            if self.search_count([("user_id", "=", rec.user_id.id)]) > 1:
                raise ValidationError("Each user can be linked to only one student.")
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth > fields.Date.context_today(self):
                raise ValueError("date of birth cannot be in the future.")

    @api.depends("grade_year", "student_group")
    def _compute_timetable(self):
        for rec in self:
            rec.timetable_sheet = self.env["school.timetable"].search(
                [
                    ("grade_year", "=", rec.grade_year),
                    ("student_group", "=", rec.student_group),
                ]
            )

    @api.model_create_multi
    def create(self, vals):
        res = super(Student, self).create(vals)
        if res.student_id == "New":
            res.student_id = self.env["ir.sequence"].next_by_code("student_squence")
        return res

    @api.depends("grade")
    def _compute_student_status(self):
        for rec in self:
            if rec.grade == "F":
                rec.status = "fail"
            else:
                rec.status = "success"

    @api.onchange("grade")
    def onChange_grade(self):
        for rec in self:
            if rec.grade == "F":
                rec.status = "fail"
            else:
                rec.status = "success"

    def second_grade_action(self):
        for rec in self:
            if rec.grade_year == "first" and rec.grade in ("A", "B", "C", "D"):
                rec.grade_year = "second"
            else:
                raise UserError(
                    f"{rec.user_id} Can Not Move Forward Next Level\n His/Her Grade is {rec.grade}"
                )

    def third_grade_action(self):
        for rec in self:
            if rec.grade_year == "second" and rec.grade in ("A", "B", "C", "D"):
                rec.grade_year = "third"
            else:
                raise UserError(
                    f"{rec.user_id} Can Not Move Forward Next Level\n His/Her Grade is {rec.grade}"
                )

    def fourth_grade_action(self):
        for rec in self:
            if rec.grade_year == "third" and rec.grade in ("A", "B", "C", "D"):
                rec.grade_year = "fourth"
            else:
                raise UserError(
                    f"{rec.user_id} Can Not Move Forward Next Level\n His/Her Grade is {rec.grade}"
                )

    def graduated_grade_action(self):
        for rec in self:
            if rec.grade_year == "fourth" and rec.grade in ("A", "B", "C", "D"):
                rec.grade_year = "graduated"
            else:
                raise UserError(
                    f"{rec.user_id} Can Not Move Forward Next Level\n His/Her Grade is {rec.grade}"
                )

    def excel_report(self):
        return {
            "type": "ir.actions.act_url",
            "url": f'/student/report/excel/{self.env.context.get("active_ids")}',
            "target": "new",
        }

    def Check_Fail(self):
        students = self.search([])
        for student in students:
            student.is_fail = student.grade == "F"
            
    def take_attendance(self):
        today = date.today()
        if today.weekday() == 4:  
            return  
        for student in self:
            for timetable in student.timetable_sheet:
                self.env['school.attendance'].create({
                    'student_id': student.id,
                    'course_id': timetable.course_id.id,
                    'instructor_id': timetable.instructor_id.id,
                    'status': 'present',
                })
    

    @api.depends('grade_ids.grade')
    def _compute_final_results(self):
        for student in self:
            results = []
            grades = student.grade_ids  
            for course in grades.mapped('course_id'):
                course_grades = grades.filtered(lambda g: g.course_id == course)
                total = sum(course_grades.mapped('grade'))
                results.append(f"{course.name}: {total}")
            student.final_results = "\n".join(results)

    @api.depends("grade_ids.grade")
    def _compute_student_grade(self):
        for student in self:
            grades = student.grade_ids.mapped("grade")

            if grades:
                avg = sum(grades) /len(student.enrollemet_sheet)
                print(f"{student.user_id.name} => Average: {avg}")
                if avg >= 90:
                    student.grade = "A"
                elif avg >= 80:
                    student.grade = "B"
                elif avg >= 70:
                    student.grade = "C"
                elif avg >= 60:
                    student.grade = "D"
                else:
                    student.grade = "F"
            else:
                student.grade = "F"


        
