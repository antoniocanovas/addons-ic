from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoQuality(models.Model):
    _name = 'udo.quality'
    _description = 'UDO Quality '

    name = fields.Char(string='Quality')
