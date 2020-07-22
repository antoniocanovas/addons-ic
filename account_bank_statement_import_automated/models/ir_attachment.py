
import base64

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons.base.models.res_bank import sanitize_account_number

import logging
_logger = logging.getLogger(__name__)



class IrAttachmentBankStatement(models.Model):
    _inherit = 'ir.attachment'


    is_bank_statement = fields.Boolean(string='Is bank Statement', default=False)