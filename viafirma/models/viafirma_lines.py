# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api

# la consulta a tecdoc devuelve todos los coches de la serie, por lo que deberia de haber un modelo coche, quye pertenezca a una marca, modelo y serie determinada
class ViafirmaLines(models.Model):
    _name = 'viafirma.lines'
    _description = 'Viafirma Lines'

    name = fields.Char(string='Nombre',related='partner_id.name', store=False)
    email = fields.Char(string='Email',related='partner_id.email', store=False)
    mobile = fields.Char(string='Mobile', related='partner_id.mobile', store=False)
    partner_id = fields.Many2one(
        'res.partner',
    )
    signed_date = fields.Date(string='Signed date')
    status = fields.Selection(selection=[('borrador','Borrador'),('RECEIVED','RECEIVED'),('ERROR','ERROR'),('firmado','Firmado'),('rechazado','Rechazado')],string="Estado",default='borrador')
    viafirma_id = fields.Many2one('viafirma')
