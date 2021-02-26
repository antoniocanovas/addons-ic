from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SectionRel(models.Model):
    _name = 'section.rel'
    _description = 'Sections Relations'

    name = fields.Char('Name')
    child_section_id = fields.Many2one(
        'sale.order.line'
    )
    father_section_id = fields.Many2one(
       'sale.order.line'
    )