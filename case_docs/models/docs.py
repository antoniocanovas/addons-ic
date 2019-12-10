# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models, api


class Docs(models.Model):
    _name = 'docs.docs'
    _description = 'Docs en Expedientes'

    name = fields.Char(string="Nombre")
    type_id = fields.Many2one('docs.types',string='Tipo')
    task_id = fields.Many2one('project.task', string='Tarea')
    project_id = fields.Many2one('project.project',related='task_id.project_id', string='proyecto')
    implied_ids = fields.Many2many('project.task.contacts', string='Implicados')

    @api.depends('type_id')
    def _get_intro_text(self):
        for record in self:
            record['intro'] = record.type_id.intro_id.text

    intro = fields.Html(string='Intro',compute=_get_intro_text,readonly=False,store=True)

    @api.depends('type_id')
    def _get_footer_text(self):
        for record in self:
            record['footer'] = record.type_id.footer_id.text

    footer = fields.Html(string='Footer', compute=_get_footer_text, readonly=False,store=True)

    @api.depends('type_id')
    def _get_body_text(self):
        for record in self:
            record['body'] = record.type_id.body_id.text

    body = fields.Html(string='body', compute=_get_body_text,readonly=False,store=True)

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return 'DOCS' + self.name + str(self.type_id)

    @api.multi
    def action_docs_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref('docs.email_template_edi_docs', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='docs.docs',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            #mark_invoice_as_sent=True,
            #custom_layout="account.mail_template_data_notification_email_account_invoice",
            force_email=True
        )
        return {
            'name': ('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

class ReportDocs(models.AbstractModel):
    _name = 'report.docs.docs'
    _description = 'Docs Reporting'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'docs.docs',
            'docs': self.env['docs.docs'].browse(docids),
            'report_type': data.get('report_type') if data else '',
        }