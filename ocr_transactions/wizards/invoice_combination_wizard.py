# Copyright



from odoo import fields, models, api
from odoo.exceptions import ValidationError

import base64
from PIL import Image




class InvoiceCombination(models.TransientModel):
    _name = 'ocr.invoice.combination'

    ocr_transaction_ids = fields.Many2one('ocr.transactions', string='Factura')
    invoice_id = fields.Many2one('ir.attachment', string='Factura')

    original_ocr_transaction_id = fields.Many2one('ocr.transactions', string='Factura')
    ocr_transaction_id = fields.Many2one('ocr.transactions', string='Factura')
    attachment_datas = fields.Binary(string='Factura', attachment=True)

    @api.multi
    def show_previus_invoice(self):
        if self.ocr_transaction_id.previus_token:
            ocr_transaction_id = self.env['ocr.transactions'].sudo().search([
                ('token', '=', self.ocr_transaction_id.previus_token)
            ])
            if len(ocr_transaction_id) > 1:
                raise ValidationError("Error hay más de una transacción con el mismo Token")
            elif not ocr_transaction_id:
                raise ValidationError("No hay factura anterior disponible")
            else:
                print(ocr_transaction_id.name)
                if not ocr_transaction_id.invoice_id:
                    raise ValidationError("La factura anterior aún no ha sido procesada,"
                                          " Pruebe más tarde")
                else:
                    view_id = self.env.ref('ocr_transactions.invoice_combination_view').id

                    return {
                        'name': "Factura Anterior",
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'ocr.invoice.combination',
                        'view_id': view_id,
                        'target': 'new',
                        'context': {
                            'default_ocr_transaction_id': ocr_transaction_id.id,
                            'default_attachment_datas': ocr_transaction_id.invoice_id.message_main_attachment_id.datas,
                            'default_original_ocr_transaction_id': self.original_ocr_transaction_id.id,
                        }
                    }
        else:
            raise ValidationError("No hay factura anterior disponible")

    @api.multi
    def show_next_invoice(self):
        print("DEBUGG")
        print(self.ocr_transaction_id.next_token)
        if self.ocr_transaction_id.next_token:
            print(self.ocr_transaction_id.next_token)
            ocr_transaction_id = self.env['ocr.transactions'].sudo().search([
                ('token', '=', self.ocr_transaction_id.next_token)
            ])
            if len(ocr_transaction_id) > 1:
                raise ValidationError("Error hay más de una transacción con el mismo Token")
            elif not ocr_transaction_id:
                raise ValidationError("No hay siguiente factura disponible")
            else:
                print(ocr_transaction_id.name)
                if not ocr_transaction_id.invoice_id:
                    raise ValidationError("La siguiente factura aún no ha sido procesada,"
                                          " Pruebe más tarde")
                else:
                    view_id = self.env.ref('ocr_transactions.invoice_combination_view').id

                    return {
                        'name': "Siguiente Factura",
                        'type': 'ir.actions.act_window',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'ocr.invoice.combination',
                        'view_id': view_id,
                        'target': 'new',
                        'context': {
                            'default_ocr_transaction_id': ocr_transaction_id.id,
                            'default_attachment_datas': ocr_transaction_id.invoice_id.message_main_attachment_id.datas,
                            'default_original_ocr_transaction_id': self.original_ocr_transaction_id.id,
                        }
                    }
        else:
            raise ValidationError("No hay siguiente factura disponible")

    @api.multi
    def invoice_combination(self):

        print("MERGE")

        attachment = self.original_ocr_transaction_id.invoice_id.message_main_attachment_id
        attachment2 = self.ocr_transaction_id.invoice_id.message_main_attachment_id
        with open('/tmp/c_test.jpg', 'wb') as f:
            f.write(base64.b64decode(attachment.datas))
        with open('/tmp/c_test2.jpg', 'wb') as f2:
            f2.write(base64.b64decode(attachment2.datas))


        #decoded_attachment = base64.b64decode(attachment.datas)
        decoded_attachment = Image.open('/tmp/c_test.jpg')
        decoded_attachment2 = Image.open('/tmp/c_test2.jpg')
        img = decoded_attachment.convert('RGB')
        img2 = decoded_attachment2.convert('RGB')
        #img.save(r'/tmp/c_test.pdf')
        #with open('/tmp/c_test.pdf', 'wb') as f:
        #    f.write(base64.b64decode(attachment.datas))
        #    f.close()
        #with open('/tmp/c_test2.pdf', 'wb') as f2:
        #    f2.write(base64.b64decode(self.invoice_id.message_main_attachment_id.datas))
        #    f.close()
        print('pdf')
        pdfs = [
            img,
            img2,
        ]
        im = Image.new("RGB", (200, 30), "#ddd")
        im.save('/tmp/NEW.PDF', save_all=True, append_images=pdfs)

        print("img save")


        attachment_id = self.env['ir.attachment'].sudo().create({
            'name': self.original_ocr_transaction_id.invoice_id.name,
            'type': 'binary',
            'datas': im,
            'datas_fname': self.original_ocr_transaction_id.name,
            'store_fname': self.original_ocr_transaction_id.name,
            'res_model': 'account.invoice',
            'res_id': self.original_ocr_transaction_id.invoice_id.id,
            'mimetype': 'application/pdf'
        })

        self.original_ocr_transaction_id.invoice_id.message_main_attachment_id = [(4, attachment_id.id)]