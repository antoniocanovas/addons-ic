from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    lead_ids = fields.Many2many(comodel_name='crm.lead',
                                relation='product_lead_rel',
                                column1='product_id',
                                column2='lead_id',
                                string="Leads",
                                )

    def get_product_template_self(self):
        for record in self:
            record.self = self.env['product.template'].search([('id','=',record.id)]).id
    self = fields.Many2one('product.template', string="Self", store=False, compute="get_product_template_self")



