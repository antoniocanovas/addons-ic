{
    'name': "HelpDesk tickets link partner credentials",
    'summary': """
        Relaciona tickets de helpdesk con partner credentials.
        """,
    'author': "Pedro Guirao",
    'license': 'AGPL-3',
    'website': "https://ingenieriacloud.com",
    'category': 'Tools',
    'version': '14.0.1.0.0',
    'depends': [
        'partner_credentials',
        'helpdesk_mgmt'
    ],
    'data': [
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
}
