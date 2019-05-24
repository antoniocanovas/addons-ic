# -*- coding: utf-8 -*-

from odoo import models, fields, api

class x_partner(models.Model):
    _inherit= 'res.partner'

    x_rgpd_informada_firmada_ids= fields.Many2many('x_rgpd_opciones', string="Clausulas registro firmadas")
    x_rgpd_informada_requerida_ids= fields.Many2many('x_rgpd_opciones', string="Clausulas registro requeridas")
    x_rgpd_tratamiento_firmada_ids= fields.Many2many('x_rgpd_opciones', string="Clausulas tratamiento firmadas")
    x_rgpd_tratamiento_requerida_ids= fields.Many2many('x_rgpd_opciones', string="Clausulas tratamiento requeridas")

    @api.depends('x_rgpd_informada_firmada_ids', 'x_rgpd_informada_requerida_ids')
    def informado_ok(self):
        for record in self:
            if record.x_rgpd_informada_firmada_ids == record.x_rgpd_informada_requerida_ids:
                record['x_rgpd_informado_ok'] = True
            else:
                record['x_rgpd_informado_ok'] = False


    @api.depends('x_rgpd_tratamiento_firmada_ids', 'x_rgpd_tratamiento_requerida_ids')
    def tratamiento_ok(self):
        for record in self:
            if record.x_rgpd_tratamiento_firmada_ids == record.x_rgpd_tratamiento_requerida_ids:
                record['x_rgpd_tratamiento_ok'] = True
            else:
                record['x_rgpd_tratamiento_ok'] = False


    @api.depends('x_rgpd_grupo_ids')
    def grupo_modificado(self):
        for record in self:
            record['x_rgpd_grupo_modificado'] = True


    x_rgpd_informado_ok = fields.Boolean(compute=informado_ok,string="Ok informado")
    x_rgpd_tratamiento_ok = fields.Boolean(compute=tratamiento_ok,string="Ok tratamiento")
    x_rgpd_grupo_ids = fields.Many2many('x_rgpd_grupos', string="Grupos")
    x_rgpd_grupo_modificado = fields.Boolean(string="Grupo modificado",compute=grupo_modificado)


