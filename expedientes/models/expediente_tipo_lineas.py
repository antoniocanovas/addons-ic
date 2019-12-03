# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class ExpedienteTipoLineas(models.Model):
    _name = 'expediente.tipo.lineas'

    tipo_id = fields.Many2one('expediente.tipos',string='Tipo')
    tramite_id = fields.Many2one('expediente.tramites',
                                 domain=[('archivado','=',False)],string='Tramite',required=True)
    dependencia_ids = fields.Many2many('expediente.tramites',
                                 domain=[('archivado', '=', False)], string='Dependencia')

    def compute_get_name(self):
        for record in self:
            record['name'] = record.tipo_id.name + " => " + record.tramite_id.name

    name = fields.Char(string='Nombre', compute=compute_get_name, required=True, readonly=True)

    @api.depends('tramite_id')
    def compute_get_usuario(self):
        for record in self:
            record['usuario_id'] = record.tramite_id.usuario_id.id

    usuario_id = fields.Many2one('res.users', compute=compute_get_usuario, string='Usuario')

    @api.depends('tramite_id')
    def compute_get_departamento(self):
        for record in self:
            record['departamento_id'] = record.tramite_id.departamento_id.id

    departamento_id = fields.Many2one('hr.department',compute=compute_get_departamento, string='Departamento')

    @api.depends('tramite_id')
    def compute_get_intervalo(self):
        for record in self:
            record['intervalo'] = record.tramite_id.intervalo

    intervalo = fields.Integer(string='Intervalo',compute=compute_get_intervalo)
