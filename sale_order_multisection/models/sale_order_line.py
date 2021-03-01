from odoo import _, api, fields, models

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    partner_id = fields.Many2one('res.partner', related='order_id.partner_id', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', related='order_id.pricelist_id', readonly=True)
    section_line_ids = fields.One2many('sale.order.line', 'section_id', store=True, string='Section Lines')

    @api.depends('name', 'sequence', 'section_id.section')
    def _get_section(self):
        print("DEBUG section")
        for record in self:
            seccion = ''
            if record.name:
                if (record.display_type == 'line_section') and (record.name[:1] == '$') and (
                        record.section != record.name.split()[0]):
                    print("IF 1", record.section , record.name, record.name.split()[0])
                    record.section = record.name.split()[0]
                else:
                    parar = False
                    lineas = record.order_id.order_line.sorted(key=lambda r: r.sequence)
                    print("Lineas")
                    for li in lineas:
                        if not parar and (li.display_type == 'line_section'):
                            seccion = li.section
                            print(seccion)
                        if (li.id == record.id): parar = True
                    if (record.section != seccion):
                        print("seccion !=")
                        record.section = seccion

    section = fields.Char('Section', store=True, compute=_get_section)

    @api.depends('section')
    def _get_section_id(self):
        print("DEBUG section id")
        for record in self:
            # Este campo que sea calculado al modificarse o crearse x_seccion:
            if (record.display_type != 'line_section') and (record.section):
                record['section_id'] = self.env['sale.order.line'].search(
                    [('order_id', '=', record.order_id.id), ('section', '=', record.section),
                     ('id', '!=', record.id), ('display_type', '=', 'line_section')]).id

    section_id = fields.Many2one('sale.order.line', readonly=True, store=True, compute=_get_section_id)

    @api.depends('create_date')
    def _get_total_section(self):
        print("DEBUG section total")
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

    @api.depends('parent_ids')
    def _get_level(self):
        print("DEBUG level")
        for record in self:
            record.level = len(record.parent_ids) + 1

    level = fields.Integer(
        'Level',
        readonly=True,
        store=True,
        compute=_get_level,
    )

    @api.depends('name')
    def _get_child_ids(self):
        print("DEBUG child")
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
        column1='parent_section_id',
        column2='child_section_id',
        readonly=True,
        store=True,
        compute=_get_child_ids)

    @api.depends('name')
    def _get_parent_ids(self):
        print("DEBUG father")
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
                record.write({'parent_ids': [(6, 0, padres)]})

    parent_ids = fields.Many2many(
        'sale.order.line',
        relation='sections_rel',
        column1='child_section_id',
        column2='parent_section_id',
        readonly=True,
        store=True,
        compute=_get_parent_ids)


