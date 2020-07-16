# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import xlsxwriter
from odoo import models
from datetime import datetime, timedelta

class SalesXlsx(models.AbstractModel):
    _name = 'report.exportar_excel_sale_order.venta_report_excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard_obj):
        for obj in wizard_obj:
            domain=[]
            if obj.fecha_inicio:
                domain.append(('date_order', '>=', obj.fecha_inicio))
            if obj.fecha_fin:
                domain.append(('date_order', '<=', obj.fecha_fin))
            if obj.horario:
                domain.append(('hora', '=', obj.horario.id))

            domain.append(('state', 'not in', ['cancel']))

            sale_order = self.env['sale.order'].search(domain)
            worksheet = workbook.add_worksheet('Report')
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            text = workbook.add_format({'font_size': 12, 'align': 'center'})

            row = 1
            col = 0
            for sale in sale_order:
                worksheet.write(row, col, sale.name, text)
                worksheet.write(row, col+1, sale.partner_id.name, text)
                worksheet.write(row, col+2, (sale.partner_id.phone if sale.partner_id.phone else ""), text)
                if sale.date_order:
                    worksheet.write(row, col+3,  datetime.strftime(sale.date_order, '%Y-%m-%d'), text)
                direccion = str(sale.partner_id.street)or " " + ' ' + str(sale.partner_id.street2) or " " + ' ' + str(sale.partner_id.city) or " " + ' ' +  str(sale.partner_id.state_id.name) or " " + ' ' +  str(sale.partner_id.country_id.name)or " "
                worksheet.write(row, col+4, direccion, text)
                worksheet.write(row, col+5, sale.payment_term_id.name or "", text)
                worksheet.write(row, col+6, sale.note, text)
                worksheet.write(row, col+7, sale.hora.name or " " , text)
                worksheet.write(row, col+8, sale.zona.name or "", text)
                worksheet.write(row, col+9, sale.amount_total or "", text)
                row=row+1

            row = 0
            col = 0
            worksheet.set_column('A:A', 10)
            worksheet.set_column('B:B', 30)
            worksheet.set_column('E:E', 50)
            worksheet.set_column('F:F', 14)
            worksheet.set_column('G:G', 50)
            worksheet.write(row, col, 'Pedido', text)
            worksheet.write(row, col+1, 'Cliente', text)
            worksheet.write(row, col+2, 'Telefono', text)
            worksheet.write(row, col+3, 'Dia', text)
            worksheet.write(row, col+4, 'Colonia', text)
            worksheet.write(row, col+5, 'Forma de Pago', text)
            worksheet.write(row, col+6, 'Observaciones', text)
            worksheet.write(row, col+7, 'Hora', text)
            worksheet.write(row, col+8, 'Zona', text)
            worksheet.write(row, col+9, 'Factura', text)
            row = 0
            col=col+1




