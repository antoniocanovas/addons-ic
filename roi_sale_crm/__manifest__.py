# -*- coding: utf-8 -*-
##############################################################################
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    Copyright (C) 2021 Serincloud S.L. All Rights Reserved
#    Antonio Cánovas <antonio.canovas@ingenieriacloud.com>
#    Pedro josé Baños Guirao <pedro@serincloud.com>
##############################################################################

{
    "name": "ROI Sale Crm",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "author": "www.serincloud.com",
    "maintainer": "Pedroguirao",
    "website": "www.serincloud.com",
    "license": "AGPL-3",
    "depends": [
        'roi',
        'sale',
        'crm',
    ],
    "data": [
        #"views/roi_set.xml",
        #"views/menu_views.xml",
        "views/roi.xml",
        #"security/ir.model.access.csv",

    ],
    "installable": True,
}
