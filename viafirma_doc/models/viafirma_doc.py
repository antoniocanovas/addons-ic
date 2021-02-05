# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from odoo import fields, models, api
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class ViafirmaDoc(models.Model):
    _inherit = 'docs.docs'

    viafirma_ids = fields.One2many(
        'viafirma',
        'viafirma_doc_id'
    )
    line_ids = fields.Many2many(
        comodel_name='res.partner',
        relation = 'doc_viafirma_rel',
        colum1 = 'doc_id',
        colum2 = 'viafirma_id',
        string='Signers'
    )
    company_signed = fields.Boolean("Company signed")

    @api.multi
    def _get_viafirmas(self):
        self.viafirmas_count = len(self.viafirma_ids)

    viafirmas_count = fields.Integer('Tickets', compute=_get_viafirmas, stored=False)

    @api.multi
    def action_view_viafirmas(self):
        action = self.env.ref(
            'viafirma_doc.action_view_viafirmas').read()[0]
        return action

    @api.multi
    def viafirma_wizard(self):

        pdf = self.env.ref('viafirma_doc.viafirma_doc_report').sudo().render_qweb_pdf([self.id])[0]
        document_to_send = base64.encodebytes(pdf)

        view_id = self.env.ref('viafirma.viafirma_wizard_view').id

        line_ids = []
        for line in self.line_ids:
            line_ids.append(line.id)

        print(line_ids)

        return {
            'name': "Wizard Viafirma",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'viafirma.wizard',
            'view_id': view_id,
            'target': 'new',
            'context': {
                'default_name': str(self.name),
                'default_document_to_send': document_to_send,
                'default_model': 'doc',
                'default_line_ids': [(6, 0, self.line_ids.ids)],
                'default_company_signed': self.company_signed,
                'default_viafirma_doc_id':self.id,
            }
        }
