# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
import json
from datetime import datetime
import requests
from odoo.exceptions import ValidationError


import logging

_logger = logging.getLogger(__name__)

#try:
#    from odoo.addons.queue_job.job import job
#except ImportError:
#    _logger.debug('Can not `import queue_job`.')
#    import functools

STATE = [
    ('sending', 'Sending'),
    ('processing', 'Processing'),
    ('error', 'Error'),
    ('done', 'Done'),
]

def add_guiones_fecha(lafecha):
    ''' utilidad que permite construir una fecha coin formato no odoo en formato aceptado por odoo '''
    fecha = str(lafecha)
    date_return = str(fecha[0:4])+'-'+str(fecha[4:])+'-01'
    return date_return

class ViafirmaOperations(models.Model):
    _name = 'viafirma.operations'
    _description = 'Viafirma Operations'

    state = fields.Selection(
        selection=STATE, string="State", default='draft', track_visibility='onchange'
    )
    search_transaction_error = fields.Char('Search Error Code')

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
        response_code = self.env('viafirma').tracking_code

        search_url = 'https://sandbox.viafirma.com/documents/api/v3/messages/status/'+ response_code

        ## user company viafrima data

        stat_firmweb = requests.get(search_url, headers=header,auth=('dev_inelga', 'PnCDKj5HrR'))
        if stat_firmweb.ok:
            statu_firmweb = json.loads(stat_firmweb.content)
            # statu_firmweb["status"] contiene el estado actual de la peticion y que me puede servir para cambiar el campo viafirma.status
            if statu_firmweb["status"] == 'RESPONSED':
                # ya ha sido firmada me puedo descargar el documento firmado y el trail de la firma
                # empezamos por el documento firmado
                url = 'https://sandbox.viafirma.com/documents/api/v3/documents/download/signed/' + response_code
                r_doc_sig =  requests.get(search_url, headers=header,auth=('dev_inelga', 'PnCDKj5HrR'))
                if r_doc_sig.ok:
                    rr_doc_sio = json.loads(r_doc_sig.content)
                    # con esto obtengo el link en el campo "link" lo tengo que descargar y unir al campo viafirma.attachment_signed_id
                # ahora le toca el turno al documento de trail, pero para este documento no hay campo en el modelo viafirma, lo dejo preparado
                url = 'https://sandbox.viafirma.com/documents/api/v3/documents/download/trail/' + response_code
                r_doc_trail = requests.get(search_url, headers=header, auth=('dev_inelga', 'PnCDKj5HrR'))
                if r_doc_trail.ok:
                    rr_doc_trail = json.loads(r_doc_trail.content)
                    # con esto obtengo el link en el campo "link" lo tengo que descargar y unir al campo viafirma.XXXXX (os recuerdo que no hay campo porque se ha considerado no guardarlo


    def create_templates(self, thedict):
        '''Esta funcion actualiza las plantillas y crea las nuevas'''

        existe = self.env['viafirma.templates'].search([('code', '=', thedict["code"])])
        if not existe:
            viafirma_template_id = self.env['viafirma.templates'].create({
                'name': thedict["code"],
                'code': thedict["code"],
                'description': thedict["title"]
            })
            return viafirma_template_id

    def updated_templates(self):

        header = self.get_uploader_header()
        search_url = 'https://sandbox.viafirma.com/documents/api/v3/template/list/antonio.canovas@ingenieriacloud.com'
        response_template = requests.get(search_url, headers=header, auth=('dev_inelga','PnCDKj5HrR'))
        if response_template.ok:
            resu_templates = json.loads(response_template.content)
            for resu_template in resu_templates:
                self.create_templates(resu_template)

    def call_viafirma(self):
        ''' solo firma web y un solo firmante, la mas simple de todas, de momento selecciono todos los registros que tenga en el modelo viafirma y que haga el proceso
         de envio para cada uno de ellos, aunque no coge ningun valor de estos, ni emqail ni adjunto'''

        envios = self.env['viafirma'].search([('state', '=', 'DRAFT')])
        for envio in envios:
            header = self.get_uploader_header()
            search_url = 'https://sandbox.viafirma.com/documents/api/v3/messages/'
            datas = self.compose_call()
            response_firmweb = requests.post(search_url, datas=json.dumps(datas), headers=header, auth=('dev_inelga', 'PnCDKj5HrR'))
            if response_firmweb.ok:
                resp_firmweb = json.loads(response_firmweb.content)
                # normalmente devuelve solo un codigo pero puede ser que haya mas, ese código hay que almacenarlo en viafirma.status_id para su posterior consulta de estado
                self.env('viafirma').tracking_code = resps_firmweb