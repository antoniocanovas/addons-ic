odoo.define('pos_product_addons.models', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
    var exports = {};
    models.load_fields('product.product', ['is_addon', 'has_addons','addon_price_hidden']);
    models.load_fields("pos.order.line", "line_stamp");

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        set_quantity: function(quantity, keep_price){
            _super_orderline.set_quantity.apply(this,arguments);
            var line_stamp = this.line_stamp;
            var self = this;
            if(quantity === 'remove' && this.product.has_addons && line_stamp){
                var order = this.pos.get_order();
                var lines = order.get_orderlines();
                var i = 0;
                while ( i < lines.length) {
                    if (line_stamp === lines[i].line_stamp){
                        order.remove_orderline(lines[i]);
                    }else{
                        i++;
                    }
                }
            }

        },

        initialize: function(attr,options){
          _super_orderline.initialize.apply(this, arguments);
          this.line_stamp = this.line_stamp || options.line_stamp;
        },

        export_as_JSON: function () {
          var json = _super_orderline.export_as_JSON.apply(this,arguments);
          json.line_stamp = this.line_stamp;
          return json;
        },

        init_from_JSON: function (json) {
          _super_orderline.init_from_JSON.apply(this, arguments);
          this.line_stamp = json.line_stamp;
        },

        export_for_printing: function(){
          var line = _super_orderline.export_for_printing.apply(this, arguments);
          line.line_stamp = this.line_stamp;
          return line;
        },
    });

    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({
        add_product: function(product, options){
            if(product.is_addon || product.has_addons){
                if(this._printed){
                    this.destroy();
                    return this.pos.get_order().add_product(product, options);
                }
                this.assert_editable();
                options = options || {};
                var line = new models.Orderline({}, {pos: this.pos, order: this, product: product});
                this.fix_tax_included_price(line);
                if(options.quantity !== undefined){
                    line.set_quantity(options.quantity);
                }
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
                if(product.has_addons){
                    var timestamp = new Date().getTime().toString()
                    line.line_stamp = timestamp;
                }
                if(product.is_addon && this.selected_orderline && this.selected_orderline.line_stamp){
                    line.line_stamp = this.selected_orderline.line_stamp;
                }

                var to_merge_orderline;
                if(this.selected_orderline && product.is_addon && product.id == this.selected_orderline.product.id && this.selected_orderline.product.is_addon){
                    to_merge_orderline = this.selected_orderline;
                }
                if(this.selected_orderline && product.is_addon && this.selected_orderline.product.has_addons && this.selected_orderline.line_stamp){
                    var order1 = this.pos.get_order();
                    var line_stamp1 = this.selected_orderline.line_stamp;
                    var selected_orderline_product_id = this.selected_orderline.product.id
                    order1.get_orderlines().forEach(function (orderline11) {
                        if (line_stamp1 == orderline11.line_stamp && product.id == orderline11.product.id){
                            to_merge_orderline = orderline11;
                        }
                    });
                }
                if(this.selected_orderline && product.has_addons && product.id == this.selected_orderline.product.id && this.selected_orderline.product.has_addons){
                    to_merge_orderline = this.selected_orderline;
                }

                if (to_merge_orderline){
                    to_merge_orderline.merge(line);
                    this.select_orderline(to_merge_orderline);
                } else {
                    this.orderlines.add(line);
                    this.select_orderline(this.get_last_orderline());
                }
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