from odoo import models, fields, api, _


class OpSubject(models.Model):
    _name = "op.subject"
    _inherit = "mail.thread"
    _description = "Curso/Asignatura"

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=256, required=True)
    grade_weightage = fields.Float('N° Creditos') #reutilizacion de campo
    type = fields.Selection(
        [('theory', 'Theory'), ('practical', 'Practical'),
         ('both', 'Both'), ('other', 'Other')],
        'Type', default="theory", required=True)
    subject_type = fields.Selection(
        [('compulsory', 'Obligatorio'), ('elective', 'Electivo')],
        'Tipo Curso', default="compulsory", required=True)
    department_id = fields.Many2one(
        'op.department', 'Department',
        default=lambda self:
        self.env.user.dept_id and self.env.user.dept_id.id or False)
    active = fields.Boolean(default=True)
    
    cycle = fields.Selection([
        ('0', 'Unico Ciclo'),
        ('1', 'Ciclo 1'),
        ('2', 'Ciclo 2'),
        ('3', 'Ciclo 3'),
        ('4', 'Ciclo 4')
    ], string='Ciclo')
    faculty_ids = fields.Many2many('op.faculty', string='Docentes') #para añadir en vista
    
    
    _sql_constraints = [
        ('unique_subject_code',
         'unique(code)', 'Code should be unique per subject!'),
    ]

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Subjects'),
            'template': '/openeducat_core/static/xls/op_subject.xls'
        }]
