# 🎓 Odoo School Management

A comprehensive Odoo 17 module for managing students, instructors, courses, and academic timetables.
Supports enrollment, grading, automated status updates, and more.

⚡ Features
✅ Student Management

Student Registration and Profile

Credit Hour Tracking

Status (Success/Fail) based on Final Grade

Automated Status Update (Failing students)

✅ Course Management

Course Registration and Capacity Constraints

Credit Hour Validation (2–4 hours)

✅ Instructor Management

Instructor Registration, Salary Computation

Email and Phone Number Constraints

✅ Enrollment & Attendance

Student Enrollment, Dropping Courses

Attendance Tracking (Present/Absent)

✅ Grades Management

Final Grade Computation (A–F)

GPA Computation across Courses

Custom Grade Reports

✅ Time Table

Conflict Validation for overlapping schedules (Student/Instructor)

Tree, Form & Calendar Views

Session Times and Rooms

Student Group and Grade Year Segmentation

✅ Automations (Cron Jobs)

Daily Student Status Update

Weekly Reports Sent to Admin

Reminder Email for Instructors 1h Before Class

🛠️ Technical Details
Framework: Odoo 17

Models:

school.student

school.instructor

school.course

school.enrollment

school.grade

school.attendance

school.timetable

Features:

Computed fields

Constraints & Validations

Sequences

Smart Buttons

Scheduled Actions

Custom Reports

REST-style Methods

Email Templates

QWeb & Excel Export

🚀 Getting Started
## ⚡️ Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/MahmoudsNasr77/odoo-school-management.git
    ```

2. Move the cloned directory to your Odoo `addons` path.

3. Restart your Odoo server and **update the app list**.

4. Install the **School Management** module from the Apps menu.
   
⚙️ Usage
Install the school_management app.

Configure courses, students, and instructors.

Create timetables and enroll students.

Let automated jobs and constraints do the rest!


👥 Author
Mahmoud Nasr
GitHub


