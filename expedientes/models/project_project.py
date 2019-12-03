# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
import datetime

class project(models.Model):
    _inherit = 'project.project'


    es_expediente = fields.Boolean(string='Es un expediente')
    tipo_expediente_id = fields.Many2one('expediente.tipos',dominio=[('estado','=','activo')],string='Tipo')
    departamento_id = fields.Many2one('hr.department',string='Departamento')

    def compute_get_tareas(self):
        for record in self:
            tareas = self.env['project.task'].search(
                [('project_id', '=', record.id), '|', ('active', '=', False), ('active', '=', True)])
            record['tarea_ids'] = [(6, 0, tareas.ids)]

    tarea_ids = fields.Many2many('project.task', string='tarea', compute=compute_get_tareas, stored=False)

    def make_expediente(self):
        self.es_expediente = True

    @api.multi
    def create_case_tasks(self):
        for record in self:
            # Crear las tareas en base al tipo de expediente, enlazando cada tarea con su línea origen:
            # Si las tareas están archivadas y pulsamos de nuevo las repite, así que lo primero, sacar del archivo:
            existen = self.env['project.task'].search(
                [('project_id', '=', record.id), '|', ('active', '=', False), ('active', '=', True)])

            # Las líneas del tipo de expediente que ya tienen tarea son:
            lineascontarea = []
            for ta in existen:
                if ta.linea_expediente_id.id:
                    lineascontarea.append(ta.linea_expediente_id.id)
            #
            # Buscamos las tareas que tendrían que haber y las creamos (por si se han borrado o ampliado el ámbito):
            for li in record.tipo_expediente_id.linea_ids:
                if li.id not in lineascontarea:
                    nombre = record.name + " - " + li.tramite_id.name
                    nuevatarea = self.env['project.task'].create({'name': nombre,
                                                         'project_id': record.id,
                                                         'user_id': li.tramite_id.usuario_id.id,
                                                         'departamento_id': li.tramite_id.departamento_id.id,
                                                         'description': li.tramite_id.descripcion_tarea,
                                                         'active': True,
                                                         'linea_expediente_id': li.id})

            # Ahora las dependencias ya que tenemos todas las tareas de las líneas y podemos relacionar:
            todas = self.env['project.task'].search(
                [('project_id', '=', record.id), '|', ('active', '=', False), ('active', '=', True)])
            for ta in todas:
                if ta.linea_expediente_id.dependencia_ids.ids:
                    dependencias = []
                    for de in ta.linea_expediente_id.dependencia_ids:
                        tarea = self.env['project.task'].search(
                            [('linea_expediente_id.tramite_id', '=', de.id), ('project_id', '=', record.id), '|',
                             ('active', '=', False), ('active', '=', True)])
                        dependencias.append(tarea.id)
                    ta['dependency_task_ids'] = [(6, 0, dependencias)]
                if (
                        ta.id not in existen.ids):  # <= Por si se pulsa el botón segunda vez, que no se archiven las que se activaron manualmente
                    ta['active'] = False

            # Ahora las fechas límite:
            for ta in todas:
                diaobjetivo = 0
                if (ta.linea_expediente_id.id) and (
                        ta.id not in existen.ids):  # <= Para permitir crear otras tareas manualmente, y mantener fechas límite si varios clicks
                    if ta.linea_expediente_id.intervalo < 7:
                        diadelasemanahoy = datetime.date.today().strftime("%w")
                        diaobjetivo = int(diadelasemanahoy) + ta.linea_expediente_id.intervalo
                        if diaobjetivo > 5:
                            intervalo = ta.linea_expediente_id.intervalo + 2
                        else:
                            intervalo = ta.linea_expediente_id.intervalo
                    else:
                        intervalo = ta.linea_expediente_id.intervalo
                    fecha = datetime.datetime.today() + datetime.timedelta(days=intervalo)

                    ta['date_deadline'] = fecha.date()

            # Cambiar la etiqueta de las tareas en base a la plantilla:
            if record.tipo_expediente_id.nombre_tarea:
                record['label_tasks'] = record.tipo_expediente_id.nombre_tarea

