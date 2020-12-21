# -*- coding: utf-8 -*-

# Copyright 2020 Ingeniería Cloud - Pedro Baños
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': "Fleet Analitic Tag",
    'summary': """Añade a los vehículos la posibilidad de asignar una etiqueta analítica para visualizar los costes asignados por este modo.
""",
    'version': '12.0.0.1.0',
    'category': 'Other',
    'website': "https://ingenieriacloud.com",
    'author': "Ingenieriacloud",
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'account',
        'fleet',
       
    ],
    'data': [
        'views/fleet_vehicle_form_inh.xml',
    ],
}
