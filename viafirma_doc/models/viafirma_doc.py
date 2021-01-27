# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
from odoo import fields, models, api
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class ViafirmaDoc(models.Model):
    _inherit = 'docs.docs'

    viafirma_ids = fields.One2many('viafirma', 'viafirma_doc_id')
    line_ids = fields.One2many(
        'viafirma.lines',
        'viafirma_doc_id',
        string='Firmantes'
    )
    company_signed = fields.Boolean("Firma empresa")

    @api.multi
    def do_viafirma_doc(self):
        view_id = self.env.ref('viafirma.viafirma_form').id

        line_ids = []
        for line in self.line_ids:
            line_ids.append(line.id)

        if self.company_signed:
            line_id = self.env['viafirma.lines'].create({
                'partner_id': self.env.user.company_id.partner_id.id,
                'viafirma_doc_id': self.id,
            })
            line_ids.append(line_id.id)

        viafirma_id = self.env['viafirma'].create({
            'name': str(self.env.user.name) + '-' + str(self.name),
            'noti_text': str(self.env.user.name) + '-' + str(self.name),
            'noti_subject': str(self.env.user.name) + '-' + str(self.name),
            'line_ids': [(6, 0, line_ids)],
            'template_type': 'base64',
            # 'noti_text': 'texto',
            # 'noti_subject': 'subject',
            'viafirma_doc_id': self.id,
            'res_model': 'Documentos',
            'res_id': self.id,
            'res_id_name': str(self.name),
            'document_policies': True,
        })

        pdf = self.env.ref('viafirma_doc.viafirma_doc_report').sudo().render_qweb_pdf([self.id])[0]

        viafirma_id.document_to_send = base64.encodebytes(pdf)

        return {
            'name': "Nuevo Viafirma",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'viafirma',
            'res_id': viafirma_id.id,
            # 'view_id': view_id,
            'domain': [('id', '=', viafirma_id)],
            'target': 'new',
        }