from odoo import _, api, fields, models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    fcanje_id = fields.Many2many(comodel_name='factura.canje',
                                         relation='posorder_canje_rel',
                                         column1='fcanje_id',
                                         column2='posorder_id',
                                         string="Factura de canje",
                                         )

    def _get_amount_subtotal(self):
        for record in self:
            record['amount_subtotal'] = record.amount_total - record.amount_tax
    amount_subtotal = fields.Float('Subtotal', store=False, compute='_get_amount_subtotal')