# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class OpFaculty(models.Model):
    _name = "op.faculty"
    _description = "Docente"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}
    _parent_name = False
    
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    first_name = fields.Char('Primer nombre', translate=True, required=True)
    middle_name = fields.Char('Segundo Nombre', size=128)
    apellido_paterno = fields.Char("Apellido Paterno",size=128,required=True)
    apellido_materno = fields.Char("Apellido Materno",size=128)
    #last_name = fields.Char('Apellidos', size=128, required=True)
    birth_date = fields.Date('Fecha Nacimiento')
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
        ('male', 'Male'),
        ('female', 'Female')
    ], 'Genero')
    nationality = fields.Many2one('res.country', 'Nacionalidad')
    emergency_contact = fields.Many2one(
        'res.partner', 'Contacto de Emergencia')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('N de Identificacion', size=64)
    login = fields.Char(
        'Login', related='partner_id.user_id.login', readonly=1)
    last_login = fields.Datetime('Latest Connection', readonly=1,
                                 related='partner_id.user_id.login_date')
    faculty_subject_ids = fields.Many2many('op.subject', string='Asignaturas',
                                           tracking=True)
    emp_id = fields.Many2one('hr.employee', 'HR Employee')
    main_department_id = fields.Many2one(
        'op.department', 'Deparatamento Principal',
        default=lambda self:
        self.env.user.dept_id and self.env.user.dept_id.id or False)
    allowed_department_ids = fields.Many2many(
        'op.department', string='Departamentos Permitidos',
        default=lambda self:
        self.env.user.department_ids and self.env.user.department_ids.ids or False)
    active = fields.Boolean(default=True)
    
    nivel_academic = fields.Selection([
        ('Grado', 'Grado'),
        ('Magister', 'Magister'),
        ('Doctorado', 'Doctorado'),
        
    ], string='Nivel Académico')

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "La fecha de nacimiento no puede ser la misma actual!"))

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

            
    def create_employee(self):
        for record in self:
            vals = {
                'name': record.name,
                'country_id': record.nationality.id,
                'gender': record.gender,
                'address_home_id': record.partner_id.id
            }
            emp_id = self.env['hr.employee'].create(vals)
            record.write({'emp_id': emp_id.id})
            record.partner_id.write({'partner_share': True, 'employee': True})

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Plantilla para importar Docente'),
            'template': '/openeducat_core/static/xls/op_faculty.xls'
        }]
