# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class DocsTypes(models.Model):
    _name = 'docs.types'
    _description = 'Tipos de plantillas para docs'

    name = fields.Char(string='Nombre plantilla',required=True)
    intro_id=fields.Many2one('docs.texts',string='Intro',domain=[('type','=','intro')])
    body_id = fields.Many2one('docs.texts', string='Body',domain=[('type','=','body')])
    footer_id = fields.Many2one('docs.texts', string='Footer',domain=[('type','=','footer')])
    active = fields.Boolean('Activo',default=True)

    @api.depends('intro_id','intro_id.text')
    def get_intro(self):
        for record in self:
            record['intro_text'] = record.intro_id.text

    intro_text = fields.Html(string='Intro', compute=get_intro)

    @api.depends('body_id','body_id.text')
    def get_body(self):
        for record in self:
            record['body_text'] = record.body_id.text

    body_text = fields.Html(string='Body', compute=get_body)

    @api.depends('footer_id','footer_id.text')
    def get_footer(self):
        for record in self:
            record['footer_text'] = record.footer_id.text

    footer_text = fields.Html(string='footer', compute=get_footer)