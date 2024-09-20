from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class FinalGrade(models.Model):
    _name = "op.final.grade"
    _inherit = "mail.thread"
    _description = "Nota Final"

    student_id = fields.Many2one('op.student', string='Estudiante', required=True)
    subject_id = fields.Many2one('op.subject', string='Asignatura', required=True)
    final_score = fields.Float('Nota Final', compute='_compute_final_score', store=True)
    score = fields.Float(string='Puntuación', help="Puntuación obtenida en el examen")
    
    @api.depends('subject_id.exam_ids.result_ids.score')
    def _compute_final_score(self):
        for record in self:
            total_weighted_score = 0.0
            total_weight = 0.0
            for exam in record.subject_id.exam_ids:
                result = self.env['op.exam.result'].search([('exam_id', '=', exam.id), ('student_id', '=', record.student_id.id)], limit=1)
                if result:
                    total_weighted_score += result.score * (exam.weight / 100)
                    total_weight += exam.weight

            record.final_score = total_weighted_score if total_weight > 0 else 0.0
