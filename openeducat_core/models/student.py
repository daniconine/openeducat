# -*- coding: utf-8 -*-
###############################################################################
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpStudentCourse(models.Model):
    _name = "op.student.course"
    _description = "Detalle de Asignaturas"
    _inherit = "mail.thread"
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', 'Student',
                                 ondelete="cascade", tracking=True)
    course_id = fields.Many2one('op.course', 'Programa', required=True, tracking=True)
    batch_id = fields.Many2one('op.batch', 'Batch', required=True, tracking=True)
    roll_number = fields.Char('Roll Number', tracking=True)
    subject_ids = fields.Many2many('op.subject', string='Cursos/Asignaturas')
    #program_id = fields.Many2one('op.program', 'Programa')  # Cambiado de academic_years_id a program_id
    #academic_term_id = fields.Many2one('op.academic.term', 'Terms')
    state = fields.Selection([('running', 'Running'),
                              ('finished', 'Finished')],
                             string="Status", default="running")
    
    mode=fields.Selection([('presencial','Presencial'),
                              ('virtual', 'Virtual'),
                              ('hibrido', 'Hibrido')],
                             string="Modalidad", default="presencial")
    type_roll=fields.Selection([('regular', 'Regular'),
                              ('especial', 'Especial')],
                             string="Tipo Matricula", default="regular")

    _sql_constraints = [
        ('unique_name_roll_number_id',
         'unique(roll_number,course_id,batch_id,student_id)',
         'Roll Number & Student must be unique per Batch!'),
        ('unique_name_roll_number_course_id',
         'unique(roll_number,course_id,batch_id)',
         'Roll Number must be unique per Batch!'),
        ('unique_name_roll_number_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Student Course Details'),
            'template': '/openeducat_core/static/xls/op_student_course.xls'
        }]


class OpStudent(models.Model):
    _name = "op.student"
    _description = "Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}

    first_name = fields.Char('Primer nombre', translate=True, required=True)
    middle_name = fields.Char('Segundo Nombre', size=128)
    apellido_paterno = fields.Char("Apellido Paterno",size=128,required=True)
    apellido_materno = fields.Char("Apellido Materno",size=128)
    birth_date = fields.Date('Fec Nacimiento')
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Grupo Sanguineo')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Genero', required=True, default='m')
    nationality = fields.Many2one('res.country', 'Nacionalidad')
    emergency_contact = fields.Many2one('res.partner', 'Contacto emergencia')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    gr_no = fields.Char("GR Number", size=20)
    category_id = fields.Many2one('op.category', 'Category')
    course_detail_ids = fields.One2many('op.student.course', 'student_id',
                                        'Detalle Programa',
                                        tracking=True)
    active = fields.Boolean(default=True)

    subject_ids = fields.Many2many(
        'op.subject',
        string='Asignaturas',
        compute='_compute_subject_ids',
        help='Asignaturas en las que está inscrito el estudiante'
    )


    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'GR Number must be unique per student!'
    )]

    #se cambio el sigueitne decorador
    @api.onchange('first_name', 'middle_name', 'apellido_paterno', 'apellido_materno')
    def _onchange_name(self):
        # Inicializamos la lista 'parts' con los campos que no son False y los convertimos en cadenas
        parts = [str(self.first_name or ''),  # Aseguramos que first_name siempre sea una cadena
                str(self.middle_name or ''),  # Si está vacío, asignamos una cadena vacía
                str(self.apellido_paterno or ''),
                str(self.apellido_materno or '')]

        # Filtramos cualquier campo vacío para que no se añadan espacios innecesarios
        parts = [part for part in parts if part]

        # Unimos las partes en una cadena con espacios y asignamos a self.name
        self.name = " ".join(parts)

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/openeducat_core/static/xls/op_student.xls'
        }]

    def create_student_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'is_student': True,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id

    #funcion que busca las asiganturas en que esta el estudiante
    def _compute_subject_ids(self):
        for student in self:
            courses = self.env['op.student.course'].search([('student_id', '=', student.id)])
            student.subject_ids = [(6, 0, courses.mapped('subject_ids').ids)]