# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import json
from datetime import datetime
import requests
from odoo.exceptions import ValidationError
from odoo import fields, models, api
from datetime import datetime


class Viafirma(models.Model):
    _inherit = 'viafirma'

    viafirma_doc_id = fields.Many2one('docs.docs')
