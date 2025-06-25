# school/controllers/main.py
from odoo import http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.http import request

class CustomAuthSignupHome(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        # Call the original method to handle signup logic
        response = super(CustomAuthSignupHome, self).web_auth_signup(*args, **kw)

       
        response.location = 'http://nasr:8069/web'
        return response
