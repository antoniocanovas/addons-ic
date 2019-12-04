# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTaskContacts(models.Model):
    _inherit = 'project.project'

    @api.depends('create_date')
    def _get_advance_supply(self):
        for record in self:
            total = 0
            cuentas = self.env['account.account'].search([('is_supply', '=', True)]).ids
            pagos_suplidos = self.env['account.analytic.line'].search(
                [('account_id', '=', record.analytic_account_id.id),
                 ('general_account_id', 'in', cuentas), ('amount', '>', 0)])
            for pago in pagos_suplidos: total += pago.amount
            record['advance_supply'] = total

    advance_supply = fields.Monetary(string='Adelanto Suplidos',stored=False,compute=_get_advance_supply)

    @api.depends('create_date')
    def _get_expense_supply(self):
        for record in self:
            total = 0
            cuentas = self.env['account.account'].search([('is_supply', '=', True)]).ids
            pagos_suplidos = self.env['account.analytic.line'].search(
                [('account_id', '=', record.analytic_account_id.id),
                 ('general_account_id', 'in', cuentas), ('amount', '<', 0)])
            for pago in pagos_suplidos: total += pago.amount
            record['expense_supply'] = -1 * total

    expense_supply = fields.Monetary(string='Gastos Suplidos',stored=False,compute=_get_expense_supply)

    @api.depends('create_date')
    def _get_aviable_supply(self):
        for record in self:
            record['aviable_supply'] = record.advance_supply - record.expense_supply

    aviable_supply = fields.Monetary(string='Disponible Suplidos',stored=False,compute=_get_aviable_supply)

    @api.depends('create_date')
    def _get_invoiced_case(self):
        for record in self:
            total = 0
            cuentas = self.env['account.account'].search([('is_supply', '=', True)]).ids
            facturado = self.env['account.analytic.line'].search([('account_id', '=', record.analytic_account_id.id),
                                                                  ('general_account_id', 'not in', cuentas),
                                                                  ('is_timesheet', '=', False)])
            for fac in facturado: total += fac.amount
            record['invoiced_case'] = total

    invoiced_case = fields.Monetary(string='Facturado',stored=False,compute=_get_invoiced_case)

    @api.depends('create_date')
    def _get_inputed_case(self):
        for record in self:
            total = 0
            imputaciones = self.env['account.analytic.line'].search(
                [('is_timesheet', '=', True), ('account_id', '=', record.analytic_account_id.id)])
            for imp in imputaciones: total += imp.amount
            record['inputed_case'] = total

    inputed_case = fields.Monetary(string='Imputaciones',stored=False,compute=_get_inputed_case)

    @api.depends('create_date')
    def _get_aviable_case(self):
        for record in self:
            total = 0
            imputaciones = self.env['account.analytic.line'].search(
                [('is_timesheet', '=', True), ('account_id', '=', record.analytic_account_id.id)])
            for imp in imputaciones: total += imp.amount
            record['aviable_case'] = total

    aviable_case = fields.Monetary(string='Saldo',stored=False,compute=_get_aviable_case)
