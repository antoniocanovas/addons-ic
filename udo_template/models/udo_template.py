from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class UdoTemplate(models.Model):
    _name = 'udo.template'
    _description = 'UDO Template'

    name = fields.Char(string='Name')
    ref = fields.Char(string='Ref')
    description = fields.Text(string='Description')
    department_id = fields.Many2one('hr.department', string='Department')
    target_id = fields.Many2one('udo.target', help='Office, Residential', string='Target')
    quality_id = fields.Many2one('udo.quality', string='Quality')
    style_id = fields.Many2one('udo.style', string='Style')
    type_id = fields.Many2one('udo.type',  string='Type')
    product_brand_id = fields.Many2one('product.brand', string='Product brand')

    line_ids = fields.One2many('udo.line', 'order_line_id')
