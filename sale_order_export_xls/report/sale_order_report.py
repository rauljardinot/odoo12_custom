# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import xlsxwriter
from odoo import models


class SalesXlsx(models.AbstractModel):
    _name = 'report.sale_excel_report.sale_report_xls.xslx'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, wizard_obj):
        sale_order=self.env['sale.order'].browse(data.get('active_ids'))
        product_ids=self.env['product.product']
        for sale in  sale_order:
            for line in sale.order_line:
                product_ids |= line.product_id

        for obj in wizard_obj:
            if not obj.todas_las_categorias:
                product_ids = self.env['product.product'].search([('id', 'in', product_ids.ids), ('categ_id', 'in',obj.categorias.ids)])
            worksheet = workbook.add_worksheet('Report')
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})
            worksheet.set_column(0, 0, 80)
            worksheet.set_column(1, 2, 25)
            worksheet.set_column(3, 3, 25)
            worksheet.set_column(4, 4, 25)
            worksheet.set_column(5, 5, 25)
            worksheet.set_column(6, 6, 25)
            worksheet.set_column(7, 7, 25)
            worksheet.set_column(8, 8, 25)


            row = 0
            col = 1
            for sale in sale_order:
                worksheet.write(row, col, sale.name, text)
                col=col+1

            row = 1
            col = 0
            for product in product_ids:
                worksheet.write(row, col, product.default_code+" "+product.name, text)
                for sale in sale_order:
                    col=col+1
                    order_line_ids=self.env['sale.order.line'].search([('id','in',sale.order_line.ids),('product_id','=',product.id)])
                    amount_tax = sum(lines.product_uom_qty for lines in order_line_ids)
                    worksheet.write(row, col,str(amount_tax), text)
                col = 0
                row=row+1
