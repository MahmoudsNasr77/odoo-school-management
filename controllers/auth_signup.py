from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request
from odoo import http

class CustomSignup(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        # National ID and Gender
        national_id = kw.get('national_id')
        gender = kw.get('gender')

        response = super(CustomSignup, self).web_auth_signup(*args, **kw)

        user = request.env['res.users'].sudo().search([('login', '=', kw.get('login'))], limit=1)
        if user:
            user.x_national_id = national_id
            request.env['school.student'].sudo().create({
                'user_id': user.id,
                'gender': gender,
                'email': user.email,
                'phone': kw.get('phone'),
            })

        return response
