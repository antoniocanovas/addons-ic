from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleMandatorySaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('write_date')
    def get_purchase_forecast(self):
        for record in self:
            total = 0
            for li in record.order_line:
                if li.udo_line_ids:
                    for liudo in li.udo_line_ids:
                        if (liudo.product_id.service_tracking == 'no'):
                            total += liudo.price_unit_cost * liudo.product_uom_qty
                elif (li.product_id.service_tracking == 'no'):
                    total += li.price_unit_cost * li.product_uom_qty
                else:
                    total = total
            record['purchase_forecast'] = total

    purchase_forecast = fields.Monetary(string='Previsión Compras', store=True, compute='get_purchase_forecast')

    @api.depends('write_date')
    def get_purchase_now(self):
        for record in self:
            total = 0
            purchases = self.env['purchase.order'].search([('sale_id', '=', record.id)])
            for purchase in purchases:
                total += purchase.amount_untaxed
            record['purchase_now'] = total

    purchase_now = fields.Monetary(string='Compras Actuales', store=False, compute='get_purchase_now')

    @api.depends('write_date')
    def get_purchase_percent(self):
        for record in self:
            total = 100
            if record.purchase_forecast != 0:
                total = record.purchase_now / record.purchase_forecast * 100
            record['purchase_percent'] = total

    purchase_percent = fields.Float(string='Compras %', store=False, compute='get_purchase_percent')

    @api.depends('write_date')
    def get_time_forecast(self):
        for record in self:
            total = 0
            for li in record.order_line:
                if li.udo_line_ids:
                    for liudo in li.udo_line_ids:
                        if (liudo.product_id.service_tracking != 'no'):
                            total += liudo.product_uom_qty
                else:
                    if (li.product_id.service_tracking != 'no'):
                        total += li.product_uom_qty
            record['time_forecast'] = total

    time_forecast = fields.Float(string='Previsión Tiempo', store=False, compute='get_time_forecast')

    @api.depends('write_date')
    def get_time_now(self):
        for record in self:
            total = 0
            for li in record.timesheet_ids:
                total += li.unit_amount
            record['time_now'] = total

    time_now = fields.Float(string='Previsión Tiempo', store=False, compute='get_time_now')

    @api.depends('write_date')
    def get_time_percent(self):
        for record in self:
            total = 100
            if (record.time_forecast != 0):
                total = record.time_now / record.time_forecast * 100
            record['time_percent'] = total

    time_percent = fields.Float(string='Previsión Tiempo', store=False, compute='get_time_percent')