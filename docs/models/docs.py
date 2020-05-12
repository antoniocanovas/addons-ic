# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning


class Docs(models.Model):
    _name = 'docs.docs'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Docs for Expedients'

    name = fields.Char(string="Name")
    type_id = fields.Many2one('docs.types',string='Type',store=True)
    task_id = fields.Many2one('project.task', string='Task')
    project_id = fields.Many2one('project.project', related='task_id.project_id', string='Project')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment', readonly=True)
    attachment_datas = fields.Binary(string='Attachment')
    attachment_name = fields.Char(string='Attachment Name')
    implied_ids = fields.Many2many('project.task.contacts', string='Implied')
    is_public = fields.Boolean('Es público')
    user_id = fields.Many2one(
        'res.users',
        string='Salesman',
        track_visibility='onchange',
        readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user, copy=False
    )
    state = fields.Selection(
        [
            ('draft', 'DRAFT'),
            ('validated', 'VALIDATED'),
        ],
        default='draft',
        string='State',
        track_visibility='always',
    )

    @api.depends('type_id')
    def _get_intro_text(self):
        for record in self:
            record['header'] = record.type_id.header_id.text

    header = fields.Html(string='Header',compute=_get_intro_text,readonly=False, store=True)

    @api.depends('type_id')
    def _get_footer_text(self):
        for record in self:
            record['footer'] = record.type_id.footer_id.text

    footer = fields.Html(string='Footer', compute=_get_footer_text, readonly=False, store=True)

    @api.depends('type_id')
    def _get_body_text(self):
        for record in self:
            record['body'] = record.type_id.body_id.text

    body = fields.Html(string='Body', compute=_get_body_text, readonly=False, store=True)

    @api.multi
    def preview_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }

    def _compute_access_url(self):
        super(Docs, self)._compute_access_url()
        for doc in self:
            doc.access_url = '/my/docs/%s' % (doc.id)

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return "Docs" + self.name + str(self.type_id.name)

    @api.multi
    def action_generate_attachment(self):
        if self.state == 'draft':
            # generate pdf from report, use report's id as reference
            report_id = 'docs.docs_report'
            pdf = self.env.ref(report_id).render_qweb_pdf(self.ids[0])
            # pdf result is a list
            b64_pdf = base64.b64encode(pdf[0])
            main_attachment = self.env['ir.attachment'].sudo().search(
                ['&', ('res_id', '=', self.id), ('name', '=', self.type_id.name + '.pdf')]
            )
            main_attachment.unlink()
            # save pdf as attachment
            name = self.name + (str(self.type_id.name))
            self.attachment_id = self.env['ir.attachment'].sudo().create({
                'name': name + '.pdf',
                'type': 'binary',
                'datas': b64_pdf,
                'datas_fname': name + '.pdf',
                'store_fname': name,
                'res_model': 'project.task',
                'res_id': self.task_id,
                'mimetype': 'application/pdf'
            })
            self.attachment_datas = self.attachment_id.datas
            self.attachment_name = self.attachment_id.datas_fname
            self.state = 'validated'

        else:
            main_attachment = self.env['ir.attachment'].sudo().search(
                ['&', ('res_id', '=', self.id), ('name', '=', self.type_id.name + '.pdf')]
            )
            main_attachment.unlink()
            self.attachment_id.unlink()
            self.state = 'draft'

    @api.multi
    def action_docs_sent(self):
        self.ensure_one()

        if self.state == 'draft':
            raise Warning((
                "PLease validate this docs before send"
            ))
        else:
            template = self.env.ref('docs.email_template_edi_docs', False)
            compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)

            attachment = self.attachment_id
            email_template = self.env.ref('docs.email_template_edi_docs')

            email_template.attachment_ids = [(4, attachment.id)]

            ctx = dict(
                default_model='docs.docs',
                default_res_id=self.ids[0],
                default_use_template=bool(template),
                default_template_id=template and template.id or False,
                default_composition_mode='comment',
                user_id=self.env.user.id,
            )

            return {
                'name': ('Send Doc'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(compose_form.id, 'form')],
                'view_id': compose_form.id,
                'target': 'new',
                'context': ctx,
            }