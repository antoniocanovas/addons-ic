
from odoo import models, api, fields
from datetime import timedelta


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    _order = 'id asc'
    #_order = 'layout_category_id,id asc'

    seller_ids = fields.Many2one(
        comodel_name="res.partner",
        string='Proveedor'
    )

    product_cost_price = fields.Float(string='Precio Coste')
    product_net_cost_price = fields.Float(string='Precio Coste Neto',
                                          detault=0.0)
    product_discount_seller = fields.Float(string='Descuento Proveedor')
    product_margin_price = fields.Float(string='Margen')

    #@api.onchange('product_id')
    #def _onchange_product_id(self):
    ##    print("ONCHANGE")
    #    if self.product_id:
    #        self.seller_ids = ''
    #        domain_seller = [
    #            ('id', 'in', self.product_id.seller_ids.ids)]
    #        return {'domain': {'seller_ids': domain_seller}}

    @api.onchange('seller_ids')
    def _onchange_seller_ids(self):
        discount_seller = 0
        product_price = self.env['product.supplierinfo'].search(
            [
                ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id),
                ('partner_id', '=', self.seller_ids.id),
                ('date_start', '<=', fields.Datetime.now()),
                '|',
                ('date_end', '>=', fields.Datetime.now()),
                ('date_end', '=', False),
            ]
        )

        self.product_cost_price = product_price.price
        self.product_discount_seller = product_price.discount
        discount_seller = self.product_cost_price * (
                product_price.discount / 100)
        self.product_net_cost_price = self.product_cost_price - discount_seller

        self.price_unit = self.product_net_cost_price
        if self.product_margin_price > 0:
            self.calcula_coste_product()

    @api.onchange('product_margin_price')
    def _onchange_product_margin_price(self):
        if self.seller_ids:
            self.calcula_coste_product()

    def calcula_coste_product(self):
        margin = self.product_net_cost_price * (self.product_margin_price / 100)
        self.price_unit = self.product_net_cost_price + margin


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pnt_collaborator_id = fields.Many2one(
        comodel_name="res.partner",
        string='Collaborator',
        domain="[('is_company','=',1)]",
    )

    #def pnt_sort_order_line(self):
    #    i = 1
    #    for record in sorted(self.order_line, key=lambda x: (
    #            x.layout_category_id.sequence, x.name)):
    #        record.sequence = i
    #        i += 1

    def calc_price_sale_order(self):
        discount_seller = 0

        order_lines = self.env['sale.order.line'].search([
            ('order_id', '=', self.id)
        ])

        for record in order_lines:

            product_price = self.env['product.supplierinfo'].search(
                [
                    ('product_tmpl_id', '=',
                     record.product_id.product_tmpl_id.id),
                    ('name', '=', record.seller_ids.id),
                    ('date_start', '<=', fields.Datetime.now()),
                    '|',
                    ('date_end', '>=', fields.Datetime.now()),
                    ('date_end', '=', False),
                ], limit=1
            )
            if product_price:
                record.product_cost_price = product_price.price
                record.product_discount_seller = product_price.discount
                ########## Precomentado antes de migrar #########
                # if fields.Datetime.now() >= product_price.date_start \
                #        and (fields.Datetime.now() <= product_price.date_end or not product_price.date_end) \
                #        and product_price.discount:

                discount_seller = record.product_cost_price * (
                        product_price.discount / 100)
                record.product_net_cost_price = record.product_cost_price - discount_seller
                record.price_unit = record.product_net_cost_price

                if record.product_margin_price > 0:
                    record.calcula_coste_product()

                margin = record.product_net_cost_price * (
                        record.product_margin_price / 100)
                record.price_unit = record.product_net_cost_price + margin

    #@api.multi
    #def order_lines_layouted(self):
    #    report_pages = super(SaleOrder, self).order_lines_layouted()
    #    new_pages = []
    #    cont = 0
    #    for pages in report_pages:
    #        for section in pages:
    #            pages[cont]['lines'] = sorted(section['lines'],
    #                                          key=lambda r: r.name)
    #            cont += 1
    #        new_pages.append(pages)
    #    return new_pages

    #@api.multi
    #def picking_lines_layouted(self):
    #    report_pages = super(SaleOrder, self).order_lines_layouted()
    #    new_pages = []
    #    cont = 0
    #    for pages in report_pages:
    #        for section in pages:
    #            pages[cont]['lines'] = sorted(section['lines'],
    #                                          key=lambda r: r.sequence)
    #            cont += 1
    #        new_pages.append(pages)
    #    return new_pages
