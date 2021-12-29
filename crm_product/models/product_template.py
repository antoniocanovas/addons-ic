from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    lead_ids = fields.Many2many(comodel_name='crm.lead',
                                relation_table='product_lead_rel',
                                column1='product_id',
                                column2='lead_id',
                                string="Leads",
                                )



