# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api

# la consulta a tecdoc devuelve todos los coches de la serie, por lo que deberia de haber un modelo coche, quye pertenezca a una marca, modelo y serie determinada
class ViafirmaTemplates(models.Model):
    _name = 'viafirma.templates'
    _description = 'Viafirma Templates'

    name = fields.Char('Name')
    code = fields.Char('Code')
    description = fields.Char('Description')

    @api.multi
    def upd_templates(self):
        tempateupdate = self.env['viafirma.operations']
        tempateupdate.updated_templates()
