# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api


class OcrValues(models.Model):
    _name = 'ocr.values'
    _description = 'Ocr Values'

    token = fields.Char('Token')
    name = fields.Char('Name')
    value = fields.Char('Value')
    ocr_transaction_id = fields.Many2one('ocr.transaction')
