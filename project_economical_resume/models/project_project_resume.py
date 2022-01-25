# Copyright Serincloud
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ProjectEconomicalResume(models.Model):
    _inherit = 'project.project'

    credit = fields.Monetary(related='partner_id.credit', stored='False', readonly=True, string="Credito en cliente")

    @api.depends('create_date')
    def _get_invoiced_due(self):
        for record in self:
            total = 0
            facturas = []
            lineas = self.env['account.invoice.line'].search(
                [('account_analytic_id', '=', record.analytic_account_id.id),
                 ('invoice_id.type', 'in', ['out_invoice']),
                 ('invoice_id.state', 'not in', ['cancel'])])

            for li in lineas:
                if (li.invoice_id.residual != 0) and (li.invoice_id.id not in facturas):
                    total += li.invoice_id.residual
                    facturas.append(li.invoice_id.id)
            record['invoiced_due'] = total

    invoiced_due = fields.Monetary(string='Por cobrar', stored=False, readonly=True,
                                   compute=_get_invoiced_due)

    @api.depends('create_date')
    def _get_invoiced(self):
        for record in self:
            total = 0
            lineas = self.env['account.invoice.line'].search(
                [('account_analytic_id', '=', record.analytic_account_id.id),
                 ('invoice_id.type', 'in', ['out_invoice']),
                 ('invoice_id.state', 'not in', ['cancel'])])
            for li in lineas:
                total += li.price_total
            record['invoiced'] = total

    invoiced = fields.Monetary(string='Importe', stored=False, readonly=True,
                               compute=_get_invoiced)

    @api.depends('create_date')
    def _get_analytic_line(self):
        for record in self:
            apuntes = self.env['account.analytic.line'].search([('account_id', '=', record.analytic_account_id.id)]).ids
            record['analytic_line_ids'] = [(6, 0, apuntes)]

    analytic_line_ids = fields.Many2many(comodel_name='account.analytic.line',
                                relation="m2m_project_account_analytic_line_rel",
                                column1="m2m_id",
                                column2="line_id", string='Costes e Ingresos',
                                         stored=False, readonly=True, compute=_get_analytic_line)

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
            record['supply_available'] = record.supply_advanced - record.supply_consumed

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

    customer_invoiced = fields.Monetary(
        string='Facturado',
        stored=False,
        compute=_get_customer_invoiced,
        help='Suma de productos y servicios facturados a cliente menos los provenientes de facturas de proveedor que se han asignado contra esta cuenta análitica'
    )

    @api.depends('create_date')
    def _get_timesheet_cost(self):
        for record in self:
            total = 0
            imputaciones = self.env['account.analytic.line'].search(
                [('project_id', '!=', False), ('account_id', '=', record.analytic_account_id.id)])
            for imp in imputaciones: total += imp.amount
            record['timesheet_cost'] = total

    timesheet_cost = fields.Monetary(
        string='Imputaciones',stored=False,
        compute=_get_timesheet_cost,
        help='Coste de horas imputadas contra este proyecto'
                                    )

    @api.depends('create_date')
    def _get_balance(self):
        for record in self:
            total = 0
            importes = self.env['account.analytic.line'].search([('account_id', '=', record.analytic_account_id.id)])
            for importe in importes: total += importe.amount
            record['balance'] = total - record.supply_advanced + record.supply_consumed

    balance = fields.Monetary(string='Saldo',stored=False,compute=_get_balance)
