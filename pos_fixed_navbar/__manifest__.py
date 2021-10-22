# -*- coding: utf-8 -*-
{
    'name': "POS Fixed Navbar",
    'summary': """
        POS Fixed Navbar""",
    'description': """
        POS Fixed Navbar
    """,
    'website': "https://www.candidroot.com/",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'category': 'Point of Sale',
    'version': '14.0.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],
    # always loaded
    'data': [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/ProductScreen/ProductsWidgetControlPanel.xml'
    ],
    
}
