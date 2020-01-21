# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import base64

from odoo import fields, models, api


class Docs(models.Model):
    _name = 'docs.docs'
    _description = 'Docs for Expedients'

    name = fields.Char(string="Name")
    type_id = fields.Many2one('docs.types',string='Type',store=True)
    task_id = fields.Many2one('project.task', string='Task')
    project_id = fields.Many2one('project.project',related='task_id.project_id', string='Project')
    implied_ids = fields.Many2many('project.task.contacts', string='Implied')
    user_id = fields.Many2one('res.users', string='Salesman', track_visibility='onchange',
                              readonly=True, states={'draft': [('readonly', False)]},
                              default=lambda self: self.env.user, copy=False)


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

    body = fields.Html(string='Body', compute=_get_body_text,readonly=False,store=True)

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        return self.name + str(self.type_id.name)

    @api.multi
    def docs_print(self):
        """ Hace falta hacer seguimiento si el DOc ha sido enviado?
        """
        return self.env.ref('docs.docs_report').report_action(self)

    @api.multi
    def action_generate_attachment(self):

        # generate pdf from report, use report's id as reference
        report_id = 'docs.docs_report'
        pdf = self.env.ref(report_id).render_qweb_pdf(self.ids[0])
        # pdf result is a list
        b64_pdf = base64.b64encode(pdf[0])

        # save pdf as attachment
        name = self.name + (str(self.type_id.name))
        return self.env['ir.attachment'].create({
            'name': self.name,
            'type': 'binary',
            'datas': b64_pdf,
            'datas_fname': name + '.pdf',
            'store_fname': name,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/x-pdf'
        })

    @api.multi
    def action_docs_sent(self):
        self.ensure_one()
        template = self.env.ref('docs.email_template_edi_docs', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)

        attachment = self.action_generate_attachment()

        email_template = self.env.ref('docs.email_template_edi_docs')
        email_template.attachment_ids = False
        email_template.attachment_ids = [(6, 0,  [attachment.id])]

        ctx = dict(
            default_model='docs.docs',
            default_res_id=self.ids[0],
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            user_id=self.env.user.id,
            attachment_ids=[(6, 0,  [attachment.id])],
            #attachment_ids=[(4, attachment.id)],
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