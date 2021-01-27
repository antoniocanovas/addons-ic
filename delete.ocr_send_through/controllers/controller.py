
import logging

from odoo import http, _
from odoo.http import request
import requests
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CorrectionPortal(http.Controller):
    @http.route(['/invoice/correction'], type='http', auth="user", website=True)
    def correction_portal(self, **post):
        ## sustituir api_key de customer por company si ocr_delivery es negativo
        invoice = request.env['account.invoice'].sudo().search([('to_correct', '=', True)], limit=1)
        invoice.to_correct = False
        if request.env.user.company_id.ocr_delivery_company and invoice.customer_id:
            pc = request.env['partner.credentials'].sudo().search([
                ('partner_id', '=', invoice.customer_id.id)], limit=1)
            apikey = pc.client_api_key
        else:
            apikey = request.env.user.company_id.api_key

        values = dict()

        values = {
            'action': "http://facturas.biyectiva.com/facturas/%s" % invoice.ocr_transaction_id.token,
            'apikey': apikey,
            'invoice': invoice,
        }

        params = {'apikey': values['apikey']}
        r = requests.post(values['action'], params)

        if str(r) == "<Response [500]>":
            raise ValidationError(
                "Server Error, please contact with your administrator.")
        else:
            return request.render("ocr_transactions.redirect_correction_form", values)