from odoo import http
from odoo.http import request

class StudentPortalController(http.Controller):
    
    @http.route('/my/final-grades', auth='user', website=True)
    def portal_final_grades(self, **kw):
        # Obtén el estudiante vinculado al usuario conectado
        student = request.env['op.student'].sudo().search([('user_id', '=', request.env.user.id)], limit=1)
        
        # Si no es un estudiante válido, mostrar un mensaje
        if not student:
            return request.render('openeducat_exam.no_student_found', {
                'message': 'No eres un estudiante registrado en el sistema.'
            })

        # Recuperar las notas finales del estudiante
        final_grades = request.env['op.final.grade'].sudo().search([('student_id', '=', student.id)])

        # Si no tiene notas, mostrar un mensaje
        if not final_grades:
            return request.render('openeducat_exam.no_grades_found', {
                'message': 'Aún no tienes notas disponibles.'
            })

        # Renderizar la plantilla con las notas del estudiante
        return request.render('openeducat_exam.portal_final_grades', {
            'student': student,
            'final_grades': final_grades
        })
