odoo.define('pos_table_state.SetStateButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class SetStateButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        mounted() {
            this.env.pos.get('orders').on('add remove change', () => this.render(), this);
            this.env.pos.on('change:selectedOrder', () => this.render(), this);
        }
        willUnmount() {
            this.env.pos.get('orders').off('add remove change', null, this);
            this.env.pos.off('change:selectedOrder', null, this);
        }
        get currentOrder() {
            return this.env.pos.get_order();
        }
        get currentStateName() {
            const table = this.env.pos.table;
            return table && table.state_id
                ? table.state_id[1]
                : this.env._t('State');
        }
        async onClick() {
            var self = this;
            var table_state_list = []

            _.each(this.env.pos.config.state_ids, function (state) {
                _.each(self.env.pos.table_state, function (state_id) {
                    if (state_id.id == state) {
		                table_state_list.push({'id': state_id.id,
			                               'label': state_id.name,
			                               'color_code': state_id.color_code,
			                               'item': state_id.id});
			        }
		        });

            });

            const selectionList = table_state_list.map(statelist => ({
                id: statelist.id,
                label: statelist.label,
                isSelected: statelist.id === self.env.pos.table.state_id.id,
                item: statelist,
            }));
            const { confirmed, payload: selectedStatelist } = await self.showPopup(
                'SelectionPopup',
                {
                    title: self.env._t('Select the state'),
                    list: selectionList,
                }
            );
            if (confirmed) {
                self.env.pos.table.state_id = [selectedStatelist.id, selectedStatelist.label]
                var currentdate = new Date();
                var datetime = currentdate.getDate() + "/"
							                + (currentdate.getMonth()+1)  + "/"
							                + currentdate.getFullYear() + " "
							                + currentdate.getHours() + ":"
							                + currentdate.getMinutes() + ":"
							                + currentdate.getSeconds();
				if (selectedStatelist.label == 'New'){
					self.env.pos.table.time_start = datetime
				}
				if (selectedStatelist.label == 'Waiting Order'){
					self.env.pos.table.time_waiting_order = datetime
				}
				if (selectedStatelist.label == 'Pending Payment'){
					self.env.pos.table.time_pending_payment = datetime
				}
				if (selectedStatelist.label == 'Done'){
					self.env.pos.table.time_done = datetime
				}
				self.rpc({
                    model: 'restaurant.table',
                    method: 'update_table_state',
                    args: [[], self.env.pos.table.id, selectedStatelist.label, selectedStatelist.id, datetime],

                });
            }
        }
    }
    SetStateButton.template = 'SetStateButton';

    ProductScreen.addControlButton({
        component: SetStateButton,
        condition: function() {
            return this.env.pos.config.state_ids;
        },
    });

    Registries.Component.add(SetStateButton);

    return SetStateButton;
});
