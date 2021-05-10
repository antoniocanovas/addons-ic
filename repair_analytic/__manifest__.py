# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Analytic for Repair Orders",
    "summary": "Adds the analytic account to the repair order",
    "version": "14.0.1.0.0",
    "category": "Repair",
    "author": "Pedro Guirao, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-analytic",
    "license": "AGPL-3",
    "depends": ["repair", "analytic"],
    "data": ["views/repair_view.xml", "views/analytic_account_view.xml"],
    "installable": True,
}
