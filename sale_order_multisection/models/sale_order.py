from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleOrderSets(models.Model):
    _inherit = 'sale.order'

    def _get_lines_count(self):
        results = self.env['sale.order.line'].search([
            ('order_id', '=', self.id),
            ('display_type', '=', 'line_section')]
        )
        self.section_lines_count = len(results)

    section_lines_count = fields.Integer('Lines', compute=_get_lines_count)

    def action_view_sections(self):
        action = self.env.ref(
            'sale_order_multisection.action_view_sections').read()[0]
        return action

    def order_sections(self):
        # Ordenar secciones alfabéticamente por 'sección', y continuar con sus líneas en un array:
        secciones = self.env['sale.order.line'].search(
            [('order_id', '=', self.id), ('display_type', '=', 'line_section')]).sorted(key=lambda r: r.section)
        lineas = []
        for se in secciones:
            for li in self.order_line:
                if (li.id == se.id) or (li.section_id.id == se.id):
                    lineas.append(li)
        # Asignar nueva secuencia según array:
        contador = 1
        for li in lineas:
            li['sequence'] = contador
            contador += 1
