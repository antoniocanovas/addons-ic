# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
from odoo.exceptions import ValidationError

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
                                'name': str(record.env.user.name) + '-' + str(record.name),
                                'noti_text': str(record.env.user.name) + '-' + str(record.name),
                                'noti_subject': str(record.env.user.name) + '-' + str(record.name),
                                'noti_tipo': [(6,0,notifications)],
                                'document_to_send': record.datas,
                                'template_type': 'base64',
                                'template_id': template.id,
                                'line_ids': [(6,0,line_ids)],
                                'document_id': record.id,
                                'res_model':'Documentos',
                                'res_id':record.id,
                                'res_id_name':str(record.name) ,
                            })


            viafirma.firma_web()
            record.viafirma_state = viafirma.state



