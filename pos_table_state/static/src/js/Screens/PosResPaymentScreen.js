odoo.define('pos_table_state.PosResPaymentScreen111', function(require) {
    'use strict';

    const PosResPaymentScreen = require('pos_restaurant.PosResPaymentScreen');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const CustomPosResPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {

	        async _finalizeValidation() {
	            super._finalizeValidation(...arguments);
	            var self = this;
	            _.each(this.env.pos.table_state, function (state) {
	                if (state.name == 'Done') {
	                    var currentdate = new Date();
						var datetime = currentdate.getDate() + "/"
				                + (currentdate.getMonth()+1)  + "/"
				                + currentdate.getFullYear() + " "
				                + currentdate.getHours() + ":"
				                + currentdate.getMinutes() + ":"
				                + currentdate.getSeconds();
						self.env.pos.table.state_id = [state.id, state.name]
						self.env.pos.table.time_done = datetime
						self.rpc({
		                    model: 'restaurant.table',
		                    method: 'update_table_state',
		                    args: [[], self.env.pos.table.id, 'Done', state.id, datetime],
		                });
	                }
	            });
	        }
    };
    Registries.Component.extend(PaymentScreen, CustomPosResPaymentScreen);

    return CustomPosResPaymentScreen;
});

