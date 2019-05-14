# -*- coding: utf-8 -*-

import requests
import base64
import logging
import urllib
import json
import swagger_client
from swagger_client.rest import ApiException
from odoo import models, fields, api
from odoo.tools import config
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.addons import decimal_precision as dp
from odoo.tools.float_utils import float_compare
from odoo import exceptions
from odoo import http

_logger = logging.getLogger(__name__)


class x_marketpayacquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('marketpay', 'Marketpay')])
    x_marketpay_key = fields.Char('Key', required=True)
    x_marketpay_secret = fields.Char('secret', required=True)
    x_marketpay_domain = fields.Char('domain', required=True)
    #x_marketpay_token_url = fields.Char('Token', required=True)
    x_marketpay_url_ok = fields.Char('url_ok', required=True)
    x_marketpay_url_ko = fields.Char('url_ko', required=True)
    x_marketpay_fee = fields.Integer('Comisión', required=True)
    x_marketpay_currency = fields.Char('Currency', default='978',
                                  required_if_provider='marketpay')
    send_quotation = fields.Boolean('Send quotation', default=True)

    @api.model
    def _get_website_callback_url(self):
        """For force a callback url from Redsys distinct to base url website,
         only apply to a Redsys response.
        """
        get_param = self.env['ir.config_parameter'].sudo().get_param
        return get_param(
            'payment_marketpay.callback_url')

    def _get_marketpay_urls(self, environment):
        """ Redsys URLs
        """
        if environment == 'prod':
            return {
                'marketpay_form_url':
                    'https://sis.redsys.es/sis/realizarPago/',
            }
        else:
            return {
                'marketpay_form_url':
                    'https://sis-t.redsys.es:25443/sis/realizarPago/',
            }



    @api.model
    def _get_website_url(self):
        """
        For a single website setting the domain website name is not accesible
        for the user, by default is localhost so the system get domain from
        system parameters instead of domain of website record.
        """
        if config['test_enable']:
            return self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')

        domain = http.request.website.domain
        if domain and domain != 'localhost':
            base_url = '%s://%s' % (
                http.request.httprequest.environ['wsgi.url_scheme'],
                http.request.website.domain
            )
        else:
            base_url = self.env['ir.config_parameter'].sudo().get_param(
                'web.base.url')
        return base_url or ''


    @api.multi
    def marketpay_form_generate_values(self, values):
        self.ensure_one()
        marketpay_values = dict(values)

        base_url = self._get_website_url()
        callback_url = self._get_website_callback_url()

        ## valores de marketpay para el usuario que hace la Operación ###
        marketpaydata = values['partner']

        # Configuración CLiente
        encoded = self.x_marketpay_key + ":" + self.x_marketpay_secret

        token_url = 'https://api-sandbox.marketpay.io/v2.01/oauth/token'

        key = 'Basic %s' % base64.b64encode(encoded.encode('ascii')).decode('ascii')
        data = {'grant_type': 'client_credentials'}
        headers = {'Authorization': key, 'Content-Type': 'application/x-www-form-urlencoded'}

        r = requests.post(token_url, data=data, headers=headers)

        rs = r.content.decode()
        response = json.loads(rs)
        token = response['access_token']

        # Configuración default de Swagger
        config = swagger_client.Configuration()
        config.host = self.x_marketpay_domain
        config.access_token = token
        client = swagger_client.ApiClient(configuration=config)
        api_instance = swagger_client.Configuration.set_default(config)

        ############ trae los valores del partner ############

        # merchant_parameters = self._prepare_merchant_parameters(values)

        # walletid = marketpaydata.x_marketpaywallet_id
        # userid = marketpaydata.x_marketpayuser_id

        walletid = "9347379"
        userid = "9347382"

        currency = "EUR"
        #amount = str(int(round(values['amount'] * 100)))
        amount = 1000
        amountfee = self.x_marketpay_fee
        #success_url = self.x_marketpay_url_ok
        #cancel_url = self.x_marketpay_url_ko
        success_url = '%s/payment/redsys/result/redsys_result_ok' % base_url
        #success_url = ('%s/payment/redsys/return' % (callback_url or base_url))[:250]
        cancel_url = '%s/payment/redsys/result/redsys_result_ko' % base_url
        apiPayin = swagger_client.PayInsRedsysApi()

        fees = swagger_client.Money(amount=amountfee, currency=currency)
        debited = swagger_client.Money(amount=amount, currency=currency)
        redsys_pay = swagger_client.RedsysPayByWebPost(credited_wallet_id=walletid, debited_funds=debited, fees=fees,
                                                       success_url=success_url, cancel_url=cancel_url)
        x_webhook = 'http://5.134.116.159:8069/payment/marketpay/result/'

        try:

            api_response = apiPayin.pay_ins_redsys_redsys_post_payment_by_web(x_webhook=x_webhook, redsys_pay_in=redsys_pay)


        except ApiException as e:
            print("Exception when calling UsersApi->users_post: %s\n" % e)

        pay_in_id = api_response.pay_in_id
        print(api_response)
        marketpay_values.update({

            'Ds_MerchantParameters': api_response.ds_merchant_parameters,
            'Ds_SignatureVersion': api_response.ds_signature_version,
            'Ds_Signature': api_response.ds_signature,

        })

        return marketpay_values



    @api.multi
    def marketpay_get_form_action_url(self):
        return self._get_marketpay_urls(self.environment)['marketpay_form_url']







