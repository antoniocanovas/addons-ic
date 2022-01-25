from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    lead_ids = fields.Many2many(comodel_name='crm.lead',
                                relation='product_lead_rel',
                                column1='product_id',
                                column2='lead_id',
                                string="Leads",
                                )

    @api.depends('create_date')
    def get_product_template_self(self):
        for record in self:
            pt = self.env['product.template'].search([('id','=',record.id)])
            record.self = pt.id
    self = fields.Many2one('product.template', string="Self", store=True, compute="get_product_template_self")



