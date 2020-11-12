# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import base64
import json
from datetime import datetime
import requests
from odoo.exceptions import ValidationError
from odoo import fields, models, api
from datetime import datetime

class Viafirma(models.Model):
    _name = 'viafirma'
    _description = 'Viafirma Model'


    name = fields.Char('Name')
    #res_model = fields.Reference(src_model, 'Modelo del documento origen')
    #res_id = fields.Reference(res_model.id, 'Id origen')
    #res_id_name = fields.Reference(res_model, 'Nombre del documento origen')
    res_model = fields.Char('Modelo del documento origen')
    res_id = fields.Char('Id origen')
    res_id_name = fields.Char('Nombre del documento origen')
    attachment_id = fields.Many2one('ir.attachment')
    attachment_signed_id = fields.Many2one('ir.attachment')
    create_date = fields.Date(string="Fecha creacion")
    completed_date = fields.Date(string='Fecha firma')
    #status = fields.Selection(String='Estado', related='viafirma_lines.status')
    status = fields.Selection(selection=[('borrador','Borrador'),('enviado','Enviado'),('error','Error'),('firmado','Firmado'),('rechazado','Rechazado')],string="Estado",default='borrador')
    template_id = fields.Many2one('viafirma.templates')
    line_ids = fields.One2many('viafirma.lines','viafirma_id')
    status_id = fields.Char('Código de seguimiento')

    @api.multi
    def compose_name(self):
        self.compose_name = ir.model + ir.model.name + str(datetime.utcnow().strftime('%d-%m-%Y'))

    # name = fields.Char('Name', compute='compose_name')

    @api.multi
    def send_viafirma(self):
        return

    def get_uploader_header(self):

        header = {
            'Content-Type': 'application/json',
        }
        return header

    def compose_call(self):
        ''' tenemos que componer la llamada a la firma, por lo que tenemos que conocer el groupcode, el texto de la notificacion
            y a quien mandar dicha notificacion. Lo anterior no esta en el modelo Viafirma, como lo rellenaremos? A parte hemos de indicar quien recibirá la respuesta de la firma'''

        data = {
            "groupCode": "inelga",
            "workflow": {
                "type": "WEB"
            },
            "notification": {
                "text": "TEST Firma web",
                "detail": "notificado vía email",
                "notificationType": "MAIL",
                "sharedLink": {
                    "appCode": "com.viafirma.documents",
                    "email": "luismi@ingenieriacloud.com",
                    "phone": "+34627161870",
                    "subject": "TEST firma remota"
                }
            },
            "document": {
                "templateType": "url",
                "templateReference": "https://descargas.viafirma.com/documents/example/doc_sample_2018.pdf",
                "policyCode": "test002"
            },
            "callbackMails": "luismi@ingenieriacloud.com",
            "callbackURL": ""
        }
        return data

    def status_response_firmweb(self):
        ''' Esta funcion ha de obtener el estado de la peticion'''

        header = self.get_uploader_header()
        response_code = self.status_id

        search_url = 'https://sandbox.viafirma.com/documents/api/v3/messages/status/' + response_code

        viafirma_user = self.env.user.company_id.user_viafirma
        viafirma_pass = self.env.user.company_id.pass_viafirma

        if viafirma_user & viafirma_pass:

            stat_firmweb = requests.get(search_url, headers=header, auth=(viafirma_user, viafirma_pass))
            if stat_firmweb.ok:
                statu_firmweb = json.loads(stat_firmweb.content)
                # statu_firmweb["status"] contiene el estado actual de la peticion y que me puede servir para cambiar el campo viafirma.status
                if statu_firmweb["status"] == 'RESPONSED':
                    # ya ha sido firmada me puedo descargar el documento firmado y el trail de la firma
                    # empezamos por el documento firmado
                    url = 'https://sandbox.viafirma.com/documents/api/v3/documents/download/signed/' + response_code
                    r_doc_sig = requests.get(search_url, headers=header, auth=(viafirma_user, viafirma_pass))
                    if r_doc_sig.ok:
                        rr_doc_sio = json.loads(r_doc_sig.content)
                        # con esto obtengo el link en el campo "link" lo tengo que descargar y unir al campo viafirma.attachment_signed_id
                    # ahora le toca el turno al documento de trail, pero para este documento no hay campo en el modelo viafirma, lo dejo preparado
                    url = 'https://sandbox.viafirma.com/documents/api/v3/documents/download/trail/' + response_code
                    r_doc_trail = requests.get(search_url, headers=header, auth=(viafirma_user, viafirma_pass))
                    if r_doc_trail.ok:
                        rr_doc_trail = json.loads(r_doc_trail.content)
                        # con esto obtengo el link en el campo "link" lo tengo que descargar y unir al campo viafirma.XXXXX (os recuerdo que no hay campo porque se ha considerado no guardarlo
        else:
            raise ValidationError(
                "You must set Viafirma login Api credentials")

    def firma_web(self):
        ''' solo firma web y un solo firmante, la mas simple de todas, de momento selecciono todos los registros que tenga en el modelo viafirma y que haga el proceso
         de envio para cada uno de ellos, aunque no coge ningun valor de estos, ni emqail ni adjunto'''
        viafirma_user = self.env.user.company_id.user_viafirma
        viafirma_pass = self.env.user.company_id.pass_viafirma

        if viafirma_user:
            if viafirma_pass:
                print("Inicio commm")
                envios = self.env['viafirma'].search([('status', '=', 'borrador')])
                for envio in envios:
                    print(envio)
                    header = self.get_uploader_header()
                    search_url = 'https://sandbox.viafirma.com/documents/api/v3/messages/'
                    datas = self.compose_call()

                    response_firmweb = requests.post(search_url, data=json.dumps(datas), headers=header,
                                                     auth=(viafirma_user, viafirma_pass))

                    print(response_firmweb, response_firmweb.content.decode('utf-8'), response_firmweb.ok)
                    if response_firmweb.ok:
                        #resp_firmweb = json.loads(response_firmweb.content.decode('utf-8'))
                        resp_firmweb = response_firmweb.content.decode('utf-8')
                        print(resp_firmweb)
                        # normalmente devuelve solo un codigo pero puede ser que haya mas, ese código hay que almacenarlo en viafirma.status_id para su posterior consulta de estado
                        envio.status_id =  resp_firmweb
        else:
            raise ValidationError(
                        "You must set Viafirma login Api credentials")
