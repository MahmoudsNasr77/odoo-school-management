from odoo.http import request,Response
from odoo.http import Controller
from odoo import http
import json
class StudentApi(Controller):
    
    @http.route('/student/list', methods=['GET'], type='http', auth="none", csrf=False)
    def student_list(self):
        try:
            students = request.env['school.student'].search([])
            students_data = students.read(['student_id', 'user_id', 'email'])

            return Response(
                json.dumps({
                    'status': 'Success',
                    'data': students_data
                }),
                content_type='application/json',
                status=200
            )

        except Exception as error:
            return Response(
                json.dumps({
                    'status': 'Error',
                    'message': str(error)
                }),
                content_type='application/json',
                status=500
            )