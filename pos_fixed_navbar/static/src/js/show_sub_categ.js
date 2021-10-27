odoo.define('pos_fixed_navbar.ShowSubCategory', function(require) {
'use strict';

    const ProductsWidget = require('point_of_sale.ProductsWidget');
    const Registries = require('point_of_sale.Registries');

    const FixedProductsWidget = ProductsWidget =>
        class extends ProductsWidget {
            get parentSubCategory() {
                var self = this;
                var parentSubCat = [];
                this.env.pos.db
                    .get_category_childs_ids(this.env.pos.db.get_category_parent_id(this.selectedCategoryId))
                    .map(function(id) {
                        if (self.selectedCategoryId !== id) {
                            parentSubCat.push(self.env.pos.db.get_category_by_id(id))
                        }
                    });
                return parentSubCat;
            }
        }
    Registries.Component.extend(ProductsWidget, FixedProductsWidget);

    return FixedProductsWidget;
});