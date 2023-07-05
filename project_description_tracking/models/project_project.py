# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _name = 'project.project'

    description = fields.Html(tracking=100)
