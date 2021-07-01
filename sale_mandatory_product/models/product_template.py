from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_mandatory = fields.Boolean(string='Sale Mandatory',  store=True, default=False)
