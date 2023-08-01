# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProjectTask(models.Model):
    _inherit = 'project.task'

    tag_ids = fields.Many2many(tracking=100)
