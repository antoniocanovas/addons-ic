from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class Project(models.Model):
    _inherit = 'project.project'

    @api.depends('sale_order_id')
    def get_iset_word_id(self):
        if not self.iset_work_id:
            self.iset_work_id = self.sale_order_id.iset_work_id

    iset_work_id = fields.Many2one('iset.work', 'iSet Work', compute='get_iset_word_id', readonly=False)