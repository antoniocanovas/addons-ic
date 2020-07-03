from odoo import fields, models, api


class FsmOrderLogistic(models.Model):
    _inherit = 'fsm.order'

    location_dest_id = fields.Many2one(
        relation='res.partner',
        related='sale_id.partner_shipping_id',
        string='Dir. de entrega',
        help='Delivery address for current sales order.'
    )

    date_open = fields.Datetime('Inicio actividad')
    date_close = fields.Datetime('Inicio actividad')

    @api.depends('location_dest_id', 'location_id', 'date_start', 'date_end')
    def _get_next_location(self):
        # Si no hay fecha de recogida, hay que ir a location_id, en caso contrario si no hay de entrega hay que ir a
        # x_location_dest_id, y si están ambas la ruta está hecha y este campo es nulo
        for record in self:
            sitio = False
            if (not record.date_start and not record.date_end):
                sitio = record.location_id.partner_id.id
            elif (record.date_start and not record.date_end):
                sitio = record.x_location_dest_id.id
            record['location_next_id'] = sitio

    location_next_id = fields.Many2one(
        relation='res.partner',
        string='Siguiente parada',
        compute=_get_next_location
    )

