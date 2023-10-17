# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    PedroGuirao pedro@serincloud.com
##############################################################################

{
    "name": "Product pricelist Tracking",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "author": "www.serincloud.com",
    "maintainer": "Serincloud",
    "website": "www.serincloud.com",
    "license": "AGPL-3",
    "depends": [
        'sale_management',
        'mail',
    ],
    "data": [
        'views/product_pricelist_views.xml'
    ],
    "installable": True,
}
