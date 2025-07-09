from odoo import http
from odoo.http import request,Response
import io
import xlsxwriter
from ast import literal_eval

class Student_Excel_Report(http.Controller):
    @http.route('/student/report/excel/<string:std_ids>',type='http',auth='user')
    def download_excel_student_report(self,std_ids):
        student_ids=request.env['school.student'].browse(literal_eval(std_ids))
        output=io.BytesIO()
        workbook=xlsxwriter.Workbook(output,{'in_memory':True})
        worksheet=workbook.add_worksheet('Student')
        header_format=workbook.add_format({'bold':True,'align':'center','bg_color':"#800080",'border':1,'font_color':'#FFFFFF'})
        string_format=workbook.add_format({'align':'center','border':1})

        header_format.set_indent(1)
        headers=['Student Id','Student Name','Student Gender','Student Phone','Student Group','Student Grade Year','Student Grade','Credit Hour']
        for col_num,header in enumerate(headers):
             worksheet.write(0,col_num,header,header_format)
        for row_num, std in enumerate(student_ids, start=1):
            worksheet.write(row_num, 0, str(std.student_id),string_format)
            worksheet.write(row_num, 1, std.name or '',string_format)
            worksheet.write(row_num, 2, std.gender or '',string_format)
            worksheet.write(row_num, 3, std.phone or '',string_format)
            worksheet.write(row_num, 4, std.student_group or '',string_format)
            worksheet.write(row_num, 5, std.grade_year or '',string_format)
            worksheet.write(row_num, 6, std.grade or '',string_format)
            worksheet.write(row_num, 7, str(std.credit_hour or ''),string_format)
        workbook.close()
        output.seek(0)
        
        file_name="Student Report.xlsx"
        
        return Response(
            output.getvalue(),
            headers=[
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition',f'attachment;filename={file_name}')
            ]
        )