odoo.define('pos_product_addons.ProductScreen', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const { onChangeOrder, useBarcodeReader } = require('point_of_sale.custom_hooks');
    const { useState } = owl.hooks;
    const { parse } = require('web.field_utils');
    const ProductScreen = require('point_of_sale.ProductScreen');

    const ProductScreenCR = ProductScreen =>
		class extends ProductScreen {
            async _clickProduct(event) {
                const product = event.detail;
                const orderline = this.currentOrder.selected_orderline;
                if (product && product.is_addon) {
                    if(!orderline){
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Warning'),
                            body: this.env._t(
                                'This product has no addons'
                            ),
                        });
                    }else if(orderline && orderline.line_stamp){
                        super._clickProduct(...arguments);
                    }else if(orderline && !orderline.product.has_addons){
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Warning'),
                            body: this.env._t(
                                'This product has no addons'
                            ),
                        });
                    } else{
                        super._clickProduct(...arguments);
                    }
                } else{
                    super._clickProduct(...arguments);
                }
            }
		};

    Registries.Component.extend(ProductScreen, ProductScreenCR);
    return ProductScreenCR;
});
