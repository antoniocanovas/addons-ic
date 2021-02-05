# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
from odoo.exceptions import ValidationError
import base64

STATE = [
    ('DRAFT', 'DRAFT'),
    ('RECEIVED', 'RECEIVED'),
    ('ERROR', 'ERROR'),
    ('WAITING', 'WAITING'),
    ('WAITING_CHECK', 'WAITING_CHECK'),
    ('WAITING_CLIENT_SIGNATURE', 'WAITING_CLIENT_SIGNATURE'),
    ('REJECTED', 'REJECTED'),
    ('EXPIRED', 'EXPIRED'),
    ('DELETED', 'DELETED'),
    ('SENT', 'SENT'),
    ('RESPONSED', 'RESPONSED')
]

class ViafirmaDocuments(models.Model):
    _inherit = 'ir.attachment'


    viafirma_ids = fields.One2many('viafirma','document_id')
    viafirma_state = fields.Selection(selection=STATE)

    @api.multi
    def get_main_att_automated(self):
        #attachment_id = self.env['ir.attachment'].search([('id', '=', self.id)])
        #print(attachment_id.datas)
        # decoded_data = attachment_id.datas.decode('base64')
        #decoded_data = base64.b64decode(attachment_id.datas)
        #print(self.datas)
        #print(attachment_id.datas)
        #print("decoded")
        self.message_main_attachment_id = [(4, self.id)]
        self.message_post(body='Created', subtype='mail.mt_comment', attachment_ids=[self.id])
        # self.message_main_attachment_id = [(4, self.id)]

    @api.multi
    def get_main_att(self):
        if not self.preview_generated:
            print("DEBUGGER")
            attachment_id = self.env['ir.attachment'].search([('id', '=', self.id)])
            print(attachment_id.datas)
            #decoded_data = attachment_id.datas.decode('base64')
            # decoded_data = base64.b64decode(self.datas)
            print("decoded")
            #self.message_post(body='Created', subtype='mail.mt_comment', attachments=[(self.name, decoded_data)])
            # self.message_main_attachment_id = [(4, self.id)]
            self.preview_generated = True

    @api.multi
    def do_viafirma_context(self):
        for record in self:

            line_ids=[]
            line_id = self.env['viafirma.lines'].create({
                'partner_id': record.partner_id.id,
            })
            line_ids.append(line_id.id)

            notifications = []
            notification_type_ids = self.env['viafirma.notification.signature'].search([('type', '=', 'notification')])

            for tipo in notification_type_ids:
                if tipo.name == 'MAIL':
                    notifications.append(tipo.id)

            template = self.env.user.company_id.template_viafirma_documents
            if template == False:
                raise ValidationError(
                    "You must set default template for Viafirma documents")

            viafirma = self.env['viafirma'].sudo().create({
                                'name': str(self.env.user.name) + '-' + str(record.name),
                                'noti_text': str(self.env.user.name) + '-' + str(record.name),
                                'noti_subject': str(self.env.user.name) + '-' + str(record.name),
                                'notification_type_ids': [(6,0,notifications)],
                                'document_to_send': record.datas,
                                'template_type': 'base64',
                                'template_id': template.id,
                                'line_ids': [(6,0,line_ids)],
                                'document_id': record.id,
                                'res_model':'Documentos',
                                'res_id':record.id,
                                'res_id_name':str(record.name) ,
                            })


            viafirma.call_viafirma()
            record.viafirma_state = viafirma.state



