# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class FacturaCanjeTaxline(models.Model):
    _name = 'factura.canje.taxline'
    _description = 'Facturas de canje, resumen impuestos'

    tax_id = fields.Many2one('account.tax', string='Impuesto', store=True, copy=False)
    amount = fields.Monetary('Importe', store=True, copy=False)
    fcanje_id = fields.Many2one('factura.canje', string='Factura de canje', store=True, copy=False)
    currency_id = fields.Many2one('res.currency', string='Moneda', default=1)
