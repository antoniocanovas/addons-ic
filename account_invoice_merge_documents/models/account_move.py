import base64
from PyPDF2 import PdfFileMerger, PdfFileWriter, PdfFileReader
from odoo import fields, models, api
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
import io

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    document_ids = fields.Many2many(comodel_name='ir.attachment', column1='attachment_id', column2='move_id',
                                    copy=False,
                                    string='Documents')
    merge_report = fields.Boolean("Merge report", default=False)
    merged_document = fields.Binary('Merged Document')
    merged_error = fields.Text(string='Error')

    def get_merged_document(self):
        try:
            new_doc_pdf = io.BytesIO()
            pdf = self.env.ref('account.account_invoices').sudo()._render_qweb_pdf([self.id])[0]
            merger = PdfFileMerger(strict=False)
            merger.append(io.BytesIO(pdf), import_bookmarks=False)

            for doc in self.document_ids:
                merger.append(doc._full_path(doc.store_fname), import_bookmarks=False)

            merger.write(new_doc_pdf)
            self.merged_document = base64.encodebytes(new_doc_pdf.getvalue())
            merger.close()

        except Exception as e:
            self.merged_error = str(e)


