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

    def action_view_password(self):
        action = {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Title",
                "message": "message",
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"},
            },
        }
        return action
