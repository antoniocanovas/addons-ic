# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Service BOM",
    "summary": "Product BOM price.",
    "version": "16.0.1.0.0",
    'category': 'Sales',
    "author": "Serincloud SL, ",
    "website": "https://www.ingenieriacloud.com",
    "license": "AGPL-3",
    "depends": [
        "product_variant_sale_price",
        "mrp",
                ],
    "data": [
        "views/product_views.xml",
    ],
    "installable": True,
}
