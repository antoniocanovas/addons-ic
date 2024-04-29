# Copyright
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class PartnerCredentials(models.Model):
    _name = "partner.credentials"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Partner Credentials"

    name = fields.Char(string="Nombre", required=True)
    type = fields.Selection(
        [("odoo", "Odoo"), ("web", "Web"), ("other", "Other")], required=True
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    user = fields.Char("User")
    password = fields.Char("Password")
    public = fields.Boolean("Public")
    url = fields.Char("Url")
    active = fields.Boolean("Active", default="True")
    description = fields.Text("Description")
    department_ids = fields.Many2many("hr.department", string="Departments")

    @api.depends('department_ids', 'department_ids.member_ids')
    def _get_department_users(self):
        users = []
        for dep in self.department_ids:
            for emp in dep.member_ids:
                if emp.user_id.id not in users:
                    users.append(emp.user_id.id)
        self.user_ids = [(6,0,users)]
    user_ids = fields.Many2many("res.users", string="Users", compute="_get_department_users")

    def _user_can_edit(self):
        admin_group = self.env.ref('partner_credentials.admin_credentials_group')
        for record in self:
            editable = False
            if (self.user.id == record.create_uid): editable = True
            if (self.user.id in admin_group.user_ids.ids): editable = True
            record['user_can_edit'] = editable
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
