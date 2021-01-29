# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class HelpdeskPC(models.Model):
    _inherit = 'helpdesk.ticket'

    partner_credentials_id = fields.Many2one('partner.credentials')
