odoo.define('pos_table_state.floors', function(require) {
    'use strict';

    var models = require('point_of_sale.models');
    var _super_PosModel = models.PosModel.prototype;

    models.PosModel = models.PosModel.extend({
	        add_new_order: function() {
	            _super_PosModel.add_new_order.apply(this, arguments);
                var self = this;
                _.each(this.env.pos.table_state, function (state) {
                    if (state.name == 'New') {
                        var currentdate = new Date();
						var datetime = currentdate.getDate() + "/"
						                + (currentdate.getMonth()+1)  + "/"
						                + currentdate.getFullYear() + " "
						                + currentdate.getHours() + ":"
						                + currentdate.getMinutes() + ":"
						                + currentdate.getSeconds();
						self.table.state_id = [state.id, state.name]
						self.table.time_start = datetime
						self.rpc({
		                    model: 'restaurant.table',
		                    method: 'update_table_state',
		                    args: [[], self.table.id, 'New', state.id, datetime],

		                });
                    }
                });
	        }
    });
});

