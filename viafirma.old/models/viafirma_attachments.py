# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api

class ViafirmaAttachments(models.Model):
    _name = 'viafirma.attachments'
    _description = 'Viafirma Attachments'

    viafirma_id = fields.Many2one(viafirma='attachment_id')
    viafirma_signed_id = fields.Many2one(viafirma='attachment_signed_id')

