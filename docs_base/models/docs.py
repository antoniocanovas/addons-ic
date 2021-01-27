# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class Docs(models.Model):
    _name = 'docs.docs'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Docs for Expedients'

    name = fields.Char(string="Name")
    type_id = fields.Many2one('docs.types',string='Type',store=True)
    is_public = fields.Boolean('Es público')


    @api.depends('type_id')
    def _get_intro_text(self):
        for record in self:
            record['header'] = record.type_id.header_id.text

    header = fields.Html(string='Header',compute=_get_intro_text,readonly=False, store=True)

    @api.depends('type_id')
    def _get_footer_text(self):
        for record in self:
            record['footer'] = record.type_id.footer_id.text

    footer = fields.Html(string='Footer', compute=_get_footer_text, readonly=False, store=True)

    @api.depends('type_id')
    def _get_body_text(self):
        for record in self:
            record['body'] = record.type_id.body_id.text

    body = fields.Html(string='Body', compute=_get_body_text, readonly=False, store=True)
