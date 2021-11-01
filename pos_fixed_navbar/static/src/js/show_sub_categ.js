odoo.define('pos_fixed_navbar.ShowSubCategory', function(require) {
'use strict';

    const ProductsWidget = require('point_of_sale.ProductsWidget');
    const Registries = require('point_of_sale.Registries');

    const FixedProductsWidget = ProductsWidget =>
        class extends ProductsWidget {
            get subcategories() {
                var parentSubCatBase =  this.env.pos.db
                    .get_category_childs_ids(this.selectedCategoryId)
                    .map(id => this.env.pos.db.get_category_by_id(id));
                var self = this;
                var parentSubCat = [];
                if(parentSubCatBase.length > 0){
                }else{
                var FixselectedCategoryId = this.selectedCategoryId
                if (this.env.pos.db.get_category_parent_id(this.selectedCategoryId) > 0){
                    FixselectedCategoryId = this.env.pos.db.get_category_parent_id(this.selectedCategoryId)
                }
                this.env.pos.db.get_category_childs_ids(FixselectedCategoryId)
                    .map(function(id) {
                        if (self.selectedCategoryId !== id) {
                            parentSubCatBase.push(self.env.pos.db.get_category_by_id(id))
                        }
                    });
                }
                return parentSubCatBase
            }

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