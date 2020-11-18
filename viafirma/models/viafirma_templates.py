# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
import json
import requests

# la consulta a tecdoc devuelve todos los coches de la serie, por lo que deberia de haber un modelo coche, quye pertenezca a una marca, modelo y serie determinada
class ViafirmaTemplates(models.Model):
    _name = 'viafirma.templates'
    _description = 'Viafirma Templates'

    name = fields.Char('Name')
    code = fields.Char('Code')
    description = fields.Char('Description')
    firma_ids = fields.Many2many(
        comodel_name="viafirma.notification.signature",
        string="Firmas",
        domain=[('type', '=', 'signature')],
    )


    def get_uploader_header(self):

        header = {
            'Content-Type': 'application/json',
        }
        return header

    @api.multi
    def create_templates(self, thedict):
        '''Esta funcion actualiza las plantillas y crea las nuevas'''

        existe = self.env['viafirma.templates'].search([('code', '=', thedict["code"])])
        if not existe:
            viafirma_template_id = self.env['viafirma.templates'].create({
                'name': thedict["code"],
                'code': thedict["code"],
                'description': thedict["title"]
            })
            return viafirma_template_id

    @api.multi
    def updated_templates(self):

        viafirma_user = self.env.user.company_id.user_viafirma
        viafirma_pass = self.env.user.company_id.pass_viafirma

        if viafirma_user:
            if viafirma_pass:

                header = self.get_uploader_header()
                search_url = 'https://sandbox.viafirma.com/documents/api/v3/template/list/antonio.canovas@ingenieriacloud.com'
                response_template = requests.get(search_url, headers=header, auth=(viafirma_user, viafirma_pass))
                if response_template.ok:
                    resu_templates = json.loads(response_template.content)
                    for resu_template in resu_templates:
                        self.create_templates(resu_template)