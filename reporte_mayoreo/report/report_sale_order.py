# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import xlsxwriter
from odoo import models, fields, api, _
import time
from datetime import date, datetime, timedelta
from odoo.exceptions import ValidationError


class SalesXlsx(models.AbstractModel):
    _name = 'report.reporte_mayoreo.venta_report_excel'
    _inherit = 'report.report_xlsx.abstract'

    # datetime_actual = fields.Datetime(string="", default=fields.Date.context_today, )

    def generate_xlsx_report(self, workbook, data, wizard_obj):
        #sale_order=self.env['sale.order'].browse(data.get('active_ids'))

        now=datetime.now()

        for obj in wizard_obj:
            domain=[]

            # raise ValidationError(obj.comercial.name)
            # raise ValidationError(now)

            if obj.fecha_inicio:
                domain.append(('confirmation_date', '>=', obj.fecha_inicio))
            if obj.fecha_inicio:
                domain.append(('confirmation_date', '<=', obj.fecha_fin))
            if obj.comercial:
                domain.append(('user_id', '=', obj.comercial.name))
            # domain.append(('state', 'not in', ['cancel']))

            sale_order = self.env['sale.order'].search(domain)
            # raise ValidationError(len(sale_order))
            # raise ValidationError(sale_order)

            # print(productos_ids)
            # for sale in sale_order:
            #     for line in sale.order_line:
            #         product_ids |= line.product_id
            # if not obj.todas_las_categorias:
            #     product_ids = self.env['product.product'].search([('id', 'in', product_ids.ids), ('categ_id', 'in',obj.categorias.ids)]
            #                                                      ,order = 'default_code asc')
            # else:
            #     product_ids = self.env['product.product'].search(
            #         [('id', 'in', product_ids.ids)]
            #         , order='default_code desc')
            worksheet = workbook.add_worksheet('Report')
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})

            # row = 1
            # col = 0
            hoja = 1

            # for sale in sale_order:
                # worksheet.write('A' + str(hoja), 'Estudiante: ', bold)
                # worksheet.write('A' + str(hoja+1), 'HOlas: ', bold)
                # worksheet.write(row+5, col+1, sale.name, text)
                # worksheet.write(row+6, col+1, sale.partner_id.name, text)
                # worksheet.write(row, col+2, (sale.partner_id.phone if sale.partner_id.phone else ""), text)
                # worksheet.write(row, col+3, sale.confirmation_date, text)#revisar aquiiiiiiiii
                # direccion = []
                # direccion = str(sale.partner_id.street) + ',' + str(sale.partner_id.street2) + ',' + str(sale.partner_id.city) + ',' + str(sale.partner_id.state_id.name) + ',' + str(sale.partner_id.country_id.name)
                # worksheet.write(row, col+4, direccion, text)
                # worksheet.write(row, col+5, sale.payment_term_id.name, text)
                # worksheet.write(row, col+6, sale.note, text)
                # worksheet.write(row, col+7, sale.hora, text)
                # worksheet.write(row, col+8, sale.zona, text)
                # worksheet.write(row, col+9, sale.amount_total, text)
                # row=row+1

            row = 0
            col = 0
            # worksheet.set_column('A:A', 10)
            # worksheet.set_column('B:B', 30)
            # worksheet.set_column('E:E', 50)
            # worksheet.set_column('F:F', 14)
            # worksheet.set_column('G:G', 50)
            worksheet.set_column(0, 0, 60)
            # worksheet.set_column(1, 2, 50)
            # worksheet.set_column(3, 3, 15)
            # worksheet.set_column(4, 4, 15)
            # worksheet.set_column(5, 5, 25)
            # worksheet.set_column(6, 6, 25)
            # worksheet.set_column(7, 7, 25)
            # worksheet.set_column(8, 8, 25)
            worksheet.write('A' + str(hoja), 'REPORTE DE VENTAS SUPERMERCADOSDIGITAL-SMD MAYOREO', bold)
            worksheet.write('I' + str(hoja), 'Fecha y hora de generacion del reporte', text)
            worksheet.write('B' + str(hoja + 2), 'Periodo del ' +str(obj.fecha_inicio)+' al '+str(obj.fecha_fin), text)
            worksheet.write('A' + str(hoja + 3), 'Ruta:', text)
            worksheet.write('D' + str(hoja + 4), 'Nombre del vendedor: '+ obj.comercial.name, text)
            worksheet.write('E' + str(hoja + 6), 'AREA DE COBRO', text)
            worksheet.write('A' + str(hoja + 7), 'Monto Cobrado incluyendo impuesto sobre ventas:', text)
            worksheet.write('G' + str(hoja + 7), 'Monto cobrado sin Impuestos sobre ventas:', text)
            worksheet.write('A' + str(hoja + 9), 'Porcentaje de morosidad de cartera', text)
            worksheet.write('E' + str(hoja + 12), 'AREA DE VENTA', text)
            worksheet.write('A' + str(hoja + 13), 'Descripcion ', bold)
            worksheet.write('C' + str(hoja + 13), 'Meta Monto ', bold)
            worksheet.write('E' + str(hoja + 13), 'Venta Monto ', bold)
            worksheet.write('G' + str(hoja + 13), 'Porcentaje A ', bold)
            worksheet.write('H' + str(hoja + 13), 'Porcentaje B ', bold)
            worksheet.write('I' + str(hoja + 13), 'Porcentaje C ', bold)
            worksheet.write('J' + str(hoja + 13), 'Porcentaje D ', bold)
            worksheet.write('K' + str(hoja + 13), 'Comision ', bold)
            # worksheet.write('A' + str(hoja + 13), 'Total ', text)

            row = hoja + 15
            col = 0
            # product_ids = self.env['product.product']
            # for sale in sale_order:
            #     worksheet.write(row, col, sale.name, text)
            #     row = row + 1

            # for sale in sale_order:
            #     worksheet.write(row, col, order_line, text)
                # for line in sale.order_line:
                #     pass
                    # product_ids |= line.product_id

            ##########################################################
            # aqui tomo los productos y sus cantidades y los imprimo
            ##########################################################
            # for sale in sale_order:
            #     for line in sale.order_line:
            #         print(str(line.product_id))
            #         producto = self.env['product.product'].search([('id','=',line.product_id.id)])
            #         # raise ValidationError(producto.name)
            #         worksheet.write(row, col, producto.name, text)
            #         worksheet.write(row, col+2, line.product_uom_qty, text)
            #         row = row + 1
            ##################################################
            ##################################################

            # ##########################################################
            # Prueba: Aqui cojo solo los productos que estan en venta
            ##########################################################
            productos_ids = self.env['product.product'].search([])
            product_ids = self.env['product.product']
            marcas_ids = self.env['product.brand']
            for sale in sale_order:
                for line in sale.order_line:
                    print(str(line.product_id))
                    producto = self.env['product.product'].search([('id','=',line.product_id.id)])
                    product_ids |= line.product_id


                    # tomar nombre de la marca y agruapr por marca
                    marca = self.env['product.brand'].search([('id','=',producto.brand_id.id)])
                    marcas_ids |= producto.brand_id

                    # raise ValidationError(producto.name)
                    worksheet.write(row, col, producto.name, text)
                    worksheet.write(row, col+2, line.product_uom_qty, text)
                    worksheet.write(row, col+4, str(marca.name), text)
                    row = row + 1

            print("Productos agrupados por nombre", product_ids)
            print("Productos agrupados por marca", marcas_ids)
            ##################################################
            ##################################################


                    # product_ids |= line.product_id
            # if not obj.todas_las_categorias:
            #     product_ids = self.env['product.product'].search(
            #         [('id', 'in', product_ids.ids), ('categ_id', 'in', obj.categorias.ids)]
            #         , order='default_code asc')
            # else:
            #     product_ids = self.env['product.product'].search(
            #         [('id', 'in', product_ids.ids)]
            #         , order='default_code desc')
            # for product in product_ids:
            #     worksheet.write(row, col, line.product_id, text)