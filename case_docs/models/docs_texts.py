# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class DocsTexts(models.Model):
    _name = 'docs.texts'
    _description = 'Docs bloques de textos'

    name = fields.Char(string='Nombre',required=True)
    type = fields.Selection(
        [('intro', 'Introducción'), ('body', 'Cuerpo del mensaje'), ('footer', 'Pié de página')], requierd=True,
        string='Tipo')
    text = fields.Html(string='Texto')
