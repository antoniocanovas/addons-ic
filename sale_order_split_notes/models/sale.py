# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def split_note_lines(self):
        for li in self.order_line:
            if li.display_type == 'line_note':
                texto = li.name
                array = texto.splitlines()
                for a in array:
                    nueva = self.env['sale.order.line'].create(
                        {'display_type': 'line_note', 'name': a, 'order_id': self.id, 'sequence': li.sequence})
                li.unlink()