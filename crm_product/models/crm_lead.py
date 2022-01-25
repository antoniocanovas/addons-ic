from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    product_ids = fields.Many2many(
        comodel_name='product.template',
        relation='product_lead_rel',
        column1='lead_id',
        column2='product_id',
    )

    def get_lead_self(self):
        for record in self:
            record.self = self.env['crm.lead'].search([('id','=',record.id)])
    self = fields.Many2one(string="Self", store=False, compute="get_lead_self")

