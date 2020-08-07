
import base64

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_bank import sanitize_account_number

import logging
_logger = logging.getLogger(__name__)

STATE = [
    ('draft', 'Draft'),
    ('error', 'Error'),
    ('completed', 'Completed'),
]


class AccountBankStatementAutomation(models.Model):
    _name = 'account.bank.statement.automated'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Importación Automática de Estractos'


    name = fields.Char('Name')
    journal_id = fields.Many2one('account.journal', domain=[('type', '=', 'bank')] )
    state = fields.Selection(
        selection=STATE, string="State", default='draft', track_visibility='onchange'
    )
    #bank_statement_import_ids = fields.One2many('bank.statement.import', 'ocr_upload_id')
    bank_statement_attachment_ids = fields.Many2many(comodel_name="ir.attachment",
                                      relation="m2m_ocr_attachments_rel",
                                      column1="m2m_id",
                                      column2="attachment_id",
                                      string="Bank Statements",
                                      #domain=[('is_bank_statement', '=', True)],
                                    )

    @api.multi
    def automated_import_files(self):
        self = self.with_context(journal_id=self.journal_id.id)
        for bsa in self.bank_statement_attachment_ids:
            print("Importando")
            bank_statement = self.env['account.bank.statement.import'].create({
                'data_file': bsa.datas,
                'display_name': bsa.datas_fname,
                'filename': bsa.datas_fname,
            })

            bank_statement.import_file()
            print("DONE")

