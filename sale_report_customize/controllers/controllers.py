# -*- coding: utf-8 -*-
from odoo import http

# class SaleReportCustomize(http.Controller):
#     @http.route('/sale_report_customize/sale_report_customize/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_report_customize/sale_report_customize/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_report_customize.listing', {
#             'root': '/sale_report_customize/sale_report_customize',
#             'objects': http.request.env['sale_report_customize.sale_report_customize'].search([]),
#         })

#     @http.route('/sale_report_customize/sale_report_customize/objects/<model("sale_report_customize.sale_report_customize"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_report_customize.object', {
#             'object': obj
#         })