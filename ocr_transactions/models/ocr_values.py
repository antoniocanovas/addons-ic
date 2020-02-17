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

    @api.depends('name')
    def _get_dictionary(self):
        for record in self:
            data = self.env['ocr.dictionary'].search([
                ('name', '=', record.name),
                ('type', '=', record.ocr_transaction_id.type)
            ])
            if data.id:
                record.dictionary_id = data.id

    dictionary_id = fields.Many2one('ocr.dictionary', store="False", compute=_get_dictionary)
