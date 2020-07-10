# Copyright

from odoo import fields, models, api


class LogisticRouteLineWizard(models.TransientModel):
    _name = 'logistic.analysis.km'
    _description = 'Logistic Route Line Wizard To Calculate KM'

    name = fields.Char('Name')
    total_km = fields.Float('Km')
    logistic_route_line_id = fields.Many2one('fsm.logistic.route.line')


    @api.multi
    def equitative_km(self):
        for record in self:
        # En Ventaza Wizard botón "Repartir km":
            orders = len(record.logistic_route_line_id.fsm_order_ids.ids)
            if (orders > 0):
                km_per_order = record.total_km / orders
                for order in record.logistic_route_line_id.fsm_order_ids:
                    order['km'] = km_per_order

    @api.multi
    def distribute_km(self):
        for record in self:
        # Ventaza Wizard "Repartir km":
            trayecto = record.logistic_route_line_id
            orders = len(record.logistic_route_line_id.fsm_order_ids.ids)
            km_total = record.total_km
            km_orders = 0

            if orders > 0:
                for order in record.logistic_route_line_id.fsm_order_ids:
                    if not (order.location_id.parnter_id.id) or not (order.location_dest_id.id) or (
                            order.location_id.partner_id.km2origin == 0) or (order.location_dest_id.km2origin == 0):
                        raise Warning("Porte sin dirección o kilometraje desde base en recogida o entrega")
                    if (order.location_id.partner_id.km2origin > order.location_dest_id.km2origin):
                        distancia = order.location_id.partner_id.km2origin
                    else:
                        distancia = order.location_dest_id.km2origin
                    km_orders += distancia

                # Ahora que tenemos la distancia total de las sumas si fueran viajes sueltos, calculamos el reparto proporcional:
                for order in record.logistic_route_line_id.fsm_order_ids:
                    if (order.location_id.partner_id.km2origin > order.location_dest_id.km2origin):
                        distancia = order.location_id.partner_id.km2origin
                    else:
                        distancia = order.location_dest_id.km2origin
                    order['km'] = distancia / km_orders * km_total