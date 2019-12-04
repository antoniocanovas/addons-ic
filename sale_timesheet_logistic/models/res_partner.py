from odoo import fields, models


class ResPartnerRoute(models.Model):
    _name = 'res.partner.route'
    _description = 'Routes of the partners'

    name = fields.Char(
        string='Route',
        required=True,
    )
    note = fields.Html()
    line_ids = fields.One2many(
        comodel_name='res.partner.route.line',
        inverse_name='route_id',
        string='Route_lines',
        copy=True,
        auto_join=True,
    )
    active = fields.Boolean(
        default=True,
    )


class ResPartnerRouteLine(models.Model):
    _name = 'res.partner.route.line'
    _description = 'Route lines'
    _order = 'sequence'

    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    origin_id = fields.Many2one(
        comodel_name='res.partner',
        string='Collection Point',
        required=True,
    )
    delivery_id = fields.Many2one(
        comodel_name='res.partner',
        string='Delivery Point',
        required=True,
    )
    route_id = fields.Many2one(
        comodel_name='res.partner.route',
        string='Route',
        required=True,
        ondelete='cascade',
        index=True,
    )
