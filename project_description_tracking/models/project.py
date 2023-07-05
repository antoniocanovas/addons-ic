# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    description = fields.Html(tracking=100)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def _get_description_text(self):
        self.description_text = self.description
    description_text = fields.Text('Description', store=True, tracking=100, compute='_get_description_text')
