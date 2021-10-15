odoo.define('pos_table_state.models', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var PosDB = require("point_of_sale.DB");
	var utils = require('web.utils');
	var round_pr = utils.round_precision;
	var exports = {};



	models.load_fields('restaurant.table', ['state_id', 'time_start', 'time_waiting_order',
											'time_pending_payment', 'time_done', 'amount']);
	models.load_models({
		model: 'restaurant.table.state',
		fields: ['name', 'type', 'color_code'],
		domain: null,
		loaded: function(self, table_state) {
			self.table_state = table_state;
		},
	});

	models.load_fields('pos.config', ['state_ids']);

});