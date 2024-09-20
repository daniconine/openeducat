import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpExam(models.Model):
    _name = "op.exam"
    _inherit = "mail.thread"
    _description = "Exámenes de Asignaturas"


    name = fields.Char('Examen', required=True)
    subject_id = fields.Many2one('op.subject', 'Asignatura', required=True)
    exam_code = fields.Char('Exam Code', size=16)
    exam_date = fields.Date('Fecha del Examen')
    responsible_id = fields.Many2many('op.faculty', string='Responsible')
    active = fields.Boolean(default=True)
    weight = fields.Float('Ponderación', required=True, help="Porcentaje que representa el examen en la nota final")
    result_ids = fields.One2many('op.exam.result', 'exam_id', string='Resultados')
    # Relación con el tipo de examen
    exam_type_id = fields.Many2one('op.exam.type', string='Tipo de Examen', required=True)

    _sql_constraints = [
        ('unique_exam_code',
         'unique(exam_code)', 'Code should be unique per exam!')]

    @api.constrains('weight')
    def _check_weight(self):
        for exam in self:
            if exam.weight <= 0.0 or exam.weight > 100.0:
                raise ValidationError(_("La ponderación debe estar entre 1 y 100."))

            
class OpExamResult(models.Model):
    _name = "op.exam.result"
    _description = "Resultados de Exámenes"

    student_id = fields.Many2one('op.student', string='Estudiante', required=True)
    exam_id = fields.Many2one('op.exam', string='Examen', required=True)
    score = fields.Float('Puntaje Obtenido')
    
    @api.constrains('score')
    def _check_score(self):
        for result in self:
            if result.score < 0 or result.score > 20:
                raise ValidationError(_("Resultado debe ser entre 0 y 20"))


      
class OpSubject(models.Model):
    _inherit = "op.subject"  # Heredamos la clase existente

    exam_ids = fields.One2many('op.exam', 'subject_id', string='Exámenes')  # Relación con exámenes

    
