# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api

class SetTemplateLine(models.Model):
    _name = 'set.template.line'
    _description = 'Set Template Line'

    set_id   = fields.Many2one('set.template', string='Set', store=True, required=True, copy=True)
    value_id = fields.Many2one('product.attribute.value', string='Value', store=True, required=True, copy=True)
    quantity = fields.Integer('Quantity', store=True, copy=True)