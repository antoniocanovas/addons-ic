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
                var is_true = true;
                const product = event.detail;
                const orderline = this.currentOrder.get_orderlines();
                if (product && product.is_addon && orderline) {
                    var has_addons_line = false;
                    _.each(orderline, function(val){
                        if(val && val.product.has_addons){
                            has_addons_line = true;
                        }
                    });
                    if(!has_addons_line){
                        is_true = false;
                    }
                }
                if(is_true){
                    super._clickProduct(...arguments);
                }else{
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Warning'),
                        body: this.env._t(
                            'This product has no addons'
                        ),
                    });
                }
            }
		};

    Registries.Component.extend(ProductScreen, ProductScreenCR);
    return ProductScreenCR;
});
