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
    attachment_trail_url = fields.Char('Url documento de Trail firmado')

    create_date = fields.Date(string="Fecha creacion")
    completed_date = fields.Date(string='Fecha firma')

    #status = fields.Selection(String='Estado', related='viafirma_lines.status')
    #status = fields.Selection(selection=[('borrador','Borrador'),('enviado','Enviado'),('error','Error'),('firmado','Firmado'),('rechazado','Rechazado')],string="Estado",default='borrador')
    status = fields.Char('Estado', default = 'Borrador')
    template_id = fields.Many2one('viafirma.templates')
    line_ids = fields.One2many(
        'viafirma.lines',
        'viafirma_id'
    )
    status_id = fields.Char(string='Código de seguimiento')
    noti_text = fields.Char(string='Texto de la notificacion')
    noti_detail = fields.Char(string='Detalle de la notificación')
    noti_tipo = fields.Many2many(
        comodel_name="viafirma.notification.signature",
        string="Tipo de Notificacione",
        domain=[('type', '=', 'notification')],
    )
    noti_subject = fields.Char(string='Asunto de la notificacion')
    police_code = fields.Char(string='Codigo de la politica',default='test002')
    template_type = fields.Selection(selection=[('url','URL'),('base64','BASE64'),('message','MESSAGE')],string="Tipo de teemplate",default='base64')
    templareReference = fields.Char(defautl='"templateReference": ')  # este campo sirve para construir la linea que puede ser una url, base65 o un codigo
    document_readRequired = fields.Boolean(string='Requiere lectura obligatoria',default=False)
    document_watermarkText = fields.Char(string='Texto a poner como marca de agua')
    document_formRequired = fields.Boolean(string='Hay que rellenar un formulario',default=False)

    viafirma_groupcode_id = fields.Many2one(
        'viafirma.groups',
        string="Código de grupo",
    )
    binary_to_encode_64 = fields.Binary("Documento ejemplo")
    error_text = fields.Char('Texto del error')


    @api.multi
    def compose_name(self):
        self.compose_name = ir.model + ir.model.name + str(datetime.utcnow().strftime('%d-%m-%Y'))

    # name = fields.Char('Name', compute='compose_name')

    @api.multi
    def send_viafirma(self):
        return

    @api.multi
    def upd_viafirma(self):
        ''' chequeamos cada 5 minutos por cron el estado de los viafirma que no tengan estado RESPONSED (finalizado) para
        actualizar su estado cada cierto tiempo y ver si ha habido algun error'''

        viafirmas =self.env['viafirma'].search([('status', '!=', 'RESPONSED')])
        print(viafirmas)
        for via in viafirmas:
            via.status_response_firmweb()

    def get_uploader_header(self):

        header = {
            'Content-Type': 'application/json',
        }
        return header

    def compose_call(self):
        ''' tenemos que componer la llamada a la firma, por lo que tenemos que conocer el groupcode, el texto de la notificacion
            y a quien mandar dicha notificacion. Lo anterior no esta en el modelo Viafirma, como lo rellenaremos? A parte hemos de indicar quien recibirá la respuesta de la firma'''

        # def_check_parameters

        groupCode = {
            "groupCode": self.viafirma_groupcode_id.name,
        }
        workflow = {
            "workflow": {
                "type": "WEB",
            },
        }

        if len(self.noti_tipo) > 1:

            notification = {
                "notification": {
                    "text": self.noti_text,
                    "detail": self.noti_detail,
                    "notificationType": "MAIL_SMS",
                    "sharedLink": {
                        "appCode": "com.viafirma.documents",
                        "email": self.line_ids.partner_id.email,  #
                        "phone": self.line_ids.partner_id.mobile,
                        "subject": self.noti_subject
                    }
                },
            }
        else:
            notification = {
                "notification": {
                    "text": self.noti_text,
                    "detail": self.noti_detail,
                    "notificationType": self.noti_tipo[0].name,
                    "sharedLink": {
                        "appCode": "com.viafirma.documents",
                        "email": self.line_ids.partner_id.email,  #
                        "phone": self.line_ids.partner_id.mobile,
                        "subject": self.noti_subject
                    }
                },
            }

        metadatalist = {
            "metadataList": [{
                "key": "MOBILE_SMS_01",
                "value": self.line_ids.partner_id.mobile
            }],
        }
        document = {
            "document": {
                "templateType": self.template_type,
                #"templateReference": "https://descargas.viafirma.com/documents/example/doc_sample_2018.pdf",
                "templateReference": str(self.binary_to_encode_64.decode('ascii')),
                "templateCode": self.template_id.code
            },
        }
        callbackmails = {
            "callbackMails": self.env.user.email,
        }
        callbackurl = {
            "callbackURL": ""
        }

        data = {**groupCode, **workflow, **notification, **metadatalist, **document, **callbackmails, **callbackurl }
        return data


    def status_response_firmweb(self):
        ''' Esta funcion ha de obtener el estado de la peticion'''

        header = self.get_uploader_header()
        response_code = self.status_id

        search_url = 'https://sandbox.viafirma.com/documents/api/v3/messages/status/' + str(response_code)
        #print(search_url)

        viafirma_user = self.env.user.company_id.user_viafirma
        viafirma_pass = self.env.user.company_id.pass_viafirma

        if viafirma_user:
            if viafirma_pass:

                stat_firmweb = requests.get(search_url, headers=header, auth=(viafirma_user, viafirma_pass))
                if stat_firmweb.ok:
                    statu_firmweb = json.loads(stat_firmweb.content.decode('utf-8'))
                    # de momento lo hago con la primera line_ids que hay
                    self.line_ids.status = statu_firmweb["status"]
                    self.status = statu_firmweb["status"]
                    # statu_firmweb["status"] contiene el estado actual de la peticion y que me puede servir para cambiar el campo viafirma.status
                    if statu_firmweb["status"] == 'RESPONSED':
                        # ya ha sido firmada me puedo descargar el documento firmado y el trail de la firma
                        # empezamos por el documento firmado
                        url = 'https://sandbox.viafirma.com/documents/api/v3/documents/download/signed/' + response_code
                        r_doc_sig = requests.get(url, headers=header, auth=(viafirma_user, viafirma_pass))
                        if r_doc_sig.ok:
                            rr_doc_sio = json.loads(r_doc_sig.content.decode('utf-8'))
                            # con esto obtengo el link en el campo "link" lo tengo que descargar y unir al campo viafirma.attachment_signed_id
                        # ahora le toca el turno al documento de trail, pero para este documento no hay campo en el modelo viafirma, lo dejo preparado
                        url = 'https://sandbox.viafirma.com/documents/api/v3/documents/download/trail/' + response_code
                        r_doc_trail = requests.get(url, headers=header, auth=(viafirma_user, viafirma_pass))
                        if r_doc_trail.ok:
                            rr_doc_trail = json.loads(r_doc_trail.content.decode('utf-8'))
                            # con esto obtengo el link en el campo "link" lo tengo que descargar y unir al campo viafirma.XXXXX (os recuerdo que no hay campo porque se ha considerado no guardarlo
                            self.attachment_trail_url = rr_doc_trail["url"]
                    elif statu_firmweb['status'] == 'ERROR':
                        # guardar el resultado de error en un campo para su visualizacion
                        url = 'https://sandbox.viafirma.com/documents/api/v3/messages/' + response_code
                        r_error = requests.get(url, headers=header, auth=(viafirma_user, viafirma_pass))
                        #print("R_error", r_error, url)
                        if r_error.ok:
                            rr_error = json.loads(r_error.content)
                            print("Pedro Error", rr_error)
                            # los dos campos de este dictionary interesantes son message y trace
                            self.error_text =  rr_error["workflow"]["history"]
        else:
            raise ValidationError(
                "You must set Viafirma login Api credentials")

    @api.multi
    def check_mandatory_attr(self, signot):
        for attr in signot:
            try:
                value = getattr(self.line_ids.partner_id, attr.value)
            except Exception as e:
                raise ValidationError(
                    "Server Error : %s" % e)
            if not value:
               raise ValidationError(
                   "%s is mandatory for this template" % attr.value)

    @api.multi
    def firma_web(self):
        ''' solo firma web y un solo firmante, la mas simple de todas, de momento selecciono todos los registros que tenga en el modelo viafirma y que haga el proceso
         de envio para cada uno de ellos, aunque no coge ningun valor de estos, ni emqail ni adjunto'''

        #Comprobamos todas las restricciones para informar al ususario antes de iniciar ejecución
        if not self.env['viafirma.templates'].updated_templates(self.template_id.code):
            raise ValidationError(
                "Template no existe")

        if self.line_ids:
            self.check_mandatory_attr(self.template_id.firma_ids)
            self.check_mandatory_attr(self.noti_tipo)

            if not self.binary_to_encode_64:
                raise ValidationError(
                    "Need a binary to send")

            viafirma_user = self.env.user.company_id.user_viafirma
            viafirma_pass = self.env.user.company_id.pass_viafirma

            if viafirma_user:
                if viafirma_pass:
                    header = self.get_uploader_header()
                    search_url = 'https://sandbox.viafirma.com/documents/api/v3/messages/'
                    datas = self.compose_call()

                    response_firmweb = requests.post(search_url, data=json.dumps(datas), headers=header,
                                                     auth=(viafirma_user, viafirma_pass))
                    if response_firmweb.ok:
                        #resp_firmweb = json.loads(response_firmweb.content.decode('utf-8'))
                        resp_firmweb = response_firmweb.content.decode('utf-8')
                        # normalmente devuelve solo un codigo pero puede ser que haya mas, ese código hay que almacenarlo en viafirma.status_id para su posterior consulta de estado
                        self.status_id =  resp_firmweb
                        self.status_response_firmweb()
            else:
                raise ValidationError(
                            "You must set Viafirma login Api credentials")
        else:
            raise ValidationError(
                "No hay firmantes seleccionados")


        # Esto para multiples records desde interfaz
        def firma_web_multi(self):
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
                        print(datas)

                        response_firmweb = requests.post(search_url, data=json.dumps(datas), headers=header,
                                                         auth=(viafirma_user, viafirma_pass))

                        print(response_firmweb, response_firmweb.content.decode('utf-8'), response_firmweb.ok)
                        if response_firmweb.ok:
                            # resp_firmweb = json.loads(response_firmweb.content.decode('utf-8'))
                            resp_firmweb = response_firmweb.content.decode('utf-8')
                            print(resp_firmweb)
                            # normalmente devuelve solo un codigo pero puede ser que haya mas, ese código hay que almacenarlo en viafirma.status_id para su posterior consulta de estado
                            envio.status_id = resp_firmweb
                            # ya puedo hacer la primera consulta para saber si ha habido algun error
                            self.status_response_firmweb()
            else:
                raise ValidationError(
                    "You must set Viafirma login Api credentials")
