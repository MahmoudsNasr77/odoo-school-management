from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = "res.users"

    x_national_id = fields.Char(string="National ID", size=14)
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")
    phone = fields.Char(string="Phone")

    @api.model
    def create(self, values):
        user = super().create(values)

        gender = values.get("gender")
        phone = values.get("phone")
        email = values.get("email")

        if gender and phone:
            self.env["school.student"].create(
                {
                    "user_id": user.id,
                    "gender": gender,
                    "phone": phone,
                    "email": email,
                }
            )

        return user

    @api.constrains("x_national_id")
    def validate_x_national_id(self):
        for rec in self:
            if rec.x_national_id:
                if not rec.x_national_id.isdigit():
                    raise ValidationError("National ID must contain digits only.")
                if len(rec.x_national_id) != 14:
                    raise ValidationError("National ID must be exactly 14 digits.")
