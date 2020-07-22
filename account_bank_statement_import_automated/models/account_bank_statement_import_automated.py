
import base64

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_bank import sanitize_account_number

import logging
_logger = logging.getLogger(__name__)



class AccountBankStatementAutomation(models.Model):
    _inherit = 'account.bank.statement'


    bank_statement_attachment_ids = fields.Many2many(comodel_name="ir.attachment",
                                      relation="m2m_ocr_attachments_rel",
                                      column1="m2m_id",
                                      column2="attachment_id",
                                      string="Bank Statements",
                                      domain=[('is_bank_statement', '=', True)],)

    @api.multi
    def automated_import_files(self):
        for bsa in self.bank_statement_attachment_ids:
            bank_statement = self.env['account.bank.statement.import'].create({
                'data_file': bsa.datas,
                'display_name': bsa.datas_fname,
                'filename': bsa.datas_fname,
            })
            bank_statement.import_file()

