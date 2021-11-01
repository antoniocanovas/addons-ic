odoo.define('pos_product_addons.OrderWidget', function(require) {
    'use strict';

    const { useState, useRef, onPatched } = owl.hooks;
    const { useListener } = require('web.custom_hooks');
    const { onChangeOrder } = require('point_of_sale.custom_hooks');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const OrderWidget = require('point_of_sale.OrderWidget');

    const OrderWidgetCR = OrderWidget =>
		class extends OrderWidget {
            get orderlinesHasAddonsArray() {
                var orderlines = this.order ? this.order.get_orderlines() : [];
                var orderlineHasAddons_dict = {}
                _.each(orderlines,function(line){
                    if(line.line_stamp){
                        if(line.line_stamp in orderlineHasAddons_dict){
                            orderlineHasAddons_dict[line.line_stamp].push(line)
                        }else{
                            orderlineHasAddons_dict[line.line_stamp] = [line]
                        }
                    }else{
                        if('undefined' in orderlineHasAddons_dict){
                            orderlineHasAddons_dict['undefined'].push(line)
                        }else{
                            orderlineHasAddons_dict['undefined'] = [line]
                        }
                    }
                })
                console.log('===2==',orderlineHasAddons_dict)
                return orderlineHasAddons_dict;
            }
		};

    Registries.Component.extend(OrderWidget, OrderWidgetCR);
    return OrderWidgetCR;
});
