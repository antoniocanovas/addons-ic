# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ViafirmaAccount(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _get_viafirma(self):
        results = self.env['viafirma'].search([('invoice_id', '=', self.id)])
        self.viafirma_count = len(results)

    viafirma_count = fields.Integer('Viafirmas', compute=_get_viafirma, stored=False)

    @api.multi
    def action_view_viafirma(self):
        action = self.env.ref(
            'viafirma_account.action_viafirma_in_invoice').read()[0]
        return action
