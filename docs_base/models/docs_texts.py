# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class DocsTexts(models.Model):
    _name = 'docs.texts'
    _description = 'Docs Text bloqs'

    name = fields.Char(string='Name',required=True)
    type = fields.Selection(
        [('header', 'Header'), ('body', 'Body of message'), ('footer', 'Footer')], required=True,
        string='Type')
    text = fields.Html(string='Text')
    active = fields.Boolean('Active',default=True)
