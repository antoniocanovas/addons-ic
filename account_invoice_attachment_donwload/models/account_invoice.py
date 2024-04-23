# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.tools import float_is_zero


class AccountInvoice(models.Model):
    _inherit = "account.move"

    @api.model
    def action_download_attachments(self):
        items = self.env['ir.attachment'].search([('res_model', '=', 'account.move')])
        if not items:
            raise UserError(
                _("None attachment selected. Only binary attachments allowed.")
            )
        ids = ",".join(map(str, items.ids))
        return {
            "type": "ir.actions.act_url",
            "url": "/web/invoice/download_zip?ids=%s" % (ids),
            "target": "self",
        }

