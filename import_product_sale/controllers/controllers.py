# -*- coding: utf-8 -*-
from odoo import http

# class ImportProductSale(http.Controller):
#     @http.route('/import_product_sale/import_product_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/import_product_sale/import_product_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('import_product_sale.listing', {
#             'root': '/import_product_sale/import_product_sale',
#             'objects': http.request.env['import_product_sale.import_product_sale'].search([]),
#         })

#     @http.route('/import_product_sale/import_product_sale/objects/<model("import_product_sale.import_product_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('import_product_sale.object', {
#             'object': obj
#         })