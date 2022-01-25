from odoo import _, api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    product_ids = fields.Many2many(
        comodel_name='product.template',
        relation='product_lead_rel',
        column1='lead_id',
        column2='product_id',
    )

    @api.depends('create_date')
    def get_lead_self(self):
        for record in self:
            lead = self.env['crm.lead'].search([('id', '=', record.id)])
            record.self = lead.id
    self = fields.Many2one('crm.lead', string="Self", store=True, compute="get_lead_self")

