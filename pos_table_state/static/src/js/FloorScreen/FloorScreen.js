odoo.define('pos_table_state.floors', function(require) {
    'use strict';

    var models = require('point_of_sale.models');
    const { Gui } = require('point_of_sale.Gui');
    const { posbus } = require('point_of_sale.utils');
    var _super_posmodel = models.PosModel.prototype;

    models.PosModel = models.PosModel.extend({
        add_new_order: function() {
            if (this.config.iface_floorplan) {
                if (this.table) {
                    _super_posmodel.add_new_order.apply(this, arguments);
                    var self = this;
                    _.each(this.env.pos.table_state, function (state) {
                        if (state.name == 'New' && self.table) {
                            var currentdate = new Date();
                            var datetime = currentdate.getDate() + "/"
                                            + (currentdate.getMonth()+1)  + "/"
                                            + currentdate.getFullYear() + " "
                                            + currentdate.getHours() + ":"
                                            + currentdate.getMinutes() + ":"
                                            + currentdate.getSeconds();
                            var datetime1 = currentdate.getHours() + ":" + currentdate.getMinutes();
                            self.table.state_id = [state.id, state.name]
                            self.table.time_start = datetime
                            self.table.time_start1 = datetime1
                            self.rpc({
                                model: 'restaurant.table',
                                method: 'update_table_state',
                                args: [[], self.table.id, 'New', state.id, datetime],
                            });
                        }
                    });
                } else {
                    Gui.showPopup('ConfirmPopup', {
                        title: 'Unable to create order',
                        body: 'Orders cannot be created when there is no active table in restaurant mode',
                    });
                    return undefined;
                }
            } else {
                return _super_posmodel.add_new_order.apply(this,arguments);
            }
        },
//	        add_new_order: function() {
//	            _super_PosModel.add_new_order.apply(this, arguments);
//                var self = this;
//                _.each(this.env.pos.table_state, function (state) {
//                    if (state.name == 'New') {
//                        var currentdate = new Date();
//						var datetime = currentdate.getDate() + "/"
//						                + (currentdate.getMonth()+1)  + "/"
//						                + currentdate.getFullYear() + " "
//						                + currentdate.getHours() + ":"
//						                + currentdate.getMinutes() + ":"
//						                + currentdate.getSeconds();
//						var datetime1 = currentdate.getHours() + ":" + currentdate.getMinutes();
//						self.table.state_id = [state.id, state.name]
//						self.table.time_start = datetime
//						self.table.time_start1 = datetime1
//						self.rpc({
//		                    model: 'restaurant.table',
//		                    method: 'update_table_state',
//		                    args: [[], self.table.id, 'New', state.id, datetime],
//		                });
//                    }
//                });
//	        }
    });
});

