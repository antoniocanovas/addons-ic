from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    iset_id = fields.Many2one('work.base')
    mrp_state = fields.Selection(related='raw_material_production_id.state', store=False)
    mrp_is_locked = fields.Boolean(related='raw_material_production_id.is_locked', store=False)