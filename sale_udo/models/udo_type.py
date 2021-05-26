from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoType(models.Model):
    _name = 'udo.type'
    _description = 'UDO Type '

    name = fields.Char(string='Type')
