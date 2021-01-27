# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class DocsTypes(models.Model):
    _name = 'docs.types'
    _description = 'Docs Types od documents'

    name = fields.Char(string='Name',required=True)
    header_id=fields.Many2one('docs.texts',string='Header',domain=[('type','=','header')])
    body_id = fields.Many2one('docs.texts', string='Body',domain=[('type','=','body')])
    footer_id = fields.Many2one('docs.texts', string='Footer',domain=[('type','=','footer')])
    active = fields.Boolean('Active',default=True)

    @api.depends('header_id','header_id.text')
    def get_intro(self):
        for record in self:
            record['header_text'] = record.header_id.text

    header_text = fields.Html(string='Header', compute=get_intro)

    @api.depends('body_id','body_id.text')
    def get_body(self):
        for record in self:
            record['body_text'] = record.body_id.text

    body_text = fields.Html(string='Body', compute=get_body)

    @api.depends('footer_id','footer_id.text')
    def get_footer(self):
        for record in self:
            record['footer_text'] = record.footer_id.text

    footer_text = fields.Html(string='Footer', compute=get_footer)