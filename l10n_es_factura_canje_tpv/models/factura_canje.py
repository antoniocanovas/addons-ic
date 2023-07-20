# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class FacturaCanje(models.Model):
    _name = 'factura.canje'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Facturas de canje'

    name = fields.Char(string='Nombre', required=True)
    date = fields.Date(string='Fecha', default=lambda self: fields.datetime.now())
    partner_id = fields.Many2one('res.partner', string='Partner')
    type = fields.Selection([('actual', 'Actual'),('historica','Histórica')], string='Type', default='actual')
    description = fields.Text('Description')
    pos_order_ids = fields.Many2many(comodel_name='pos.order',
                                     relation='posorder_canje_rel',
                                     column1='posorder_id',
                                     column2='fcanje_id',
                                     string="Factura de canje",
                                     domain="[('fcanje_id','=',False),('state','in',['done','paid'])]"
                                     )

    amount_total = fields.Monetary('Total', store=True, copy=False)
    amount_tax = fields.Monetary('Impuestos', store=True, copy=False)
    amount_subtotal = fields.Monetary('Subtotal', store=True, copy=False)
    currency_id = fields.Many2one('res.currency', default=1, store=True)
    tax_line_ids = fields.One2many('factura.canje.taxline', 'fcanje_id', store=True, copy=False)

#    @api.onchange('pos_order_ids')
    def get_fcanje_taxlines(self):
        monetary_precision = self.env['decimal.precision'].sudo().search([('id', '=', 1)]).digits
        for l in self.tax_line_ids:
            l.unlink()

        impuestos = []
        amount_total, amount_tax = 0, 0
        for po in self.pos_order_ids:
            amount_total += po.amount_total
            amount_tax += po.amount_tax
            for li in po.lines:
                for tax in li.tax_ids_after_fiscal_position:
                    if tax not in impuestos: impuestos.append(tax)
        for im in impuestos:
            amount = 0
            for po in self.pos_order_ids:
                for li in po.lines:
                    for tax in li.tax_ids_after_fiscal_position:
                        if tax.id == im.id:
                            amount += round(li.price_subtotal * (im.amount / 100), monetary_precision)
            new = self.env['factura.canje.taxline'].create({'fcanje_id': self.id, 'amount': amount, 'tax_id': im._origin.id})
        self.write({'amount_total':amount_total, 'amount_tax':amount_tax, 'amount_subtotal':amount_total - amount_tax})


    @api.depends('create_date')
    def _get_pos_factura_canje_code(self):
        self.name = self.env['ir.sequence'].next_by_code('pos.factura.canje.code')
    name = fields.Char('Code', store=True, readonly=True, compute=_get_pos_factura_canje_code)
