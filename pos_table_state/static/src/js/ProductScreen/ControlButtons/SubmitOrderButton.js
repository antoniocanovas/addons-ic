odoo.define('pos_table_state.SubmitOrderButton', function(require) {
    'use strict';

    const SubmitOrderButton = require('pos_restaurant.SubmitOrderButton');
    const Registries = require('point_of_sale.Registries');
    var models = require('point_of_sale.models');
    var _super_posmodel = models.PosModel.prototype;

    const SubmitOrderButtonColorChange = (SubmitOrderButton) =>
        class extends SubmitOrderButton {

	        async onClick() {
	            super.onClick(...arguments);
	            var self = this;
	            _.each(this.env.pos.table_state, function (state) {
	                if (state.name == 'Waiting Order') {
	                    var currentdate = new Date();
						var datetime = currentdate.getDate() + "/"
						                + (currentdate.getMonth()+1)  + "/"
						                + currentdate.getFullYear() + " "
						                + currentdate.getHours() + ":"
						                + currentdate.getMinutes() + ":"
						                + currentdate.getSeconds();
						self.env.pos.table.state_id = [state.id, state.name]
						self.env.pos.table.time_waiting_order = datetime
						self.rpc({
		                    model: 'restaurant.table',
		                    method: 'update_table_state',
		                    args: [[], self.env.pos.table.id, 'Waiting Order', state.id, datetime],

		                });
	                }
	            });
	        }
    };
    Registries.Component.extend(SubmitOrderButton, SubmitOrderButtonColorChange);

    return SubmitOrderButtonColorChange;
});

