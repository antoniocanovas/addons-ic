from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    vehicle_ids = fields.Many2many('product.template',domain=[('is_vehicle','=','True')])


