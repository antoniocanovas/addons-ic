odoo.define('pos_table_state.PrintBillButton', function(require) {
    'use strict';

    const PrintBillButton = require('pos_restaurant.PrintBillButton');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    const POSPrintBillButton = PrintBillButton =>
		class extends PrintBillButton {
			async onClick() {
				super.onClick(...arguments);
	            var self = this;
	            _.each(this.env.pos.table_state, function (state) {
	                if (state.name == 'Pending Payment') {
	                    var currentdate = new Date();
						var datetime = currentdate.getDate() + "/"
						                + (currentdate.getMonth()+1)  + "/"
						                + currentdate.getFullYear() + " "
						                + currentdate.getHours() + ":"
						                + currentdate.getMinutes() + ":"
						                + currentdate.getSeconds();
						self.env.pos.table.state_id = [state.id, state.name]
						self.env.pos.table.time_pending_payment = datetime
						self.rpc({
		                    model: 'restaurant.table',
		                    method: 'update_table_state',
		                    args: [[], self.env.pos.table.id, 'Pending Payment', state.id, datetime],
		                });
	                }
	            });
	        }
		};

    Registries.Component.extend(PrintBillButton, POSPrintBillButton);

	return POSPrintBillButton;
});
