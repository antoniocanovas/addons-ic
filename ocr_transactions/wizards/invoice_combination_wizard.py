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

    original_ocr_transaction_id = fields.Many2one('ocr.transactions', string='Factura')
    ocr_transaction_id = fields.Many2one('ocr.transactions', string='Factura')
    attachment_datas = fields.Binary(string='Documento', attachment=True)
    invoice_id_link = fields.Many2one('account.invoice', string='Enlace a Factura')

    @api.multi
    def show_invoice(self):
        self.ensure_one()
        if self.ocr_transaction_id.invoice_id:
            try:
                form_view_id = self.env.ref("ocr_transactions.ocr_account_invoice_form").id
            except Exception as e:
                form_view_id = False
            return {
                'type': 'ir.actions.act_window',
                'name': 'action_ocr_in_invoice',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'res_id': self.ocr_transaction_id.invoice_id.id,
                'views': [(form_view_id, 'form')],
                'target': 'current',
            }
        else:
            raise ValidationError("No hay Factura asociada")

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

                    attachment = False
                    for msg in ocr_transaction_id.invoice_id.message_ids:
                        if msg.body == "<p>created with OCR Documents</p>":
                            attachment = msg.attachment_ids[0].datas

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
                            'default_invoice_id_link': ocr_transaction_id.invoice_id.id,
                            'default_attachment_datas': attachment,
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
                                          " O está en estado erróneo")
                else:
                    view_id = self.env.ref('ocr_transactions.invoice_combination_view').id

                    attachment = False
                    for msg in ocr_transaction_id.invoice_id.message_ids:
                        if msg.body == "<p>created with OCR Documents</p>":
                            attachment = msg.attachment_ids[0].datas

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
                            'default_invoice_id_link': ocr_transaction_id.invoice_id.id,
                            'default_attachment_datas': attachment,
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
            raise ValidationError(("Ha habido un problema al tratar la imagen, pruebe de nuevo: %s\n" % e))

    @api.multi
    def assign_token(self, original, combined):
        if combined.next_token and combined.next_token == original.token:
            if combined.previus_token:
                original.previus_token = combined.previus_token
                ocr_transaction_id = self.env['ocr.transactions'].sudo().search([
                    ('token', '=', combined.previus_token)
                ])
                if ocr_transaction_id:
                    ocr_transaction_id.next_token = original.token
        elif combined.previus_token and combined.previus_token == original.token:
            if combined.next_token:
                original.next_token = combined.next_token
                ocr_transaction_id = self.env['ocr.transactions'].sudo().search([
                    ('token', '=', combined.next_token)
                ])
                if ocr_transaction_id:
                    ocr_transaction_id.previus_token = original.token

    @api.multi
    def combine_values(self, original, combined):
        if combined.value_ids:
            for value in combined.value_ids:
                value.ocr_transaction_id = original.id
                value.token = original.token

    @api.multi
    def invoice_combination(self):

        #check consecutive invoices
        original = self.original_ocr_transaction_id
        combined = self.ocr_transaction_id
        if original.next_token != combined.token and original.previus_token != combined.token:
            raise ValidationError(("Las facturas seleccionadas no son consecutivas"))

        attachment = False
        attachment2 = False
        for msg in original.invoice_id.message_ids:
            if msg.body == "<p>created with OCR Documents</p>":
                attachment = msg.attachment_ids[0].datas
        for msg in combined.invoice_id.message_ids:
            if msg.body == "<p>created with OCR Documents</p>":
                attachment2 = msg.attachment_ids[0].datas

        image_stream = io.BytesIO(codecs.decode(attachment, 'base64'))
        image = Image.open(image_stream)
        image_stream2 = io.BytesIO(codecs.decode(attachment2, 'base64'))
        image2 = Image.open(image_stream2)

        if original.previus_token == combined.token:
            #Reordenamos si van en orden inverso
            # Revisar asignación de tokens
            #t_combined = combined
            #combined = original
            #original = t_combined
            pages = [image2, image]
        else:
            pages = [image, image2]

        combined_img = self.combine_invoice_imgs(pages)

        if combined_img:
            try:
                with open('/tmp/tmp_combined_img.jpg', "rb") as img_file:
                    img_file_encode = base64.b64encode(img_file.read())
            except Exception as e:
                img_file_encode = False
                raise ValidationError(("Ha habido un problema al tratar la imagen, pruebe de nuevo: %s\n" % e))

            attachment_id = self.env['ir.attachment'].sudo().create({
                'name': "Combined" + str(original.name) + "_" + str(
                    original.id),
                'type': 'binary',
                'datas': img_file_encode,
                'datas_fname': original.name,
                'store_fname': original.name,
                'res_model': 'account.invoice',
                'res_id': original.invoice_id.id,
                'mimetype': 'image/jpeg'
            })
            if attachment_id:

                for msg in original.invoice_id.message_ids:
                    if msg.body == "<p>created with OCR Documents</p>":
                        for img in msg.attachment_ids:
                            img.unlink()
                    msg.unlink()

                original.invoice_id.message_post(body="created with OCR Documents",
                                                                         attachment_ids=[attachment_id.id])
                original.invoice_id.message_main_attachment_id = [
                    (6, 0, [attachment_id.id])]

                self.assign_token(original, combined)
                self.combine_values(original, combined)

                combined.invoice_id.unlink()

                #return vista de factura resultante
                #try:
                #    form_view_id = self.env.ref("my_module.my_form_view_external_id").id
                #except Exception as e:
                #    form_view_id = False
                #return {
                #    'type': 'ir.actions.act_window',
                #    'name': 'My Action Name',
                #    'view_type': 'form',
                #    'view_mode': 'form',
                #    'res_model': 'my.model',
                #    'res_id': ''
                #    'views': [(form_view_id, 'form')],
                #    'target': 'current',
                #}

            else:
                raise ValidationError(("Ha habido un problema al tratar la imagen, pruebe de nuevo en unos instantes"))
