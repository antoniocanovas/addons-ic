# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api
import pyotp
import datetime


class PartnerCredential(models.Model):
    _name = "partner.credential"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Partner Credentials"

    name = fields.Char(string="Nombre", required=True, tracking=100)
    category_id = fields.Many2one('partner.credential.category', string="Category", required=True, tracking=100)
    partner_id = fields.Many2one("res.partner", string="Partner", tracking=100)
    user = fields.Char("User", tracking=100)
    active = fields.Boolean('Active', default=True)

    encrypted = fields.Encrypted()
    password = fields.Char("Password", encrypt='encrypted')

    url = fields.Char("Url", tracking=100)
    active = fields.Boolean("Active", default="True", tracking=100)
    description = fields.Text("Description")

    department_categ_ids = fields.Many2many(
        related='category_id.department_ids', string='Category deps.',
        help='Departments with access to view and modify, inherited from the category.'
    )
    department_ids = fields.Many2many(
        "hr.department", string="Addtional deps.", tracking=100,
        help='Additional departments with access to this credential (in addition to those in the category).'
    )

    key_2fa_secret = fields.Char("2FA Secret")

    def get_f2a_key(self):
        if self.key_2fa_secret:
            totp = pyotp.TOTP(self.key_2fa_secret)

            self.key_2fa = totp.now()
            self.key_2fa_time_remaining = totp.interval - datetime.datetime.now().timestamp() % totp.interval
        else:
            self.key_2fa = ""

    key_2fa = fields.Char("2FA Key", compute="get_f2a_key")
    key_2fa_time_remaining = fields.Integer("Validity (seconds)")

    @api.depends('password')
    def _get_pass_updated(self):
        for record in self:
            record['pass_updated'] = record.pass_updated +1
    pass_updated = fields.Integer("Password updated", store=True, tracking=100, compute="_get_pass_updated")

    """ Quitado 04/06/24, da error al entrar por primera vez como admin:
    def _get_allowed_categories(self):
        categories_obj = self.env['partner.credential.category'].search([])
        for credential in self:
            categ_list=[]
            for categories in categories_obj:
                if self.env.user.department_id in categories.department_ids:
                    categ_list.append(categories.id)
            credential['categ_ids'] = [(6, 0, categ_list)]

    categ_ids = fields.Many2many("partner.credential.category", string="Users", store=False, compute="_get_allowed_categories")
    """
    @api.depends('department_ids', 'department_ids.member_ids.user_id', 'department_categ_ids', 'department_categ_ids.member_ids.user_id')
    def _get_department_users(self):
        for record in self:
            users = []
            for dep in record.department_ids:
                for emp in dep.member_ids:
                    if (emp.user_id.id) and (emp.user_id.id not in users):
                        users.append(emp.user_id.id)
            for dep in record.department_categ_ids:
                for emp in dep.member_ids:
                    if (emp.user_id.id) and (emp.user_id.id not in users):
                        users.append(emp.user_id.id)
            record['user_ids'] = [(6, 0, users)]
    user_ids = fields.Many2many("res.users", string="Users", store=True, compute="_get_department_users")

    def _user_can_edit(self):
        for record in self:
            admin_group = self.env.ref('partner_credential.admin_credential_group')
            edit = False
            if (self.env.user == record.create_uid): edit = True
            if (admin_group.users.ids) and (self.env.user in admin_group.users): edit = True
            record['user_can_edit'] = edit
    user_can_edit = fields.Boolean('Edit', compute='_user_can_edit')

    def action_view_password(self):
        action = {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Copy quickly !!",
                "message": self.password,
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
        return action
