# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
import base64

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

    @api.multi
    def do_viafirma(self):

        pdf = self.env.ref('account.account_invoices').sudo().render_qweb_pdf([self.id])[0]

        line_ids=[]
        line_id = self.env['viafirma.lines'].create({
            'partner_id': self.partner_id.id,
        })
        line_ids.append(line_id.id)

        print(line_ids)

        viafirma_id = self.env['viafirma'].create({
            'name': str(self.env.user.name) + '-' + str(self.sequence_number_next_prefix) + str(self.sequence_number_next),
            'binary_to_encode_64': base64.encodebytes(pdf),
            'template_type': 'base64',
            'line_ids': [(6,0,line_ids)],
            #'noti_text': 'texto',
            #'noti_subject': 'subject',
            'invoice_id': self.id,
            'res_model':'Facturas',
            'res_id':self.id,
            'res_id_name':str(self.sequence_number_next_prefix) + str(self.sequence_number_next),

        })