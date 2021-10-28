odoo.define('pos_product_addons.models', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
    var exports = {};
    models.load_fields('product.product', ['is_addon', 'has_addons','addon_price_hidden']);

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        set_quantity: function(quantity, keep_price){
            console.log('=====set_quantity===Me==',quantity,this);
            _super_orderline.set_quantity.apply(this,arguments);
        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        add_product: function(product, options){
            if(product && product.is_addon){
                if(this._printed){
                    this.destroy();
                    return this.pos.get_order().add_product(product, options);
                }
                this.assert_editable();
                options = options || {};
                var line = new models.Orderline({}, {pos: this.pos, order: this, product: product});
                this.fix_tax_included_price(line);
//                if(options.quantity !== undefined){
//                    line.set_quantity(options.quantity);
//                }
                if (options.price_extra !== undefined){
                    line.price_extra = options.price_extra;
                    line.set_unit_price(line.product.get_price(this.pricelist, line.get_quantity(), options.price_extra));
                    this.fix_tax_included_price(line);
                }
                if(options.price !== undefined){
                    line.set_unit_price(options.price);
                    this.fix_tax_included_price(line);
                }
                if(options.lst_price !== undefined){
                    line.set_lst_price(options.lst_price);
                }
                if(options.discount !== undefined){
                    line.set_discount(options.discount);
                }
                if (options.description !== undefined){
                    line.description += options.description;
                }
                if(options.extras !== undefined){
                    for (var prop in options.extras) {
                        line[prop] = options.extras[prop];
                    }
                }
                if (options.is_tip) {
                    this.is_tipped = true;
                    this.tip_amount = options.price;
                }
                var to_merge_orderline;
                for (var i = 0; i < this.orderlines.length; i++) {
                    if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
                        to_merge_orderline = this.orderlines.at(i);
                    }
                }
//                if (to_merge_orderline){
//                    to_merge_orderline.merge(line);
//                    this.select_orderline(to_merge_orderline);
//                } else {
                    this.orderlines.add(line);
                    this.select_orderline(this.get_last_orderline());
//                }
                if (options.draftPackLotLines) {
                    this.selected_orderline.setPackLotLines(options.draftPackLotLines);
                }
                if (this.pos.config.iface_customer_facing_display) {
                    this.pos.send_current_order_to_customer_facing_display();
                }
            }else{
                _super_order.add_product.apply(this,arguments);
            }
        },
    });
});