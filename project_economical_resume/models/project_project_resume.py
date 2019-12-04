# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectTaskContacts(models.Model):
    _inherit = 'project.project'

    @api.depends('create_date')
    def _get_supply_advanced(self):
        for record in self:
            total = 0
            cuentas = self.env['account.account'].search([('is_supply', '=', True)]).ids
            pagos_suplidos = self.env['account.analytic.line'].search(
                [('account_id', '=', record.analytic_account_id.id),
                 ('general_account_id', 'in', cuentas), ('amount', '>', 0)])
            for pago in pagos_suplidos: total += pago.amount
            record['supply_advanced'] = total

    supply_advanced = fields.Monetary(string='Adelanto Suplidos', stored=False, compute=_get_supply_advanced)

    @api.depends('create_date')
    def _get_supply_consumed(self):
        for record in self:
            total = 0
            cuentas = self.env['account.account'].search([('is_supply', '=', True)]).ids
            pagos_suplidos = self.env['account.analytic.line'].search(
                [('account_id', '=', record.analytic_account_id.id),
                 ('general_account_id', 'in', cuentas), ('amount', '<', 0)])
            for pago in pagos_suplidos: total += pago.amount
            record['supply_consumed'] = -1 * total

    supply_consumed = fields.Monetary(string='Gastos Suplidos',stored=False,compute=_get_supply_consumed)

    @api.depends('create_date')
    def _get_supply_available(self):
        for record in self:
            record['supply_available'] = record.advance_supply - record.expense_supply

    supply_available = fields.Monetary(string='Disponible Suplidos',stored=False,compute=_get_supply_available)

    @api.depends('create_date')
    def _get_customer_invoiced(self):
        for record in self:
            total = 0
            cuentas = self.env['account.account'].search([('is_supply', '=', True)]).ids
            facturado = self.env['account.analytic.line'].search([('account_id', '=', record.analytic_account_id.id),
                                                                  ('general_account_id', 'not in', cuentas),
                                                                  ('project_id', '=', False)])
            for fac in facturado: total += fac.amount
            record['customer_invoiced'] = total

    customer_invoice = fields.Monetary(string='Facturado',stored=False,compute=_get_customer_invoiced)

    @api.depends('create_date')
    def _get_timesheet_cost(self):
        for record in self:
            total = 0
            imputaciones = self.env['account.analytic.line'].search(
                [('project_id', '!=', False), ('account_id', '=', record.analytic_account_id.id)])
            for imp in imputaciones: total += imp.amount
            record['timesheet_cost'] = total

    timesheet_cost = fields.Monetary(string='Imputaciones',stored=False,compute=_get_timesheet_cost)

    @api.depends('create_date')
    def _get_balance(self):
        for record in self:
            total = 0
            importes = self.env['account.analytic.line'].search([('account_id', '=', record.analytic_account_id.id)])
            for importe in importes: total += importe.amount
            record['balance'] = total - record.advance_supply + record.expense_supply

    balance = fields.Monetary(string='Saldo',stored=False,compute=_get_balance)
