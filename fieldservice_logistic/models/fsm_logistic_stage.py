from odoo import fields, models, api


class FsmOrderLogistic(models.Model):
    _inherit = 'fsm.stage'


    @api.depends('create_date')
    def _get_external_id(self):
        for record in self:
            nombre = self.env['ir.model.data'].search([('model', '=', 'fsm.stage'), ('res_id', '=', record.id)]).name
            record['external_id'] = nombre

    external_id = fields.Char(string='Trayecto', stored=True, readonly=True, compute=_get_external_id)
