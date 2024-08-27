# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<http://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'Web Design',
    'category': 'Website',
    "sequence": 3,
    'version': '1',
    'license': 'LGPL-3',
    'author': '',
    'website': '',
    'data': [
        'views/assets.xml',
        'views/snippets/example.xml',
        'views/snippets/homesectionform.xml',
        'views/snippets/landing_section_form.xml',
        'views/snippets/landing_section_slider.xml',
        'views/snippets/landing_section_targets.xml',
        'views/snippets/landing_section_methodology.xml',
        'views/snippets/landing_section_results.xml',
        'views/snippets/landing_section_requirements.xml',
        'views/snippets/landing_section_advantages.xml',
        'views/snippets/landing_section_postulate.xml',
    ],
    'images': [
        'static/description/web_openeducat_banner.jpg',
        'static/src/img/Landing_Portada_MBA.jpg',
        'static/src/img/small-logo.png',
        'static/src/img/snippets_icons/gerens_logo.png',
        'static/src/img/web_new/banner_slide_mbminero.jpg',
        'static/src/img/web_new/download-pdf-icon.png',
        'static/src/img/web_new/fondo-dirigido.png',
        'static/src/img/web_new/icon-dir-1.png',
        'static/src/img/web_new/icon-dir-2.png',
        'static/src/img/web_new/icon-dir-3.png',
        'static/src/img/web_new/icon-dir-4.png',
        'static/src/img/web_new/icon-rn-1.png',
        'static/src/img/web_new/icon-rn-2.png',
        'static/src/img/web_new/img-cr-1.png',
        'static/src/img/web_new/img-cr-2.png',
        'static/src/img/web_new/img-cr-3.png',
        'static/src/img/web_new/Landing_Portada_MBA.jpg',
        'static/src/img/web_new/rectangle-left.png',
        'static/src/img/web_new/rectangle-right.png',
        'static/src/img/web_new/slider-next-icon.png',
        'static/src/img/web_new/slider-prev-icon.png',
        'static/src/img/web_new/small-logo.png'
    ],
    'depends': [
        'website',
    ],
    'application': True,
    'assets': {
        'web.assets_frontend': [
            ## libs
            '/web_design/static/src/libs/bootstrap-grid.min.css',
            '/web_design/static/src/libs/bootstrap-reboot.min.css',
            #'/web_design/static/src/libs/jquery-3.7.1.min.js',
            '/web_design/static/src/libs/slick.min.css',
            '/web_design/static/src/libs/slick.min.js',

            ## module
            '/web_design/static/src/scss/main.scss',
            '/web_design/static/src/js/script.js'
        ],
    }
}
