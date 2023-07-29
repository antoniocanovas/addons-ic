from odoo import api, fields, models, _


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

#    Borro "ARROBA"api.multi
    def create_invoices(self):
        res = super().create_invoices()
        invoices_ids = res['res_id']
        domain = res['domain']
        invoices = self.env['account.move']
        if bool(invoices_ids):
            invoices = invoices.browse(invoices_ids).exists()
        elif not isinstance(domain, str):
            invoices = invoices.search(domain).exists()

        for invoice in invoices:
            if invoice.move_type not in ['out_invoice', 'out_refund']:
                continue
            sales = invoice.invoice_line_ids.mapped('sale_line_ids.order_id')
            if bool(sales):
                collaborator = sales.mapped('pnt_collaborator_id')
                if len(collaborator) == 1:
                    invoice.pnt_collaborator_id = collaborator.id
        return res

