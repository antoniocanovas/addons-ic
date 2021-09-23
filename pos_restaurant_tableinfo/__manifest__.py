# -*- coding: utf-8 -*-
# Part of Odoo.


{
    'name': 'Restaurant Table Info',
    'version': '14.0.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'Table information as checkin or amount for Restaurant extensions Point of Sale ',
    'description': """


""",
    'depends': [
        "pos_restaurant",
        "pos_discount",
        "pos_hr"],
    'website': '',
    'data': [
        'views/pos_restaurant_tableinfo.xml',
    ],
    'qweb': [
        'static/src/xml/Screens/Restaurant/TableInfo.xml',

    ],

    'installable': True,
    'auto_install': False,
}
