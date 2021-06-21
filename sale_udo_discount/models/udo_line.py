from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoLine(models.Model):
    _inherit = 'udo.line'

    fixed_cost = fields.Boolean(
        string='Fixed',
        help="If active this price will not be recalculated with product cost",
        store=True,
        readonly=False,
    )
