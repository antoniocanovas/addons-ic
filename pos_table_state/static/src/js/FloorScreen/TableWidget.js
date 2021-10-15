odoo.define('pos_table_state.TableWidget', function(require) {
    'use strict';

    const TableWidget = require('pos_restaurant.TableWidget');
    const Registries = require('point_of_sale.Registries');

    const POSTableWidget = TableWidget =>
		class extends TableWidget {
			mounted() {
				super.mounted(...arguments);
				const table = this.props.table;
				var self = this;
				function unit(val) {
	                return `${val}px`;
	            }
				const style = {
	                width: table.shape === 'round' ? '200px' : '160px',
	                height: table.shape === 'round' ? '200px' : '160px',
	                'line-height': '100px',
	                top: unit(table.position_v),
	                left: unit(table.position_h),
	                'border-radius': table.shape === 'round' ? unit(1000) : '3px',
	            };
				_.each(this.env.pos.table_state, function (state) {
	                if (state.id == table.state_id[0]) {
			            if (state.color_code) {
			                if (table.height >= 150 && table.width >= 150) {
				                style['font-size'] = '32px';
				            }
			                Object.assign(self.el.style, style);
				            const tableCover = self.el.querySelector('.table-cover');
				            Object.assign(tableCover.style, { height: `${Math.ceil(self.fill * 100)}%` });
							$(self.el).css('background', state.color_code)
			            }
	                }
		            else {
			            if (table.height >= 150 && table.width >= 150) {
			                style['font-size'] = '32px';
			            }
			            Object.assign(self.el.style, style);
			            const tableCover = self.el.querySelector('.table-cover');
			            Object.assign(tableCover.style, { height: `${Math.ceil(self.fill * 100)}%` });
		            }
				});
            }
		};

    Registries.Component.extend(TableWidget, POSTableWidget);

	return POSTableWidget;
});