# Copyright 2017 Simone Orsi.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Website blog private',
    'version': '16.0.1.0.0',
    'author': 'Serincloud SL',
    'website': 'https://github.com/OCA/website',
    'license': 'LGPL-3',
    'category': 'Website',
    'summary': 'Blog only for internal users, as news board.',
    'depends': [
        'website_blog',
    ],
    'data': [
        'security/ir_model_access.xml',
    ],
    'installable': True,
}
