# © 2016-2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
from odoo.http import request

_logger = logging.getLogger(__name__)

try:
    from Crypto.Cipher import DES3
except ImportError:
    _logger.info("Missing dependency (pycryptodome). See README.")


class AcquirerRedsys(models.Model):
    _inherit = 'payment.acquirer'

    def _get_redsys_urls(self, environment):
        """ Redsys URLs
        """
        if environment == 'prod':
            return {
                'redsys_form_url':
                'https://sis.redsys.es/sis/realizarPago/',
            }
        else:
            return {
                'redsys_form_url':
                'https://sis-t.redsys.es:25443/sis/realizarPago/',
            }

    provider = fields.Selection(selection_add=[('redsys', 'Redsys')])
    x_marketpay_key = fields.Char('Key', required=True)
    x_marketpay_secret = fields.Char('secret', required=True)
    x_marketpay_domain = fields.Char('domain', required=True)
    # x_marketpay_token_url = fields.Char('Token', required=True)
    x_marketpay_url_ok = fields.Char('url_ok', required=True)
    x_marketpay_url_ko = fields.Char('url_ko', required=True)
    x_marketpay_fee = fields.Integer('Comisión', required=True)
    x_marketpay_currency = fields.Char('Currency', default='978',
                                       required_if_provider='marketpay')
    send_quotation = fields.Boolean('Send quotation', default=True)



    @api.constrains('redsys_percent_partial')
    def check_redsys_percent_partial(self):
        if (self.redsys_percent_partial < 0 or
                self.redsys_percent_partial > 100):
            raise exceptions.Warning(
                _('Partial payment percent must be between 0 and 100'))

    @api.model
    def _get_website_callback_url(self):
        """For force a callback url from Redsys distinct to base url website,
         only apply to a Redsys response.
        """
        get_param = self.env['ir.config_parameter'].sudo().get_param
        return get_param(
            'payment_market_redsys.callback_url')

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

    def _prepare_merchant_parameters(self, tx_values):
        # Check multi-website
        base_url = self._get_website_url()
        callback_url = self._get_website_callback_url()
        if self.redsys_percent_partial > 0:
            amount = tx_values['amount']
            tx_values['amount'] = amount - (
                amount * self.redsys_percent_partial / 100)
        values = {
            'Ds_Sermepa_Url': (
                self._get_redsys_urls(self.environment)[
                    'redsys_form_url']),
            'Ds_Merchant_Amount': str(int(round(tx_values['amount'] * 100))),
            'Ds_Merchant_Currency': self.redsys_currency or '978',
            'Ds_Merchant_Order': (
                tx_values['reference'] and tx_values['reference'][-12:] or
                False),
            'Ds_Merchant_MerchantCode': (
                self.redsys_merchant_code and
                self.redsys_merchant_code[:9]),
            'Ds_Merchant_Terminal': self.redsys_terminal or '1',
            'Ds_Merchant_TransactionType': (
                self.redsys_transaction_type or '0'),
            'Ds_Merchant_Titular': (
                self.redsys_merchant_titular[:60] and
                self.redsys_merchant_titular[:60]),
            'Ds_Merchant_MerchantName': (
                self.redsys_merchant_name and
                self.redsys_merchant_name[:25]),
            'Ds_Merchant_MerchantUrl': (
                '%s/payment/redsys/return' % (callback_url or base_url))[:250],
            'Ds_Merchant_MerchantData': self.redsys_merchant_data or '',
            'Ds_Merchant_ProductDescription': (
                self._product_description(tx_values['reference']) or
                self.redsys_merchant_description and
                self.redsys_merchant_description[:125]),
            'Ds_Merchant_ConsumerLanguage': (
                self.redsys_merchant_lang or '001'),
            'Ds_Merchant_UrlOk':
            '%s/payment/redsys/result/redsys_result_ok' % base_url,
            'Ds_Merchant_UrlKo':
            '%s/payment/redsys/result/redsys_result_ko' % base_url,
            'Ds_Merchant_Paymethods': self.redsys_pay_method or 'T',
        }
        return self._url_encode64(json.dumps(values))

    def _url_encode64(self, data):
        data = base64.b64encode(data.encode())
        return data

    def _url_decode64(self, data):
        return json.loads(base64.b64decode(data).decode())

    def sign_parameters(self, secret_key, params64):
        params_dic = self._url_decode64(params64)
        if 'Ds_Merchant_Order' in params_dic:
            order = str(params_dic['Ds_Merchant_Order'])
        else:
            order = str(
                urllib.parse.unquote(params_dic.get('Ds_Order', 'Not found')))
        cipher = DES3.new(
            key=base64.b64decode(secret_key),
            mode=DES3.MODE_CBC,
            IV=b'\0\0\0\0\0\0\0\0')
        diff_block = len(order) % 8
        zeros = diff_block and (b'\0' * (8 - diff_block)) or b''
        key = cipher.encrypt(str.encode(order + zeros.decode()))
        if isinstance(params64, str):
            params64 = params64.encode()
        dig = hmac.new(
            key=key,
            msg=params64,
            digestmod=hashlib.sha256).digest()
        return base64.b64encode(dig).decode()

    @api.multi
    def redsys_form_generate_values(self, values):
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
        amount = str(int(round(values['amount'] * 100)))
        #amount = 1000
        amountfee = self.x_marketpay_fee

        #success_url = '%s/payment/redsys/result/redsys_result_ok' % base_url
        #success_url = ('%s/payment/redsys/return' % (callback_url or base_url))[:250]
        success_url = '%s/wallet/add/money/transaction' % base_url
        cancel_url = '%s/payment/redsys/result/redsys_result_ko' % base_url

        apiPayin = swagger_client.PayInsRedsysApi()

        fees = swagger_client.Money(amount=amountfee, currency=currency)
        debited = swagger_client.Money(amount=amount, currency=currency)
        redsys_pay = swagger_client.RedsysPayByWebPost(credited_wallet_id=walletid, debited_funds=debited, fees=fees,
                                                       success_url=success_url, cancel_url=cancel_url)
        #x_webhook = ('%s/payment/redsys/return' % (callback_url or base_url))[:250]
        #print(x_webhook)
        try:

            api_response = apiPayin.pay_ins_redsys_redsys_post_payment_by_web(redsys_pay_in=redsys_pay)


        except ApiException as e:
            print("Exception when calling UsersApi->users_post: %s\n" % e)


        pay_in_id = api_response.pay_in_id

        print(api_response)

        PT = request.env['payment.transaction'].sudo()
        tx = PT.search([
            ('is_wallet_transaction', '=', True), ('wallet_type', '=', 'credit'),
            ('partner_id', '=', marketpaydata.id), ('state', '=', 'draft')], limit=1)


        tx.marketpay_txnid = pay_in_id

        print(tx)

        marketpay_values.update({

            'Ds_MerchantParameters': api_response.ds_merchant_parameters,
            'Ds_SignatureVersion': api_response.ds_signature_version,
            'Ds_Signature': api_response.ds_signature,


        })

        return marketpay_values


    @api.multi
    def redsys_get_form_action_url(self):
        return self._get_redsys_urls(self.environment)['redsys_form_url']

    def _product_description(self, order_ref):
        sale_order = self.env['sale.order'].search([('name', '=', order_ref)])
        res = ''
        if sale_order:
            description = '|'.join(x.name for x in sale_order.order_line)
            res = description[:125]
        return res


