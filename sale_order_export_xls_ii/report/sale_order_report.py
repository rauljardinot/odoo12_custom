# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import xlsxwriter
from odoo import models


class SalesXlsx(models.AbstractModel):
    _name = 'report.sale_excel_report.sale_report_xls.xslx'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, wizard_obj):
        #sale_order=self.env['sale.order'].browse(data.get('active_ids'))


        for obj in wizard_obj:
            domain=[]

            if obj.fecha_inicio:
                domain.append(('date_order', '>=', obj.fecha_inicio))
            if obj.fecha_inicio:
                domain.append(('date_order', '<=', obj.fecha_fin))
            if obj.referencia_cliente:
                domain.append(('client_order_ref', '=', obj.referencia_cliente))
            if obj.horario:
                domain.append(('hora', '=', obj.horario.id))
            domain.append(('state', 'not in', ['cancel']))

            sale_order = self.env['sale.order'].search(domain)
            product_ids = self.env['product.product']
            for sale in sale_order:
                for line in sale.order_line:
                    product_ids |= line.product_id
            if not obj.todas_las_categorias:
                product_ids = self.env['product.product'].search([('id', 'in', product_ids.ids), ('categ_id', 'in',obj.categorias.ids)]
                                                                 ,order = 'default_code asc')
            else:
                product_ids = self.env['product.product'].search(
                    [('id', 'in', product_ids.ids)]
                    , order='default_code asc')
            worksheet = workbook.add_worksheet('Report')
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})

            row = 1
            col = 0
            for sale in sale_order:
                worksheet.write(row, col, sale.name, text)
                worksheet.write(row, col+1, sale.partner_id.name, text)
                row=row+1

            row = 0
            col = 2
            worksheet.set_column('A:A', 10)
            worksheet.set_column('B:B', 16)
            for product in product_ids:
                worksheet.set_column('C:WWW', 25)

                worksheet.write(row, col, (product.default_code  if product.default_code else "")+" "+product.name, text)
                for sale in sale_order:
                    row=row+1
                    order_line_ids=self.env['sale.order.line'].search([('id','in',sale.order_line.ids),('product_id','=',product.id)])
                    amount_tax = sum(lines.product_uom_qty for lines in order_line_ids)
                    amount_tax=str(int(float(amount_tax)))
                    if amount_tax=='0':
                        amount_tax=''
                    worksheet.write(row, col,amount_tax, text)
                row = 0
                col=col+1

