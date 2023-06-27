from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        values = super(AccountMove, self).action_post()

        if (self.move_type in ['out_invoice']) and (self.state in ['posted']):
            for li in self.invoice_line_ids:
                cost = 0
                if not (li.analytic_cost_id.id) and (li.analytic_account_id.id) and (li.product_id.product_tmpl_id.autoanalytic):
                    if li.product_uom_id.uom_type == 'reference':
                        cost = li.product_id.standard_price
                    elif li.product_uom_id.uom_type == 'bigger':
                        cost = li.product_id.standard_price * li.product_uom_id.factor_inv
                    elif li.product_uom_id.uom_type == 'smaller':
                        cost = li.product_id.standard_price / li.product_uom_id.factor
                    cost = -1 * cost * li.quantity

                    new = self.env['account.analytic.line'].create({
                        'name':li.product_id.name,
                        'account_id': li.analytic_account_id.id,
                        'product_id': li.product_id.id,
                        'unit_amount': li.quantity,
                        'product_uom_id': li.product_uom_id.id,
                        'amount': cost
                    })
                    li['analytic_cost_id'] = new.id

        return values