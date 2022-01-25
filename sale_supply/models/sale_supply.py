# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = 'account.account'


    is_supply  = fields.Boolean(string='Es suplido')



