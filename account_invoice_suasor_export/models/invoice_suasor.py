# Copyright
# License LGPL-3.0 or later (http =//www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

import logging

_logger = logging.getLogger(__name__)


class SuasorInvoice(models.Model):
    _name = 'suasor.invoice'
    _description = 'Export to Suasor'

    invoice_id = fields.Many2one(
            'account.invoice',
        )

    name = fields.Char('Name')
    fecha_emision = fields.Date('fecha_emision')
    tipo_factura = fields.Char('tipo_factura')
    n_documento = fields.Char('n_documento')
    total_factura = fields.Char('total_factura')
    #cuenta = fields.Char('cuenta')
    nif = fields.Char('nif')
    nombre = fields.Char('nombre')
    provincia = fields.Char('Provincia')
    pais = fields.Char('pais')
    terminos_pago = fields.Char('terminos_pago')
    grupo = fields.Char('Grupo')

    base_iva1 = fields.Char('base_iva1')
    iva_percent1 = fields.Char('iva_percent1')
    iva_tax1 = fields.Char('iva_tax1')
    imp_irpf1 = fields.Char('imp_irpf1')
    irpf_percent1 = fields.Char('irpf_percent1')
    imp_recargo1 = fields.Char('imp_recargo1')
    req_percent1 = fields.Char('req_percent1')
    servicios1 = fields.Char('servicios1')
    bien_inversion1 = fields.Char('bien_inversion1')
    cta_contrapartida1 = fields.Char('cta_contrapartida1')
    base_iva2 = fields.Char('base_iva2')
    iva_percent2 = fields.Char('iva_percent2')
    iva_tax2 = fields.Char('iva_tax2')
    imp_irpf2 = fields.Char('imp_irpf2')
    irpf_percent2 = fields.Char('irpf_percent2')
    imp_recargo2 = fields.Char('imp_recargo2')
    req_percent2 = fields.Char('req_percent2')
    servicios2 = fields.Char('servicios2')
    bien_inversion2 = fields.Char('bien_inversion2')
    cta_contrapartida2 = fields.Char('cta_contrapartida2')
    base_iva3 = fields.Char('base_iva3')
    iva_percent3 = fields.Char('iva_percent3')
    iva_tax3 = fields.Char('iva_tax3')
    imp_irpf3 = fields.Char('imp_irpf3')
    irpf_percent3 = fields.Char('irpf_percent3')
    imp_recargo3 = fields.Char('imp_recargo3')
    req_percent3 = fields.Char('req_percent3')
    servicios3 = fields.Char('servicios3')
    bien_inversion3 = fields.Char('bien_inversion3')
    cta_contrapartida3 = fields.Char('cta_contrapartida3')