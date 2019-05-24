# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from odoo import models, fields, api


class x_rgpd_rats(models.Model):
    _name = "x_rgpd_rats"
    _description = "RGPD rats"

    x_name = fields.Char(string="Nombre", required=True)

    x_interesado_id = fields.Many2one('x_rgpd_grupos',string="Grupo interesados")
    x_descripcion = fields.Text(string="Descripción")
    x_estado = fields.Selection(selection=[('borrador', 'Borrador'), ('activo', 'Activo'), ('archivado', 'Archivado')],
                                string="Estado", default='activo')
    #x_grupo_ids = fields.Many2many('x_rgpd_grupos', relation='x_rgpd_grupo_x_rgpd_rats_rel',column1='x_rgps_rats_id',
    #                               column2='x_rgpd_grupos_id',string="Grupos")
    x_grupo_ids = fields.Many2many('x_rgpd_grupos', relation='x_rgpd_grupo_x_rgpd_rats_rel', column1='x_rgps_rats_id',
                                                                 column2='x_rgpd_grupos_id',string="Grupos")


    ##### RES.PARTNER #########
    x_cedido_ids = fields.Many2many('res.partner', domain=[('supplier','=',True)],string="Cesiones")
    x_empleado_ids = fields.Many2many('res.partner', domain=[('is_company','=',False)],string="Empleados RT")
    x_responsable_empresa_id = fields.Many2one('res.partner', domain=[('is_company','=',True)],string="Propietario")
    x_usuario_ids = fields.Many2many('res.partner', stored=False,string="Usuarios")
    x_responsable_delegado_id = fields.Many2one('res.partner', domain=[('is_company','=',False)],string="Responasable delegado")
    ##### RES.USER######

    x_responsable_tratamiento_id = fields.Many2one('res.partner', domain=[('is_company', '=', False)], string="Responsable tratamiento")
    x_responsable_funcional_id = fields.Many2one('res.partner', domain=[('is_company', '=', False)], string="Responsable funcional")
    ##### Mail list #####

    x_lista_id = fields.Many2one('mail.channel', string="Lista de comunicaciones")

    x_rango_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','rango')],string="Núm de registros")
    x_sensible_ids = fields.Many2many('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','sensible')],string="Datos sensibles")
    x_ambito_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','ambito')],string="Ámbito geográfico")
    x_analizado_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','analizado')],string="Análisis de perfiles")
    x_vulnerable_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','vulnerable')],string="Grupos vulnerables")
    x_uso_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','uso')],string="Uso de la información")
    x_origen_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','origen')],string="Origen de la información")
    x_recopilado_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','recopilacion')],string="Modo recogida")
    x_consentimiento_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','consentimiento')],string="Solicitud de consentimiento")
    x_ejercer_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','ejercimiento')],string="Método de Ejercimiento de derechos RGPD")
    x_europa_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','europa')],string="Localiación UE")
    x_conservado_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','conservado')],string="Cancelación")
    x_tratado_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','tratamiento')],string="Gestión")
    x_baselegal_id = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','baselegal')],string="Base legal")
    x_alojado_ids = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','alojado')],string="Alojados")
    x_accesible_ids = fields.Many2one('x_rgpd_opciones', domain=[('x_tipo_id.x_codigo','=','accesible')],string="Dispositivos y medios")\

    @api.multi
    def calcula_medida(self):
        for record in self:
            todas = []
            if record.create_date:
                for me in record.x_rango_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_consentimiento_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_uso_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_vulnerable_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_ejercer_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_baselegal_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_recopilado_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_alojado_ids.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_ambito_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_europa_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_origen_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_analizado_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_tratado_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_conservado_id.x_medida_ids:
                    todas.append(me.id)
                for me in record.x_accesible_ids.x_medida_ids:
                    todas.append(me.id)

                for se in record.x_sensible_ids:
                    for me in se.x_medida_ids:
                        todas.append(me.id)

                record['x_medida_ids'] = [(6, 0, todas)]

    @api.multi
    def clausula_informativa(self):
        for record in self:
            todas = []
            if record.create_date:
                if record.x_rango_id.x_clausula_informativa:
                    todas.append(record.x_rango_id.id)
                if record.x_consentimiento_id.x_clausula_informativa:
                    todas.append(record.x_consentimiento_id.id)
                if record.x_uso_id.x_clausula_informativa:
                    todas.append(record.x_uso_id.id)
                if record.x_vulnerable_id.x_clausula_informativa:
                    todas.append(record.x_vulnerable_id.id)
                if record.x_ejercer_id.x_clausula_informativa:
                    todas.append(record.x_ejercer_id.id)
                if record.x_baselegal_id.x_clausula_informativa:
                    todas.append(record.x_baselegal_id.id)
                if record.x_recopilado_id.x_clausula_informativa:
                    todas.append(record.x_recopilado_id.id)
                if record.x_alojado_ids.x_clausula_informativa:
                    todas.append(record.x_rango_id.id)
                if record.x_ambito_id.x_clausula_informativa:
                    todas.append(record.x_ambito_id.id)
                if record.x_europa_id.x_clausula_informativa:
                    todas.append(record.x_europa_id.id)
                if record.x_origen_id.x_clausula_informativa:
                    todas.append(record.x_origen_id.id)
                if record.x_analizado_id.x_clausula_informativa:
                    todas.append(record.x_analizado_id.id)
                if record.x_tratado_id.x_clausula_informativa:
                    todas.append(record.x_tratado_id.id)
                if record.x_conservado_id.x_clausula_informativa:
                    todas.append(record.x_conservado_id.id)
                if record.x_accesible_ids.x_clausula_informativa:
                    todas.append(record.x_accesible_ids.id)
                for se in record.x_sensible_ids:
                    if se.x_clausula_informativa:
                        todas.append(se.id)

                record['x_clausula_informativa_ids'] = [(6, 0, todas)]

    @api.multi
    def clausula_tratamiento(self):
        for record in self:
            todas = []
            if record.create_date:
                if record.x_rango_id.x_clausula_tratamiento:
                    todas.append(record.x_rango_id.id)
                if record.x_consentimiento_id.x_clausula_tratamiento:
                    todas.append(record.x_consentimiento_id.id)
                if record.x_uso_id.x_clausula_tratamiento:
                    todas.append(record.x_uso_id.id)
                if record.x_vulnerable_id.x_clausula_tratamiento:
                    todas.append(record.x_vulnerable_id.id)
                if record.x_ejercer_id.x_clausula_tratamiento:
                    todas.append(record.x_ejercer_id.id)
                if record.x_baselegal_id.x_clausula_tratamiento:
                    todas.append(record.x_baselegal_id.id)
                if record.x_recopilado_id.x_clausula_tratamiento:
                    todas.append(record.x_recopilado_id.id)
                if record.x_alojado_ids.x_clausula_tratamiento:
                    todas.append(record.x_rango_id.id)
                if record.x_ambito_id.x_clausula_tratamiento:
                    todas.append(record.x_ambito_id.id)
                if record.x_europa_id.x_clausula_tratamiento:
                    todas.append(record.x_europa_id.id)
                if record.x_origen_id.x_clausula_tratamiento:
                    todas.append(record.x_origen_id.id)
                if record.x_analizado_id.x_clausula_tratamiento:
                    todas.append(record.x_analizado_id.id)
                if record.x_tratado_id.x_clausula_tratamiento:
                    todas.append(record.x_tratado_id.id)
                if record.x_conservado_id.x_clausula_tratamiento:
                    todas.append(record.x_conservado_id.id)
                if record.x_accesible_ids.x_clausula_tratamiento:
                    todas.append(record.x_accesible_ids.id)
                for se in record.x_sensible_ids:
                    if se.x_clausula_tratamiento:
                        todas.append(se.id)

                record['x_clausula_tratamiento_ids'] = [(6, 0, todas)]



    x_clausula_informativa_ids = fields.Many2many('x_rgpd_opciones', compute=clausula_informativa,string="Cláusulas informativas", stored=False)
    x_clausula_tratamiento_ids = fields.Many2many('x_rgpd_opciones', compute=clausula_tratamiento,string="Cláusulas tratamiento", stored=False)

    x_medida_ids = fields.Many2many('x_rgpd_medidas',
                                    string="Cáculo no almacenado de todas la medidas sin repetir de las opciones",
                                    compute=calcula_medida, store=False)
