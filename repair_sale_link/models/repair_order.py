# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models, api


class RepairOrder(models.Model):
    _inherit = "repair.order"

    sale_order_id = fields.Many2one('sale.order', string='Pedido')

