# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api
from .common import IMAGE_PLACEHOLDER

# Used to render html field in TreeView
TREE_TEMPLATE = (
    '<table style="width:100%%;border:none;" title="table">'
    "<tbody>"
    "<tr>"
    #'<td style="width: 0%%;"><img class="rounded-circle"'
    #' style="width: 64px; padding:10px;" src="data:image/png;base64,%s"'
    #' alt="Avatar" title="%s" width="100" border="0" /></td>'
    #'<td style="width: 100%%;">'
    '<td style="width: 0%%;"></td>'
    '<table style="width: 100%%; border: none;">'
    "<tbody>"
    "<tr>"
    '<td id="name" style="font-size: 16px;vertical-align:top;"><strong><span id="name">%s</span></strong>  &nbsp; <span id="responsible">[%s]</span></td></td>'
    '<td id="customer" style="text-align:right;"><strong><span title="%s" id="customer">%s</span></strong></td>'
    "</tr>"
)

class ProjectProject(models.Model):
    _inherit = 'project.project'

    roadmap_ids = fields.One2many('project.roadmap', 'project_id', string='Etapas')
    roadmap_count = fields.Integer('Roadmaps not hidden', compute="_compute_roadmap_count", store=False)
    @api.depends("roadmap_ids.hidden")
    def _compute_roadmap_count(self):
        for rec in self:
            total = 0
            roadmaps = self.env['project.roadmap'].search([('id' in roadmap_ids.ids),('hidden','=',False)])
            if roadmaps.ids: total = len(roadmaps.ids)
        rec['roadmap_count'] = total

    project_user_avatar = fields.Binary(string="Avatar", readonly=False, related="user_id.image_128")
    project_roadmap_display = fields.Html(string="Project Roadmap", compute="_compute_project_display")

    @api.depends("roadmap_ids")
    def _compute_project_display(self):

        # Compose subject
        for rec in self:
            roadmap_template = (
                ""
            )
            #    "<tr>"
            #    '<td><strong>Responsable</strong></td>'
            #    '<td><strong>Nombre</strong></td>'
            #    '<td><strong>Tipo</strong></td>'
            #    '<td><strong>Fecha Límite</strong></td>'
            #    '<td><strong>Estado</strong></td>'
            #    '</tr>'
            #)

            for roadmap in rec.roadmap_ids:
                if roadmap.hidden == False:
                    roadmap_template += (
                        '<tr>'
                        '<td style="font-size: 12px;">[%s] %s : %s </td>' 
                        '<td  style="text-align:right;font-size: 12px;"> %s (%s), %s </td>'
                        '</tr>' % (
                            roadmap.priority if roadmap.priority else '',
                            roadmap.type if roadmap.type else '',
                            roadmap.name if roadmap.name else '',
                            roadmap.user_id.name if roadmap.user_id.name else '',
                            roadmap.state if roadmap.state else '',
                            roadmap.date_limit if roadmap.date_limit else '',
                        )
                    )

            roadmap_template += (
                "</td>"
                "</tr>"
                "</tbody>"
                "</table>"
            )
            rec.project_roadmap_display = TREE_TEMPLATE % (
                #rec.project_user_avatar.decode("utf-8") if rec.project_user_avatar
                #else IMAGE_PLACEHOLDER,
                #rec.user_id.name,
                rec.name,
                rec.partner_id.name if rec.partner_id else '',
                rec.user_id.name if rec.user_id else '',
                rec.user_id.name if rec.user_id else '',

            ) + roadmap_template
