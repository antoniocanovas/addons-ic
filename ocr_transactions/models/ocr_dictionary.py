# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api


class OcrDictionary(models.Model):
    _name = 'ocr.dictionary'
    _description = 'Ocr Dictionary'

    res_model = fields.Char('Model')
    name = fields.Char('Label')
    res_field = fields.Char('Field')
    res_id = fields.Char('External ID')
    type = fields.Char('External ID')
