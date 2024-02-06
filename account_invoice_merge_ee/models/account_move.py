# Copyright 2024 Puntsistemes S.L.U

from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_invoice_line_key_cols(self):
        fields = super(AccountMove, self)._get_invoice_line_key_cols()
        subscription_fields = (
            "subscription_id",
            "subscription_mrr",
            "subscription_start_date",
            "subscription_end_date",
        )
        fields.extend(subscription_fields)

        return fields
