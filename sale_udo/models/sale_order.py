from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoSaleOrder(models.Model):
    _inherit = 'sale.order.line'



