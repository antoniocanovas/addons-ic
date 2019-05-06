# -*- coding: utf-8 -*-
from odoo import http

import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class MarketpayController(http.Controller):
    _return_url = '/payment/marketpay/return'
    _cancel_url = '/payment/marketpay/cancel'
    _exception_url = '/payment/marketpay/error'
    _reject_url = '/payment/marketpay/reject'

    @http.route([
        '/payment/marketpay/return',
        '/payment/marketpay/cancel',
        '/payment/marketpay/error',
        '/payment/marketpay/reject',
    ], type='http', auth='none', csrf=False)
    def marketpay_return(self, **post):
        """ marketpay."""
        _logger.info('Marketpay: entering form_feedback with post data %s',
                     pprint.pformat(post))
        if post:
            request.env['payment.transaction'].sudo().form_feedback(
                post, 'marketpay')
        return_url = post.pop('return_url', '')
        if not return_url:
            return_url = '/shop'
        return werkzeug.utils.redirect(return_url)

    @http.route(
        ['/payment/marketpay/result/<page>'], type='http', auth='public',
        methods=['GET'], website=True)
    def marketpay_result(self, page, **vals):
        try:
            sale_order_id = request.session.get('sale_last_order_id')
            sale_obj = request.env['sale.order']
            order = sale_obj.sudo().browse(sale_order_id)
            res = {
                'order': order,
            }
            return request.render('payment_marketpay.%s' % str(page), res)
        except Exception:
            return request.render('website.404')