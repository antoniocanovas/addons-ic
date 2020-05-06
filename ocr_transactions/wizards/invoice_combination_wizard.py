# Copyright

import base64
import codecs
from PIL import Image
import io
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class InvoiceCombination(models.TransientModel):
    _name = 'ocr.invoice.combination'
    _description = 'Invoice Combination'

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
        if self.ocr_transaction_id.next_token:
            ocr_transaction_id = self.env['ocr.transactions'].sudo().search([
                ('token', '=', self.ocr_transaction_id.next_token)
            ])
            if len(ocr_transaction_id) > 1:
                raise ValidationError("Error hay más de una transacción con el mismo Token")
            elif not ocr_transaction_id:
                raise ValidationError("No hay siguiente factura disponible")
            else:
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
    def combine_invoice_imgs(self, pages):
        widths, heights = zip(*(i.size for i in pages))
        total_width = max(widths)
        total_height = sum(heights)
        new_im = Image.new('RGB', (total_width, total_height))
        y = 0
        for img in pages:
            new_im.paste(img, (0, y))
            y += img.height
        try:
            new_im.save('/tmp/tmp_combined_img.jpg')
            return True
        except Exception as e:
            raise Warning(("Ha habido un problema al tratar la imagen, pruebe de nuevo: %s\n" % e))

    @api.multi
    def assign_next_token(self, original, combined):
        if combined.next_token:
            ocr_transaction_id = self.env['ocr.transactions'].sudo().search([
                ('token', '=', combined.next_token)
            ])
            if ocr_transaction_id.next_token:
                original.next_token = ocr_transaction_id.next_token

    @api.multi
    def combine_values(self, original, combined):
        if combined.value_ids:
            for value in combined.value_ids:
                value.ocr_transaction_id = original.id
                value.token = original.token

    @api.multi
    def invoice_combination(self):

        attachment = self.original_ocr_transaction_id.invoice_id.message_main_attachment_id
        attachment2 = self.ocr_transaction_id.invoice_id.message_main_attachment_id

        image_stream = io.BytesIO(codecs.decode(attachment.datas, 'base64'))
        image = Image.open(image_stream)
        image_stream2 = io.BytesIO(codecs.decode(attachment2.datas, 'base64'))
        image2 = Image.open(image_stream2)

        pages = [image, image2]
        combined = self.combine_invoice_imgs(pages)

        if combined:
            try:
                with open('/tmp/tmp_combined_img.jpg', "rb") as img_file:
                    img_file_encode = base64.b64encode(img_file.read())
            except Exception as e:
                raise Warning(("Ha habido un problema al tratar la imagen, pruebe de nuevo: %s\n" % e))

            attachment_id = self.env['ir.attachment'].sudo().create({
                'name': "Combined" + str(self.original_ocr_transaction_id.name) + "_" + str(
                    self.original_ocr_transaction_id.id),
                'type': 'binary',
                'datas': img_file_encode,
                'datas_fname': self.original_ocr_transaction_id.name,
                'store_fname': self.original_ocr_transaction_id.name,
                'res_model': 'account.invoice',
                'res_id': self.original_ocr_transaction_id.invoice_id.id,
                'mimetype': 'image/jpeg'
            })
            if attachment_id:
                self.original_ocr_transaction_id.invoice_id.message_post(body="Factura Combinada",
                                                                         attachment_ids=[attachment_id.id])
                self.original_ocr_transaction_id.invoice_id.message_main_attachment_id = [
                    (6, 0, [attachment_id.id])]

                self.assign_next_token(self.original_ocr_transaction_id, self.ocr_transaction_id)
                self.combine_values(self.original_ocr_transaction_id, self.ocr_transaction_id)

                self.ocr_transaction_id.invoice_id.unlink()

            else:
                raise Warning(("Ha habido un problema al tratar la imagen, pruebe de nuevo en unos instantes"))
