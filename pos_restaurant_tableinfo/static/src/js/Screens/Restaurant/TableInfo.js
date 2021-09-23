odoo.define('pos_retail_standard.RetailTableWidget', function (require) {
    'use strict';

    const TableWidget = require('pos_restaurant.TableWidget');
    const Registries = require('point_of_sale.Registries');

    const RetailTableWidget = (TableWidget) =>
        class extends TableWidget {

            get checkedIn() {
                const orders = this.env.pos.get_table_orders(this.props.table);
                if (orders.length > 0) {
                    return true
                } else {
                    return false
                }
            }

            get tableInformation() {
                let info = {
                    'checkedIn': null,
                    'amount': 0,
                    'state': null,
                }
                const orders = this.env.pos.get_table_orders(this.props.table);
                if (orders.length > 0) {
                    for (let i=0; i < orders.length; i++) {
                        let order = orders[i]

                        info['checkedIn'] = moment(order.creation_date).format('hh:mm')

                        //order['created_time']

                        info['amount'] = order.get_total_with_tax()
                        //info['amount'] = order.get_state()

                    }
                    return info
                } else {
                    return info
                }
            }
        }

    Registries.Component.extend(TableWidget, RetailTableWidget);

    return RetailTableWidget
});