# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools import html2plaintext

class ProjectProject(models.Model):
    _inherit = 'project.project'

    description = fields.Html(tracking=100)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    tag_ids = fiels.Many2many(tracking=100)

    @api.depends('description')
    def _get_description_text(self):
        for record in self:
            record['description_text'] = html2plaintext(record.description or "")
    description_text = fields.Text('Description', store=True, tracking=100, compute='_get_description_text')
