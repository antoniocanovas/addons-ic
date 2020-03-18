import logging
import pprint
import werkzeug
import json
from datetime import datetime
import swagger_client
from swagger_client.rest import ApiException

from odoo import http, _
from odoo.http import request


_logger = logging.getLogger(__name__)


class CorrectionPortal(http.Controller):
    @http.route(['/invoice/correction'], type='http', auth="user", website=True)
    def wallet_add_money(self, **post):
        print(self)
        #url_portal = "http://facturas.biyectiva.com/facturas/%s" % self.ocr_transaction_id.token

        #acquirers = request.env['payment.acquirer'].sudo().search([
        #    ('website_published', '=', True),
        #    ('is_wallet_acquirer', '=', True)])
        #values = dict()
        #values['form_acquirers'] = [acq for acq in acquirers if
        #                            acq.payment_flow == 'form' and
        #                            acq.view_template_id]
        #values = {
        #    'wallet_bal': request.env.user.partner_id.wallet_balance,
        #    'acquirers': acquirers,
        #    'form_acquirers': values['form_acquirers'],
        #}
        #return request.render("ocr_sync_invoce.redirect_correction_form", values)
        return request.render("ocr_sync_invoice.redirect_correction_form")