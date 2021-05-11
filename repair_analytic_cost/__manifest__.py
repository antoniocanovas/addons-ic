# Copyright 2021 IC - Pedro Guirao
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Repair cost Analytic",
    "summary": "Adds the analytic account to the production order",
    "version": "14.0.1.0.0",
    "category": "Manufacturing",
    "author": "Pedro Guirao, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-analytic",
    "license": "AGPL-3",
    "depends": ["repair_analytic","base_automation"],
    "data": ["views/repair_view.xml","data/automatic_actions.xml"],
    "installable": True,
}
