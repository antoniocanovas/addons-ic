from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    iset_work_id = fields.Many2one('iset.work', 'iSet Work')
