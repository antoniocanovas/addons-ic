from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    @api.depends('sale_order_id')
    def get_iset_word_id(self):
        if not self.work_extended_id:
            self.work_extended_id = self.sale_order_id.work_extended_id

    work_extended_id = fields.Many2one('work.extended', 'Work extended', compute='get_iset_word_id', readonly=False)