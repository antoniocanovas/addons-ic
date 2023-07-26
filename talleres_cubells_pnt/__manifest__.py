# -*- coding: utf-8 -*-
{
    'name': 'Personalizaciones para Talleres Cubells',
    'version': '14.0.1.0.0',
    'summary': 'Personalizaciones',
    'author': 'Punt Sistemes S.L.U.',
    'contributors': ['Isaac Gallart <igallart@puntsistemes.es>'],
    'website': 'http://www.puntsistemes.es',
    'license': 'AGPL-3',
    'category': 'Custom',
    'installable': True,
    'auto_install': False,
    'application': False,
    'depends': [
        'purchase',
        'sale',
        'stock',
        'account',
        'maintenance',
        'hr_maintenance',
        'purchase_discount',
    ],
    'data': [
            'security/ir.model.access.csv',
            #'views/templates.xml',
            'views/purchase_view.xml',
            'views/stock_view.xml',
            'views/sale_order.xml',
            'views/maintenance.xml',
            'views/model.xml',
            'views/fuel.xml',
            'views/invoice.xml',
    ]
}
