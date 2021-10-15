# -*- coding: utf-8 -*-
{
    'name': "POS Table State",
    'summary': """
        POS Table State""",
    'description': """
        POS Table State
    """,
    'website': "https://www.candidroot.com/",
    'author': "Candidroot Solutions Pvt. Ltd.",
    'category': 'Point of Sale',
    'version': '14.0.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['point_of_sale', 'pos_restaurant'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'data/restaurant_table_state_data.xml',
        'views/restaurant_table_state_views.xml',
        'views/restaurant_table_views.xml',
        'views/pos_config_view.xml',
    ],
    'qweb': [
        'static/src/xml/Screens/FloorScreen/TableWidget.xml',
        'static/src/xml/ProductScreen/ControlButtons/SetStateButton.xml',
    ],
    
}
