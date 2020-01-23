# Copyright 2020 Ingeniería Cloud - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_irnr_partner = fields.Boolean(
        string='Is an IRNR Partner?'
    )
    nrc_import = fields.Float(
        string='NRC Import',
    )

    @api.onchange('property_account_position_id')
    def fiscal_position_change_irnr(self):
        if self.property_account_position_id:
            fp = self.property_account_position_id
            no_ue1 = self.env.ref('l10n_es_irnr.fp_irpfnrnue24')
            no_ue2 = self.env.ref('l10n_es_irnr.fp_irpfnrue19')
            if not no_ue1 or not no_ue2:
                raise UserError(_('You must update chart template in order to '
                                  'be able to use this module.'))
            self.is_irnr_partner = fp.id == no_ue1.id or fp.id == no_ue2.id

