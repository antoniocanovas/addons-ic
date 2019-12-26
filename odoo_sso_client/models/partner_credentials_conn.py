# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class PartnerConnFields(models.Model):
    _inherit = 'partner.credentials'

    url_sso = fields.Char('Servidor')
    db = fields.Char('Base de Datos')

