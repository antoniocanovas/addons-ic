# Copyright 2021 Pedro Guirao - Ingenieriacloud.com


from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    repair_ids = fields.One2many('repair.order', 'sale_order_id', string="Reparaciones")
