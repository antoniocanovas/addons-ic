# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
import datetime

class project(models.Model):
    _inherit = 'project.project'


    is_expedient = fields.Boolean(string='Es un expediente')
    expedient_type_id = fields.Many2one('expedient.type',domain=[('state','=','activo')],string='Tipo')
    departament_id = fields.Many2one('hr.department',string='Departamento')

    def compute_get_task(self):
        for record in self:
            tareas = self.env['project.task'].search(
                [('project_id', '=', record.id), '|', ('active', '=', False), ('active', '=', True)])
            record['task_ids'] = [(6, 0, tareas.ids)]

    task_ids = fields.Many2many('project.task', string='tarea', compute=compute_get_task, stored=False)

    def make_expedient(self):
        self.is_expedient = True

    @api.multi
    def create_case_tasks(self):
        for record in self:
            # Crear las tareas en base al tipo de expediente, enlazando cada tarea con su línea origen:
            # Si las tareas están archivadas y pulsamos de nuevo las repite, así que lo primero, sacar del archivo:
            exist = self.env['project.task'].search(
                [('project_id', '=', record.id), '|', ('active', '=', False), ('active', '=', True)])

            # Crear o actualizar añadiendo las etapas que faltan en el proyecto:
            #etapas_plantilla = record.expedient_type_id.stage_ids
            #for etapa in etapas_plantilla:
            #    record['type_ids'] = [(4, etapa.id)]

            # Crear o actualizar añadiendo las etapas que faltan en el proyecto:
        
            for e in record.expedient_type_id.stage_ids:
                record['type_ids'] = [(4, e.id)]

            # Las líneas del tipo de expediente que ya tienen tarea son:
            lineswithtask = []
            for ta in exist:
                if ta.expedient_line_id.id:
                    lineswithtask.append(ta.expedient_line_id.id)
            #
            # Buscamos las tareas que tendrían que haber y las creamos (por si se han borrado o ampliado el ámbito):
            for li in record.expedient_type_id.line_ids:
                if li.id not in lineswithtask:
                    nombre = record.name + " - " + li.procedure_id.name
                    nuevatarea = self.env['project.task'].create({'name': nombre,
                                                                  'project_id': record.id,
                                                                  'user_id': li.procedure_id.user_id.id,
                                                                  'departament_id': li.procedure_id.departament_id.id,
                                                                  'description': li.procedure_id.task_description,
                                                                  'active': True,
                                                                  'expedient_line_id': li.id})

            # Ahora las dependencias ya que tenemos todas las tareas de las líneas y podemos relacionar:
            todas = self.env['project.task'].search(
                [('project_id', '=', record.id), '|', ('active', '=', False), ('active', '=', True)])
            for ta in todas:
                if ta.expedient_line_id.dependency_ids.ids:
                    dependencias = []
                    for de in ta.expedient_line_id.dependency_ids:
                        tarea = self.env['project.task'].search(
                            [('expedient_line_id.procedure_id', '=', de.id), ('project_id', '=', record.id), '|',
                             ('active', '=', False), ('active', '=', True)])
                        dependencias.append(tarea.id)
                    ta['dependency_task_ids'] = [(6, 0, dependencias)]


                    # Archivar las nuevas tareas que tengan dependencias no cumplidas, por si se pulsa por segunda vez el botón "Actualizar trámites":
                    # Respeta las existentes de antes por si hemos querido adelantar algún trámite manualmente:
                if (ta.id not in exist.ids) and (ta.expedient_line_id.id) and (
                            ta.expedient_line_id.dependency_ids.ids):
                    activo = True
                    for de in ta.expedient_line_id.dependency_ids:
                        tarea_en_proyecto = self.env['project.task'].search(
                            [('id', 'in', todas.ids), ('expedient_line_id', '=', de.id)])
                        if (tarea_en_proyecto.stage_id.closed == False):
                            activo = False
                        ta['active'] = activo

            # Ahora las fechas límite:
            for ta in todas:
                diaobjetivo = 0
                if (ta.expedient_line_id.id) and (
                        ta.id not in exist.ids):  # <= Para permitir crear otras tareas manualmente, y mantener fechas límite si varios clicks
                    if ta.expedient_line_id.interval < 7:
                        diadelasemanahoy = datetime.date.today().strftime("%w")
                        diaobjetivo = int(diadelasemanahoy) + ta.expedient_line_id.interval
                        if diaobjetivo > 5:
                            interval = ta.expedient_line_id.interval + 2
                        else:
                            interval = ta.expedient_line_id.interval
                    else:
                        interval = ta.expedient_line_id.interval
                    fecha = datetime.datetime.today() + datetime.timedelta(days=interval)

                    ta['date_deadline'] = fecha.date()

            # Cambiar la etiqueta de las tareas en base a la plantilla:
            if record.expedient_type_id.task_name:
                record['label_tasks'] = record.expedient_type_id.task_name

