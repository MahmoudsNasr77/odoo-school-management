# school/models/res_users_inherit.py
from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    # You might want to add these fields directly to res.users if they are globally applicable
    # or keep them only on school.student if they are specific to students.
    # For signup, it's often easier to temporarily store them on res.users during creation.
    # We will pass them to the student creation.

    @api.model
    def signup(self, values, token=None):
        # Call the original signup method first to create the res.users record
        new_user = super(ResUsers, self).signup(values, token)

        # Extract gender and phone from the signup values
        gender = values.get('gender')
        phone = values.get('phone')

        if gender and phone:
            # Create a new student record
            self.env['school.student'].create({
                'user_id': new_user.id,
                'gender': gender,
                'phone': phone,
                'email': new_user.email, # Assuming email is also available from signup
                # Add other default values for student here if needed
                # e.g., 'student_group': 'a', 'grade_year': 'first'
            })
        return new_user