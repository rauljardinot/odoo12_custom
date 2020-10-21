# -*- coding: utf-8 -*-
from odoo import http

# class SaleOrderExportXls(http.Controller):
#     @http.route('/sale_order_export_xls/sale_order_export_xls/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_export_xls/sale_order_export_xls/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_export_xls.listing', {
#             'root': '/sale_order_export_xls/sale_order_export_xls',
#             'objects': http.request.env['sale_order_export_xls.sale_order_export_xls'].search([]),
#         })

#     @http.route('/sale_order_export_xls/sale_order_export_xls/objects/<model("sale_order_export_xls.sale_order_export_xls"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_export_xls.object', {
#             'object': obj
#         })