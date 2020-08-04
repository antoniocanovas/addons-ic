import base64

from odoo import fields, models, api


import logging

_logger = logging.getLogger(__name__)


class CaritasResPartner(models.Model):
    _inherit = 'res.partner'

    fead_id = fields.Boolean('Fead')
    faga_id = fields.Boolean('Faga')
    azagra_id = fields.Boolean('Azagra')
    zona_pastoral_id = fields.Many2one('caritas.zona','Zona Pastoral')



