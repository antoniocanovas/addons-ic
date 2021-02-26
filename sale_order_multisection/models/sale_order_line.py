from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('name', 'sequence', 'section_id.section')
    def _get_section(self):
        for record in self:
            seccion = ''
            if (record.display_type == 'line_section') and (record.name[:1] == '$') and (
                    record.section != record.name.split()[0]):
                record.section = record.name.split()[0]
            elif not record.display_type:
                parar = False
                lineas = record.order_id.order_line.sorted(key=lambda r: r.sequence)
                for li in lineas:
                    if not parar and (li.display_type == 'line_section'):
                        seccion = li.section
                    if (li.id == record.id): parar = True
                if (record.section != seccion):
                    record.section = seccion

    section = fields.Char('Section', store=True, compute=_get_section)

    @api.depends('section')
    def _get_section_id(self):
        for record in self:
            # Este campo que sea calculado al modificarse x_seccion:
            if not record.display_type and record.section:
                record.section_id = self.env['sale.order.line'].search(
                    [('order_id', '=', record.order_id.id), ('section', '=', record.section),
                     ('id', '!=', record.id)]).id

    section_id = fields.Many2one('sale.order.line', readonly=True, store=True, compute=_get_section_id)

    @api.depends('create_date')
    def _get_total_section(self):
        for record in self:
            total = 0
            if record.display_type == 'line_section':
                secciones = record.child_ids.ids
                secciones.append(record.id)
                lineas = self.env['sale.order.line'].search([('section_id', 'in', secciones)])
                for li in lineas: total += li.price_subtotal
            record['total_section'] = total

    total_section = fields.Float(
        'Total Section',
        readonly=True,
        compute=_get_total_section,
    )

    @api.depends('father_ids')
    def _get_level(self):
        for record in self:
            record.level = len(record.father_ids) + 1

    level = fields.Integer(
        'Level',
        readonly=True,
        store=True,
        compute=_get_level,
    )

    @api.depends('name')
    def _get_child_ids(self):
        for record in self:
            if record.name:
                hijos = []
                if (record.display_type == 'line_section') and (record.name[:1] == '$'):
                    largosec = len(record.section)
                    lineas = self.env['sale.order.line'].search(
                        [('order_id', '=', record.order_id.id), ('display_type', '=', 'line_section'), ('id', '!=', record.id)])
                    for li in lineas:
                        if (li.section) and (record.section == li.section[:largosec]):
                            hijos.append(li.id)
                record.write({'child_ids': [(6, 0, hijos)]})

    child_ids = fields.Many2many(
        'sale.order.line',
        relation='sections_rel',
        column1='father_section_id',
        column2='child_section_id',
        readonly=True,
        store=True,
        compute=_get_child_ids)

    @api.depends('name')
    def _get_father_ids(self):
        for record in self:
            if record.name:
                padres = []
                if (record.display_type == 'line_section') and (record.name[:1] == '$'):
                    largosec = len(record.section)
                    lineas = self.env['sale.order.line'].search(
                        [('order_id', '=', record.order_id.id), ('display_type', '=', 'line_section'),
                         ('id', '!=', record.id)])
                    for li in lineas:
                        largoli = len(li.section)
                        if (li.section) and (li.section == record.section[:largoli]):
                            padres.append(li.id)
                record.write({'father_ids': [(6, 0, padres)]})

    father_ids = fields.Many2many(
        'sale.order.line',
        relation='sections_rel',
        column1='child_section_id',
        column2='father_section_id',
        readonly=True,
        store=True,
        compute=_get_father_ids)


