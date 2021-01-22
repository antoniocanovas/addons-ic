# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ViafirmaExtend(models.Model):
    _inherit = 'viafirma'

    invoice_id = fields.Many2one('account.invoice', string='Factura')
