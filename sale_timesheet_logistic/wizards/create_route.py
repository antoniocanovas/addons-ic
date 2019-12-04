from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PartnerRouteWizard(models.TransientModel):
    _name = "partner.route.wizard"
    _description = "Create routes from sale order lines"

    name = fields.Char(
        string='Enter the name of the new route',
        required=True,
    )

    def create_route(self):
        if not self._context.get('active_id'):
            return {'type': 'ir.actions.act_window_close'}
        sale = self.env['sale.order'].browse(self._context['active_id'])
        routes = self.env['res.partner.route']
        if sale:
            origins = sale.mapped('order_line').filtered(lambda x: x.origin_id)
            deliveries = sale.mapped('order_line').filtered(
                lambda x: x.delivery_id)
            if not sale.mapped('order_line.product_id').filtered(
                    lambda x: x.type == 'service'):
                raise UserError(
                    _('Routes only can be defined with service products.'))
            if not origins and not deliveries:
                raise UserError(_('You must have lines with origin and '
                                  'delivery points.'))
            if origins != deliveries:
                raise UserError(_('You must define origin and delivery points '
                                  'in every line.'))
            values = []
            for line in origins:
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

    @api.model
    def default_get(self, fields):
        sale = self.env['sale.order'].browse(self._context['active_id'])
        result = super().default_get(fields)
        if sale:
            result['name'] = _('Route %s') % sale.name
        return result
