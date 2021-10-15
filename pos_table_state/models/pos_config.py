# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    state_ids = fields.Many2many('restaurant.table.state', 'restaurant_table_state_rel', 'table_id', 'state_id', 'State')
    
    
    def write(self, vals):
        if vals.get('state_ids'):
            len_state = len(vals.get('state_ids')[0])
            for state in vals.get('state_ids')[0][len_state - 1]:
                state_id = self.env['restaurant.table.state'].sudo().browse(state)
                if state_id.name == 'Manual':
                    raise ValidationError(_('You can\'t add Manual Type state.'))
        return super(PosConfig, self).write(vals)