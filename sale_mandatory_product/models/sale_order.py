from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleMandatorySaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_mandatory = fields.Boolean(string='Sale Mandatory SO', store=True, default=True)
