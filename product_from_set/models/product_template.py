# Copyright Serincloud SL - Ingenieriacloud.com


from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    set_template_ids = fields.Many2many('set.template', string='Set templates', store="True",)
    parent_id = fields.Many2one('product.template', string='Parent set', store=True)
    set_product_ids  = fields.One2many('product.template','parent_id', string='Set products', store=True, readonly=True)

    def _create_set_products(self):
        if not self.default_code:
            raise UserError('Asigna código a este producto para usarlo en las referencias de los surtidos')
        for li in self.set_template_ids:
            code = self.default_code + self.li.code
            exist = self.env['product.template'].search([('default_code','=', code)])
            if not exist.id:
                exist = self.env['product.template'].create({'name':code, 'default_code':code, 'barcode':code,
                                                                   'detailed_type':'product',
                                                                   'parent_id':self.id
                                                                   })


            # Exista o no deberíamos comprobar si ya tiene la lista de materiales:
            if not exist.bom_ids.ids:
                new_bom = self.env['mrp.bom'].create({'code':code, 'type':'normal', 'product_qty':1,
                                                      'product_tmpl_id':self.id,})

            # Mismo chequeo con las líneas bom:
            if not exist.bom_ids.bom_line_ids.ids:
                # Crear las líneas del BOM tras haber buscado si existen las variantes en SELF:
                for value in li.line_ids:
                    exist_pp = self.env['product.product'].search([('product_tmpl_id','=',self.id),
                                                                   ('product_template_variant_value_ids', 'in', li.main_value_ids),
                                                                   ('product_template_variant_value_ids', 'in', li.value_id),
                                                                   ])
                    if exist_pp.id:
                        new_bom_line = self.env['mrp.bom.line'].create({'bom_id':new_bom_id,
                                                                        'product_id':exist_pp.id,
                                                                        'quantity':value.quantity,
                                                                        })