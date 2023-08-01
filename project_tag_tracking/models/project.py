# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ProjectProject(models.Model):
    _inherit = 'project.project'

    tag_ids = fields.Many2many(tracking=100)



class ProjectTask(models.Model):
    _inherit = 'project.task'

    tag_ids = fields.Many2many(tracking=100)
