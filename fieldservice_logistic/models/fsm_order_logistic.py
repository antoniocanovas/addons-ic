from odoo import fields, models, api


class FsmOrderLogistic(models.Model):
    _inherit = 'fsm.order'

    km = fields.Float('Kilómetros')
    kg = fields.Float('Kg')
    units = fields.Float('Unidades')

    location_dest_id = fields.Many2one(
        'res.partner',
        related='sale_id.partner_shipping_id',
        string='Dir. de entrega',
        help='Delivery address for current sales order.'
    )

    stage_external_id = fields.Char(
        related ='stage_id.external_id',
        string = 'Estado FSM',
        store = True,
    )

    @api.onchange('vehicle_id')
    def get_logistic_route_domain(self):
        for record in self:
            return {'domain': {'logistic_route_line_id': [('active','=',True),('fsm_vehicle_id','!=',False),('fsm_vehicle_id','=', record.vehicle_id.id)]}}

    logistic_route_line_id = fields.Many2one('fsm.logistic.route.line', string='Trayecto')

    date_up = fields.Datetime('Cargardo', track_visibility='onchange')
    date_down = fields.Datetime('Descargado', track_visibility='onchange')

    @api.depends('location_dest_id', 'location_id', 'date_up', 'date_down')
    def _get_next_location(self):
        # Si no hay fecha de recogida, hay que ir a location_id, en caso contrario si no hay de entrega hay que ir a
        # x_location_dest_id, y si están ambas la ruta está hecha y este campo es nulo
        for record in self:
            if (not record.date_up and not record.date_down):
                record['location_next_id'] = record.location_id.partner_id.id
            elif (record.date_up and not record.date_down):
                record['location_next_id'] = record.location_dest_id.id

    location_next_id = fields.Many2one(
        'res.partner',
        string='Siguiente parada',
        compute=_get_next_location
    )


    location_next_latitude = fields.Float(related='location_next_id.partner_latitude', stored='False')
    location_next_longitude = fields.Float(related='location_next_id.partner_longitude', stored='False')
    location_next_country = fields.Char(related='location_next_id.country_id.name', stored='False')


    @api.multi
    def delivered_collected(self):
        #self.ensureone()
        #Traido de V13
        for porte in self:
            if porte.date_up:
                porte.date_down = fields.datetime.now()
            else:
                porte.date_up = fields.datetime.now()

    def action_complete_auto(self):
        self.date_end = fields.datetime.now()
        self.action_complete()

    def action_start_auto(self):
        self.date_start = fields.datetime.now()
        self.action_start()

