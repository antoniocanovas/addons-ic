# Copyright 2020 Ingeniería Cloud - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import fields, models


class NrcTemplate(models.Model):
    _name = 'nrc.template'
    _description = 'NRC Template'

    name = fields.Char(
        required=True,
    )
    nrc_type = fields.Selection(
        selection=[
            ('nrc_request', 'NRC Request'),
            ('nrc_line', 'NRC Line'),
            ('nrc_end', 'NRC End'),
            ('nrc_answer', 'NRC Answer'),
        ],
        string='NRC Type',
    )
    line_ids = fields.One2many(
        comodel_name='nrc.template.line',
        inverse_name='nrc_id',
        string='NRC Lines',
    )
    note = fields.Html()


class NrcTemplateLine(models.Model):
    _name = 'nrc.template.line'
    _description = 'NRC Template Line'
    _order = 'sequence asc'

    nrc_id = fields.Many2one(
        comodel_name='nrc.template',
        string='NRC Template',
    )
    sequence = fields.Integer(
        default=1,
        required=True,
    )
    position = fields.Integer(
        required=True,
    )
    length = fields.Integer(
        required=True,
    )
    char_type = fields.Selection(
        selection=[
            ('numeric', 'Numeric'),
            ('alphanumeric', 'Alphanumeric'),
        ],
        string='Type',
    )
    description = fields.Char(
        required=True,
    )
    padding = fields.Selection(
        selection=[
            ('zeros', 'With Zeros'),
            ('blanks', 'With Blanks'),
        ],
        string='Padding',
    )
    required = fields.Boolean(
        string='Is Required?',
    )
