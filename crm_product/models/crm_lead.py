from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    product_ids = fields.Many2many(
        comodel_name='product.template',
        relation='product_lead_rel',
        column1='lead_id',
        column2='product_id',
    )
