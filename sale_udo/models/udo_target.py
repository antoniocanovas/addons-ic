from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoTarget(models.Model):
    _name = 'udo.target'
    _description = 'UDO Target '

    name = fields.Char(string='Target', required=True)
