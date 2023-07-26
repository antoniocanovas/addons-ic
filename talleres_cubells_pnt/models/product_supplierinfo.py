
from odoo import models, api, fields
from datetime import timedelta


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

#    @api.depends('partner_id','date_start','price','discount')
    def name_get(self):
        for record in self:
            name = record.partner_id.name + str(record.price) + "€, Dto: " + str(record.discount) + "% "
            if record.last_purchase_date:
                name += str(record.last_purchase_date)
            record['display_name'] = name
    display_name = fields.Char('Name', store=False, compute='name_get')

    name = fields.Char('Name', store=False, compute='name_get')