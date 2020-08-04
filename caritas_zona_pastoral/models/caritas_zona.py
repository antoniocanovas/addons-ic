import base64

from odoo import fields, models, api


import logging

_logger = logging.getLogger(__name__)


class CaritasZona(models.Model):
    _name = 'caritas.zona'
    _description = 'Zonas Pastorales'

    name = fields.Char('Name')




