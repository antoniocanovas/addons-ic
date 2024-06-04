from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class PartnerCredentialCategory(models.Model):
    _name = 'partner.credential.category'
    _description = 'Partner credential category'

    name = fields.Char(string='Name', required=True)
    department_ids = fields.Many2many("hr.department", string="Departments")
    logo = fields.Binary('Logo')

    def _get_credential_category_count(self):
        for record in self:
            credentials = self.env['partner.credential'].search([('category_id','=',record.id)])
            record['credential_count'] = len(credentials)
    credential_count = fields.Integer("Credential count", compute='_get_credential_category_count')

    def action_view_credentials(self):
        action = self.env['ir.actions.act_window'].with_context({'active_id': self.id})._for_xml_id('partner_credential.act_credential_category_2_credential_all')
        action['display_name'] = _("%(name)s", name=self.name)
        context = action['context'].replace('active_id', str(self.id))
        context = ast.literal_eval(context)
        context.update({
            'create': self.active,
            'active_test': self.active
            })
        action['context'] = context
        return action