class TxMarketpay(models.Model):
    _inherit = 'payment.transaction'

    marketpay_txnid = fields.Char('Transaction ID')

    def merchant_params_json2dict(self, data):
        parameters = data.get('Ds_MerchantParameters', '')
        return json.loads(base64.b64decode(parameters).decode())

    @api.model
    def _marketpay_form_get_tx_from_data(self, data):
        """ Given a data dict coming from redsys, verify it and
        find the related transaction record. """

        print("form get ###################")

        parameters = data.get('Ds_MerchantParameters', '')
        parameters_dic = json.loads(base64.b64decode(parameters).decode())
        reference = urllib.parse.unquote(parameters_dic.get('Ds_Order', ''))
        pay_id = parameters_dic.get('Ds_AuthorisationCode')
        shasign = data.get(
            'Ds_Signature', '').replace('_', '/').replace('-', '+')
        test_env = http.request.session.get('test_enable', False)
        if not reference or not pay_id or not shasign:
            error_msg = 'Redsys: received data with missing reference' \
                        ' (%s) or pay_id (%s) or shashign (%s)' % (reference,
                                                                   pay_id, shasign)
            if not test_env:
                _logger.info(error_msg)
                raise ValidationError(error_msg)
            # For tests
            http.OpenERPSession.tx_error = True
        tx = self.search([('reference', '=', reference)])
        if not tx or len(tx) > 1:
            error_msg = 'Redsys: received data for reference %s' % (reference)
            if not tx:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            if not test_env:
                _logger.info(error_msg)
                raise ValidationError(error_msg)
            # For tests
            http.OpenERPSession.tx_error = True
        if tx and not test_env:
            # verify shasign
            shasign_check = tx.acquirer_id.sign_parameters(
                tx.acquirer_id.marketpay_secret_key, parameters)
            if shasign_check != shasign:
                error_msg = (
                        'Redsys: invalid shasign, received %s, computed %s, '
                        'for data %s' % (shasign, shasign_check, data)
                )
                _logger.info(error_msg)
                raise ValidationError(error_msg)
        return tx

    @api.model
    def _get_marketpay_state(self, status_code):

        print("STATE ###################")

        if 0 <= status_code <= 100:
            return "done"
        elif status_code <= 203:
            return "pending"
        elif 912 <= status_code <= 9912:
            return "cancel"
        else:
            return "error"

    def _marketpay_form_validate(self, data):

        print("Validate ###################")

        params = self.merchant_params_json2dict(data)
        status_code = int(params.get('Ds_Response', '29999'))
        state = self._get_marketpay_state(status_code)
        vals = {
            'state': state,
            'marketpay_txnid': params.get('Ds_AuthorisationCode'),
        }
        state_message = ""
        if state == 'done':
            vals['state_message'] = _('Ok: %s') % params.get('Ds_Response')
        elif state == 'pending':  # 'Payment error: code: %s.'
            state_message = _('Error: %s (%s)')
        elif state == 'cancel':  # 'Payment error: bank unavailable.'
            state_message = _('Bank Error: %s (%s)')
        else:
            state_message = _('Redsys: feedback error %s (%s)')
        if state_message:
            vals['state_message'] = state_message % (
                params.get('Ds_Response'), params.get('Ds_ErrorCode'),
            )
            if state == 'error':
                _logger.warning(vals['state_message'])
        self.write(vals)
        return state != 'error'



    @api.model
    def form_feedback(self, data, acquirer_name):

        print("form feedback ###################")

        res = super(TxMarketpay, self).form_feedback(data, acquirer_name)
        try:
            tx_find_method_name = '_%s_form_get_tx_from_data' % acquirer_name
            if hasattr(self, tx_find_method_name):
                tx = getattr(self, tx_find_method_name)(data)
            _logger.info(
                '<%s> transaction processed: tx ref:%s, tx amount: %s',
                acquirer_name, tx.reference if tx else 'n/a',
                tx.amount if tx else 'n/a')

        except Exception:
            _logger.exception(
                'Fail to confirm the order or send the confirmation email%s',
                tx and ' for the transaction %s' % tx.reference or '')
        return res
