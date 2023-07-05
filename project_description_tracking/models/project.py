# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    description = fields.Html(tracking=100)



class ProjectTask(models.Model):
    _inherit = 'project.task'

    description = fields.Html(tracking=100)
