from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import requests
import base64
import json
import logging
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    api_key = fields.Char(
        string='Api Key',
    )
    api_domain = fields.Char(
        default='http://biyectiva.com:5000',
        string='Api Url'
    )