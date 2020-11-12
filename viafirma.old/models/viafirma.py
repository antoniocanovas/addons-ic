# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

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

