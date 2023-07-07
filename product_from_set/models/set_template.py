# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SetTemplate(models.Model):
    _name = 'set.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Set Template'

    name = fields.Char(string='Nombre', required=True)
    code = fields.Char(string='Nombre', required=True)
