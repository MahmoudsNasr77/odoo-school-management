from odoo import http
from odoo.http import request
from ..utils.jwt_token import generate_token
import json
class JwtAuthController(http.Controller):
    
    
    
    @http.route('/api/login', type='json', auth='public', csrf=False)
    def login(self, **kw):
        
        try:
            data = json.loads(request.httprequest.data)

            login = str(data.get('login'))
            password = str(data.get('password'))
            uid = request.session.authenticate(request.db, login, password)
            if uid:
                return {'token': generate_token(uid, request.env)}
            return {'error': 'Invalid credentials'}
        except Exception as error:
            return str(error)
