
import logging

from odoo import http, _
from odoo.http import request

_logger = logging.getLogger(__name__)


class CorrectionPortal(http.Controller):
    @http.route(['/invoice/correction'], type='http', auth="user", website=True)
    def correction_portal(self, **post):

        invoice = request.env['account.invoice'].sudo().search([('to_correct', '=', True)], limit=1)
        invoice.to_correct = False

        values = dict()

        values = {
            'action': "http://facturas.biyectiva.com/facturas/%s" % invoice.ocr_transaction_id.token,
            'apikey': request.env.user.company_id.api_key,
            'invoice': invoice,
        }
        return request.render("ocr_transactions.redirect_correction_form", values)