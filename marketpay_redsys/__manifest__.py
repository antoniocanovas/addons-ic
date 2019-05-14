# Copyright 2017 Tecnativa - Sergio Teruel

{
    'name': 'Redsys by Marketpay',
    'category': 'Payment Acquirer',
    'summary': 'Payment Acquirer: Marketpay/Redsys',
    'version': '1.0.0',
    'author': "Pedro Baños Guirao"
              "ingenieriacloud.com",
    'depends': [
        'payment',
        'website_sale',
    ],
    "external_dependencies": {
        "python": [

        ],
    },
    'data': [
        'views/marketpay.xml',
        'views/marketpay_acquirer.xml',
        'views/payment_marketpay_templates.xml',

    ],
    'license': 'AGPL-3',
    'installable': True,
}
