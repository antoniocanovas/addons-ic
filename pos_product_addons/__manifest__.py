# -*- coding: utf-8 -*-
{
    'name': "POS Product Addons",
    'summary': """POS Product Addons""",
    'description': """POS Product Addons""",
    'website': "https://www.candidroot.com/",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'category': 'Point of Sale',
    'version': '14.0.0.0.1',
    'depends': ['point_of_sale'],
    'data': [
        'views/assets.xml',
        'views/pos_view.xml',
    ],
    'qweb': [
        'static/src/xml/Screens/OrderlineDetails.xml',
        'static/src/xml/Screens/OrderWidget.xml',
    ],
    
}
