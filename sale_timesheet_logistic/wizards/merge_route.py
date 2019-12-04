from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PartnerRouteMergeWizard(models.TransientModel):
    _name = "partner.route.merge.wizard"
    _description = "Merge Routes"

    name = fields.Char(
        string='Enter the name of the new route',
        required=True,
    )

    def merge_route(self):
        if not self._context.get('active_ids'):
            return {'type': 'ir.actions.act_window_close'}
        routes = self.env['res.partner.route'].browse(
            self._context['active_ids'])
        if len(routes) < 2:
            raise UserError(
                _('You must select two or more routes to merge.'))
        values = []
        for route in routes:
            for line in route.line_ids:
                values.append((0, 0, {
                    'origin_id': line.origin_id.id,
                    'delivery_id': line.delivery_id.id,
                }))
        if values:
            route = routes.create({
                'name': self.name,
                'line_ids': values,
            })
            ctx = dict(self.env.context)
            return {
                'name': _('New Route'),
                'view_mode': 'form,tree',
                'res_model': 'res.partner.route',
                'res_id': route.id,
                'type': 'ir.actions.act_window',
                'context': ctx,
            }
