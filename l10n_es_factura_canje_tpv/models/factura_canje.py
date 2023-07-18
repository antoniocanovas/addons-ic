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

    @api.depends('pos_order_ids', 'pos_order_ids.amount_total', 'pos_order_ids.amount_tax')
    def get_fcanje_taxlines(self):
        for record in self:
            record.tax_line_ids.unlink()
            impuestos = []
            for po in record.pos_order_ids:
                for li in po.lines:
                    for tax in li.tax_ids_after_fiscal_position:
                        if tax not in impuestos: impuestos.append(tax)
            for im in impuestos:
                amount = 0
                for po in record.pos_order_ids:
                    for li in po.lines:
                        for tax in li.tax_ids_after_fiscal_position:
                            if tax.id == im.id:
                                amount += li.price_subtotal * (im.amount / 100)
                new = env['tax_line_ids'].create({'fcanje_id': record.id, 'amount': amount, 'tax_id': im.id})

    tax_line_ids = fields.One2many('factura_canje_taxline', 'fcanje_id', store=True, copy=False, readonly=True)

    @api.depends('create_date')
    def _get_pos_factura_canje_code(self):
        self.name = self.env['ir.sequence'].next_by_code('pos.factura.canje.code')
    name = fields.Char('Code', store=True, readonly=True, compute=_get_pos_factura_canje_code)
