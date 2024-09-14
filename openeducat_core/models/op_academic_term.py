from odoo import models, fields


class OpAcademicTerm(models.Model):

    _name = 'op.academic.term'
    _description = "CicloAcademico"

    name = fields.Char('Nombre del Ciclo', required=True)
    term_start_date = fields.Date('Fecha de Inicio', required=True)
    term_end_date = fields.Date('Fecha de Fin', required=True)
    program_id = fields.Many2one(
        'op.program', 'Programa', required=True)
    parent_term = fields.Many2one('op.academic.term', 'Parent Term')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company)
