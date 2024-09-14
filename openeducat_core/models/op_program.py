from odoo import models, fields

class OpProgram(models.Model):
    _name = 'op.program'
    _description = "Programa GERENS"

    name = fields.Char('Nombre del Programa', required=True)
    start_date = fields.Date('Fecha de Inicio', required=True)
    end_date = fields.Date('Fecha de Fin', required=True)
    company_id = fields.Many2one('res.company', string='Compañía', default=lambda self: self.env.company)  # Campo agregado
    create_boolean = fields.Boolean(default=False)  # Campo agregado
    term_structure = fields.Selection([
        ('maestria_4_ciclos', 'Maestría - 4 Ciclos (2 años)'),
        ('capacitacion_1_ciclo', 'Capacitación (1 ciclo)'),
        ('otros', 'Otro (estructuras personalizadas)')
    ], string='Estructura del Programa', required=True)

    academic_term_ids = fields.One2many('op.academic.term', 'program_id', string='Ciclos Académicos')

    def term_create(self):
        academic_terms = self.env['op.academic.term']
        academic_terms.search([('program_id', '=', self.id)]).unlink()  # Eliminar ciclos previos

        if self.term_structure == 'maestria_4_ciclos':
            # Crear 4 términos vacíos para que el usuario asigne nombres y fechas manualmente
            for i in range(4):
                academic_terms.create({
                    'name': f'Ciclo {i + 1}',  # Nombres provisionales, se pueden cambiar manualmente
                    'program_id': self.id,
                })

        elif self.term_structure == 'capacitacion_1_ciclo':
            # Crear un solo ciclo para la capacitación
            academic_terms.create({
                'name': 'Capacitación',
                'program_id': self.id,
            })



