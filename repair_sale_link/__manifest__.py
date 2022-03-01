# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Repair Sale Link",
    "summary": "Link all repairs for a Sale Order.",
    "version": "14.0.1.0.0",
    "category": "Repair",
    "author": "Pedro Guirao, ",
    "website": "",
    "license": "AGPL-3",
    "depends": ["repair", "sale"],
    "data": [
        "views/repair_view.xml",
        "views/sale_order.xml",
    ],
    "installable": True,
}
