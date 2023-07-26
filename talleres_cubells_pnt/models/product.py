# -*- coding: utf-8 -*-
from odoo import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        print("NAME GET")
        res = super(ProductProduct, self).name_get()
        recs = self.browse([x[0] for x in res])
        recs = [(x.id, (
        (x.default_code and "%s [%s]" % (x.name, x.default_code)) or x.name))
                for x in recs]
        print(recs)
        return sorted(recs, key=lambda r: r[1].lower())


