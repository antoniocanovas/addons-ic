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
    ocr_transaction_id = fields.Many2one('ocr.transactions')
    dictionary_id = fields.Many2one('ocr.dictionary')

    #@api.depends('name')
    #def _get_dictionary(self):
    #    data = self.env['ocr.dictionary'].search([('name', '=', self.name)])
    #    if data.id:
    #        self.dictionary_id = data.id

    #compute = _get_dictionary

