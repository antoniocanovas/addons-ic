from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    ocr_transaction_id = fields.Many2one('ocr.transactions', string='OCR', readonly=True)
    customer_id = fields.Many2one('res.partner', readonly=True, string='Customer')

    @api.constrains('ocr_transaction_id')
    def check_customer_id(self):
        for invoice in self:
            if invoice.ocr_transaction_id:
                invoice.customer_id = invoice.ocr_transaction_id.ocr_upload_id.partner_id.id

    @api.multi
    def create_invoice_lines_from_ocr(self):
        for invoice in self:
            # Comprobamos que el partner tiene asignadas cuentas contables por defecto para crear las líneas de factura:
            if (not invoice.partner_id.ocr_sale_account_id.id) or (not invoice.partner_id.ocr_purchase_account_id.id):
                raise ValidationError(
                    'Asigne las cuentas contables por defecto para OCR en la ficha de esta empresa, antes de intentar crear las líneas de factura.')

            # Inicializando:
            base_iva21 = 0
            base_iva10 = 0
            base_iva4 = 0

            # Diccionario de impuestos para ventas:
            if invoice.type in ['out_invoice', 'out_refund']:
                cc = invoice.partner_id.ocr_sale_account_id.id
                cc_name = invoice.partner_id.ocr_sale_account_id.name
                taxiva21 = self.env['ocr.dictionary'].search([('name', '=', 'IVA21'), ('type', '=', 'out_invoice')]).tax_id
                taxiva10 = self.env['ocr.dictionary'].search([('name', '=', 'IVA10'), ('type', '=', 'out_invoice')]).tax_id
                taxiva4 = self.env['ocr.dictionary'].search([('name', '=', 'IVA4'), ('type', '=', 'out_invoice')]).tax_id
                taxiva0 = self.env['ocr.dictionary'].search([('name', '=', 'IVA0'), ('type', '=', 'out_invoice')]).tax_id
                # Diccionario de retenciones para ventas:

                taxret19 = self.env['ocr.dictionary'].search([('name', '=', 'IRPF19'), ('type', '=', 'out_invoice')]).tax_id
                taxret15 = self.env['ocr.dictionary'].search([('name', '=', 'IRPF15'), ('type', '=', 'out_invoice')]).tax_id
                taxret7 = self.env['ocr.dictionary'].search([('name', '=', 'IRPF7'), ('type', '=', 'out_invoice')]).tax_id
                taxret2 = self.env['ocr.dictionary'].search([('name', '=', 'IRPF2'), ('type', '=', 'out_invoice')]).tax_id

            # Diccionario de impuestos para compras:
            elif invoice.type in ['in_invoice', 'in_refund']:
                cc = invoice.partner_id.ocr_purchase_account_id.id
                cc_name = invoice.partner_id.ocr_purchase_account_id.name
                taxiva21 = self.env['ocr.dictionary'].search([('name', '=', 'IVA21'), ('type', '=', 'in_invoice')]).tax_id
                taxiva10 = self.env['ocr.dictionary'].search([('name', '=', 'IVA10'), ('type', '=', 'in_invoice')]).tax_id
                taxiva4 = self.env['ocr.dictionary'].search([('name', '=', 'IVA4'), ('type', '=', 'in_invoice')]).tax_id
                taxiva0 = self.env['ocr.dictionary'].search([('name', '=', 'IVA0'), ('type', '=', 'in_invoice')]).tax_id
                # Diccionario de retenciones para compras:
                taxret19 = self.env['ocr.dictionary'].search([('name', '=', 'IRPF19'), ('type', '=', 'in_invoice')]).tax_id
                taxret15 = self.env['ocr.dictionary'].search([('name', '=', 'IRPF15'), ('type', '=', 'in_invoice')]).tax_id
                taxret7 = self.env['ocr.dictionary'].search([('name', '=', 'IRPF7'), ('type', '=', 'in_invoice')]).tax_id
                taxret2 = self.env['ocr.dictionary'].search([('name', '=', 'IRPF2'), ('type', '=', 'in_invoice')]).tax_id

            # Valores:
            subtotal = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'SubTotal')])
            total = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'TOTAL')])
            iva21 = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'IVA21')])
            iva10 = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'IVA10')])
            iva4 = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'IVA4')])
            iva0 = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'IVA0')])
            ret19 = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'IRPF19')])
            ret15 = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'IRPF15')])
            ret7 = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'IRPF7')])
            ret2 = self.env['ocr.values'].search(
                [('ocr_transaction_id', '=', invoice.ocr_transaction_id.id), ('name', '=', 'IRPF2')])

            # Cálculo de bases imponibles POR IVA:
            if iva21.id:  base_iva21 = float(iva21.value) * 100 / 21
            if iva10.id:  base_iva10 = float(iva10.value) * 100 / 10
            if iva4.id:   base_iva4 = float(iva4.value) * 100 / 4

            # Cálculo de bases imponibles POR RETENCIONES:
            if ret19.id:  base_ret19 = float(ret19.value) * 100 / 19
            if ret15.id:  base_ret15 = float(ret15.value) * 100 / 15
            if ret7.id:   base_ret7 = float(ret7.value) * 100 / 7
            if ret2.id:   base_ret2 = float(ret2.value) * 100 / 2

            if subtotal.id:  neto = float(subtotal.value)

            # Cálculo de retenciones al 19%:
            if (ret19.id) and (base_ret19 > 0):
                if (base_iva21 >= base_ret19):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva21.id, taxret19.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret19,
                         'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva21 -= base_ret19
                    neto -= base_ret19
                    base_ret19 = 0

                # Lo mismo por si es iva10
                if (base_iva10 >= base_ret19) and (base_ret19 > 0):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva10.id, taxret19.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret19,
                         'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva10 -= base_ret19
                    neto -= base_ret19
                    base_ret19 = 0
                # Lo mismo por si es iva4 para 19
                if (base_iva4 >= base_ret19) and (base_ret19 > 0):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva4.id, taxret19.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret19,
                         'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva4 -= base_ret19
                    neto -= base_ret19

            # Cálculo de retenciones al 15%:
            if (ret15.id) and (base_ret15 > 0):
                if (base_iva21 >= base_ret15):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva21.id, taxret15.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret15,
                         'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva21 -= base_ret15
                    neto -= base_ret15
                    base_ret15 = 0
                # Lo mismo por si es iva10
                if (base_iva10 >= base_ret15) and (base_ret15 > 0):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva10.id, taxret15.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret15,
                         'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva10 -= base_ret15
                    neto -= base_ret15
                    base_ret15 = 0
                # Lo mismo por si es iva4 para 19
                if (base_iva4 >= base_ret15) and (base_ret15 > 0):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva4.id, taxret15.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret15,
                         'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva4 -= base_ret15
                    neto -= base_ret15

            # Cálculo de retenciones al 7%:
            if (ret7.id) and (base_ret7 > 0):
                if (base_iva21 >= base_ret7):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva21.id, taxret7.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret7, 'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva21 -= base_ret7
                    neto -= base_ret7
                    base_ret7 = 0
                # Lo mismo por si es iva10
                if (base_iva10 >= base_ret7) and (base_ret7 > 0):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva10.id, taxret7.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret7, 'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva10 -= base_ret7
                    neto -= base_ret7
                    base_ret7 = 0
                # Lo mismo por si es iva4 para 19
                if (base_iva4 >= base_ret7) and (base_ret7 > 0):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva4.id, taxret7.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret7, 'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva4 -= base_ret7
                    neto -= base_ret7

            # Cálculo de retenciones al 2%:
            if (ret2.id) and (base_ret2 > 0):
                if (base_iva21 >= base_ret2):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva21.id, taxret2.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret2, 'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva21 -= base_ret2
                    neto -= base_ret2
                    base_ret2 = 0
                # Lo mismo por si es iva10
                if (base_iva10 >= base_ret2) and (base_ret2 > 0):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva10.id, taxret2.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret2, 'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva10 -= base_ret2
                    neto -= base_ret2
                    base_ret2 = 0
                # Lo mismo por si es iva4 para 19
                if (base_iva4 >= base_ret2) and (base_ret2 > 0):
                    # crear línea con base de retención y dejar base restante para otra línea:
                    impuestos = [taxiva4.id, taxret2.id]
                    nuevalin = self.env['account.invoice.line'].create(
                        {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_ret2, 'account_id': cc})
                    nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                    base_iva4 -= base_ret2
                    neto -= base_ret2

            # Líneas de impuestos estándar, sin retención:
            if (taxiva21.id) and (base_iva21 > 0):
                impuestos = [taxiva21.id]
                nuevalin = self.env['account.invoice.line'].create(
                    {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_iva21, 'account_id': cc})
                nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                neto -= base_iva21
            if (taxiva10.id) and (base_iva10 > 0):
                impuestos = [taxiva10.id]
                nuevalin = self.env['account.invoice.line'].create(
                    {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_iva10, 'account_id': cc})
                nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                neto -= base_iva10
            if (taxiva4.id) and (base_iva4 > 0):
                impuestos = [taxiva4.id]
                nuevalin = self.env['account.invoice.line'].create(
                    {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': base_iva4, 'account_id': cc})
                nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]
                neto -= base_iva4

            # Caso de línea sin impuestos y sin detectar IVA0%:
            if (subtotal.id) and (neto > 0):
                impuestos = [taxiva0.id]
                nuevalin = self.env['account.invoice.line'].create(
                    {'invoice_id': invoice.id, 'name': cc_name, 'quantity': 1, 'price_unit': neto, 'account_id': cc})
                nuevalin['invoice_line_tax_ids'] = [(6, 0, impuestos)]

            # Reculcalate Taxes
            if invoice.invoice_line_ids.ids:
                invoice.compute_taxes()


