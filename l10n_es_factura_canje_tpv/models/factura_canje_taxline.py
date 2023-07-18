# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class FacturaCanjeTaxline(models.Model):
    _name = 'factura.canje.taxline'
    _description = 'Facturas de canje, resumen impuestos'

    name = fields.Char('Name', related='fcanje_id.name')
    tax_id = fields.Many2one('account.tax', string='Impuesto', store=True)
    amount = fields.Monetary('Importe', store=True)
    fcanje_id = fields.Many2one('factura.canje', string='Factura de canje', store=True)
    currency_id = fields.Many2one('res.currency', string='Moneda', store=True, default=1)
