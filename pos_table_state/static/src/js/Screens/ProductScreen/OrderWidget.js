odoo.define('pos_table_state.OrderWidget', function(require) {
    'use strict';

    const OrderWidget = require('point_of_sale.OrderWidget');
    const Registries = require('point_of_sale.Registries');

    const POSOrderWidget = (OrderWidget) =>
        class extends OrderWidget {
            get order() {
                var self = this;
                if(this.env.pos.get_order() && self.env.pos.get_order().table){
                    self.env.pos.get_order().table.amount = self.env.pos.get_order() ? self.env.pos.get_order().get_total_with_tax() : 0;
                    self.rpc({
                        model: 'restaurant.table',
                        method: 'update_table_order_total',
                        args: [[], self.env.pos.get_order().table.id, self.env.pos.get_order().table.amount],
                    });
                }
                return super.order;
            }
//            get order() {
//                var self = this;
//	            self.env.pos.get_order().table.amount = self.env.pos.get_order() ? self.env.pos.get_order().get_total_with_tax() : 0;
//	            self.rpc({
//                    model: 'restaurant.table',
//                    method: 'update_table_order_total',
//                    args: [[], self.env.pos.get_order().table.id, self.env.pos.get_order().table.amount],
//                });
//	            return super.order;
//	        }
    };
    Registries.Component.extend(OrderWidget, POSOrderWidget);

    return POSOrderWidget;
});

