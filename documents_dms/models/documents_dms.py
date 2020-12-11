# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api



class DocumentDms(models.Model):
    _inherit = 'ir.attachment'

    type_id = fields.Many2one('document.types',string='Type')
    route_id = fields.Selection(string='Route', related='type_id.route',  store=False)
    mobile = fields.Char(string='Mobile', related='partner_id.mobile', store=False)
    external_ref = fields.Char('External Ref')

    @api.multi
    def _calculate_internal_ref(self):
        for record in self:
            record['internal_ref']= '#' + str(record.id)

    internal_ref = fields.Char('Internal Ref', compute=_calculate_internal_ref, store="False")

    #@api.onchange('partner_id')
    #def _get_main_attachment(self):
    #    for record in self:
    #        self._set_main_attachment(record)

    #has_main = fields.Boolean(compute='_get_main_attachment')

    #def _set_main_attachment(self, attachment):
    #    print("TRY MAIN ATTACHMENT")
    #   # if self.message_main_attachment_id == False:
    #    body = "<p>created with Documents D</p>"
    #    self.message_post(body=body, subtype='mail.mt_comment', attachments={attachment})
    #    self.message_main_attachment_id = [(4, attachment.id)]
