# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api

# la consulta a tecdoc devuelve todos los coches de la serie, por lo que deberia de haber un modelo coche, quye pertenezca a una marca, modelo y serie determinada
class ViafirmaNotificationSignature(models.Model):
    _name = 'viafirma.notification.signature'
    _description = 'Viafirma Notification and Signature'

    type = fields.Char('Type', help="Variable name in partner")
    name = fields.Char('Name')
