# -*- coding: utf-8 -*-
from odoo import http

# class Extra-addons/demodata(http.Controller):
#     @http.route('/extra-addons/demodata/extra-addons/demodata/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/extra-addons/demodata/extra-addons/demodata/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('extra-addons/demodata.listing', {
#             'root': '/extra-addons/demodata/extra-addons/demodata',
#             'objects': http.request.env['extra-addons/demodata.extra-addons/demodata'].search([]),
#         })

#     @http.route('/extra-addons/demodata/extra-addons/demodata/objects/<model("extra-addons/demodata.extra-addons/demodata"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('extra-addons/demodata.object', {
#             'object': obj
#         })