class TxRedsys(models.Model):
    _inherit = 'payment.transaction'

    # Redsys status
    _redsys_valid_tx_status = list(range(0, 100))
    _redsys_pending_tx_status = list(range(101, 203))
    _redsys_cancel_tx_status = [912, 9912]
    _redsys_error_tx_status = list(range(9064, 9095))

    marketpay_txnid = fields.Char('Marketpay ID')


    def merchant_params_json2dict(self, data):
        parameters = data.get('Ds_MerchantParameters', '')
        return json.loads(base64.b64decode(parameters).decode())

    # --------------------------------------------------
    # FORM RELATED METHODS
    # --------------------------------------------------

    @api.model
    def _redsys_form_get_tx_from_data(self, data):
        """ Given a data dict coming from redsys, verify it and
        find the related transaction record. """

        print("################RESULT FORM #####################")

        pedido = data['order']
        reference = pedido.transaction_ids[0].reference
        print(reference)
        tx = self.search([('reference', '=', reference)])
        print(tx)


        #parameters = data.get('Ds_MerchantParameters', '')
        #parameters_dic = json.loads(base64.b64decode(parameters).decode())
        #reference = urllib.parse.unquote(parameters_dic.get('Ds_Order', ''))
        #pay_id = parameters_dic.get('Ds_AuthorisationCode')
        #shasign = data.get(
        #    'Ds_Signature', '').replace('_', '/').replace('-', '+')
        #test_env = http.request.session.get('test_enable', False)
        #if not reference or not pay_id or not shasign:
        #    error_msg = 'Redsys: received data with missing reference' \
        #        ' (%s) or pay_id (%s) or shashign (%s)' % (reference,
        #                                                   pay_id, shasign)
        #    if not test_env:
        #        _logger.info(error_msg)
        #       raise ValidationError(error_msg)
        #    # For tests
        #    http.OpenERPSession.tx_error = True
        #tx = self.search([('reference', '=', reference)])
        #if not tx or len(tx) > 1:
        #    error_msg = 'Redsys: received data for reference %s' % (reference)
        #    if not tx:
        #        error_msg += '; no order found'
        #    else:
        #        error_msg += '; multiple order found'
        #    if not test_env:
        #        _logger.info(error_msg)
        #        raise ValidationError(error_msg)
        #    # For tests
        #    http.OpenERPSession.tx_error = True
        #if tx and not test_env:
            # verify shasign
        #    shasign_check = tx.acquirer_id.sign_parameters(
        #        tx.acquirer_id.redsys_secret_key, parameters)
        #    if shasign_check != shasign:
        #        error_msg = (
        #            'Redsys: invalid shasign, received %s, computed %s, '
        #            'for data %s' % (shasign, shasign_check, data)
        #        )
        #        _logger.info(error_msg)
        #        raise ValidationError(error_msg)
        print("SALIMOS DEL FORM")
        return tx

    @api.multi
    def _redsys_form_get_invalid_parameters(self, data):
        print("invalid")
        test_env = http.request.session.get('test_enable', False)
        invalid_parameters = []
        #parameters_dic = self.merchant_params_json2dict(data)
        #if (self.acquirer_reference and
        #        parameters_dic.get('Ds_Order')) != self.acquirer_reference:
        #    invalid_parameters.append(
        #        ('Transaction Id', parameters_dic.get('Ds_Order'),
        #         self.acquirer_reference))

        # check what is buyed
        #if self.acquirer_id.redsys_percent_partial > 0.0:
        #    new_amount = self.amount - (
        #        self.amount * self.acquirer_id.redsys_percent_partial / 100)
        #    self.amount = new_amount

        #if (float_compare(float(parameters_dic.get('Ds_Amount', '0.0')) / 100,
        #                  self.amount, 2) != 0):
        #    invalid_parameters.append(
        #        ('Amount', parameters_dic.get('Ds_Amount'),
        #         '%.2f' % self.amount))

        if invalid_parameters and test_env:
            # If transaction is in test mode invalidate invalid_parameters
            # to avoid logger error from parent method
            return []
        return invalid_parameters

    @api.multi
    def _redsys_form_validate(self, data):

        #Tomamos la id de paymenttransaction

        pedido = data['order']
        reference = pedido.transaction_ids[0].reference
        tx = self.search([('reference', '=', reference)])


        # create an instance of the API class
        api_instance = swagger_client.PayInsRedsysApi()
        pay_in_id = tx.redsys_txnid  # int | The Id of a payment
        print(pay_in_id)

        try:
            # View a Redsys payment
            api_response = api_instance.pay_ins_redsys_redsys_get_payment(pay_in_id)
            print(api_response)
        except ApiException as e:
            print("Exception when calling PayInsRedsysApi->pay_ins_redsys_redsys_get_payment: %s\n" % e)


        print("vamos!!")
        print(api_response.status)

        #parameters_dic = self.merchant_params_json2dict(data)
        #status_code = int(parameters_dic.get('Ds_Response', '29999'))
        if api_response.status == "SUCCEEDED":
            print("dentro del if")
            self.write({
                'state': 'done',
                #'redsys_txnid': parameters_dic.get('Ds_AuthorisationCode'),
                'state_message': 'Ok',
            })
            #if self.acquirer_id.send_quotation:
            #    self.sale_order_ids.force_quotation_send()
            print("escrito el estado del pedido")
            return True

        if api_response.status == "FAILED":
            # 'Payment error: bank unavailable.'
            self.write({
                'state': 'cancel',
                #'redsys_txnid': parameters_dic.get('Ds_AuthorisationCode'),
                'state_message': 'Bank Error'

            })
            return False


    @api.model
    def form_feedback(self, data, acquirer_name):

        res = super(TxRedsys, self).form_feedback(data, acquirer_name)

        print("#########################DEMO###############################")





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

