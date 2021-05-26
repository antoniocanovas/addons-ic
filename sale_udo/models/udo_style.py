from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoStyle(models.Model):
    _name = 'udo.style'
    _description = 'UDO Style '

    name = fields.Char(string='Style')
