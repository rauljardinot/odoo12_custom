# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import datetime
from odoo import api, fields, models

class SaleWizardExcel(models.TransientModel):
    _name = 'ventas.excel.wizard'

    sale_oder_ids = fields.Many2one(
        comodel_name='sale.order',
        string='Sale_oder_ids',
        required=False)

    fecha_inicio = fields.Date(
        string='Fecha Inicio',
        required=False)
    fecha_fin = fields.Date(
        string='Fecha Fin',
        required=False)

    horario= fields.Many2one(
        comodel_name='horario.horario',
        string='Horario',
        required=False)

    @api.multi
    def print_xls_report(self):
        datas = {}
        datas['active_ids'] = self._context.get('active_ids')
        self.sale_oder_ids = self.env['sale.order'].browse(self._context.get('active_ids')).ids
        datas['model'] = 'sale.excel.wizard'
        datas['form'] = self.read()[0]
        return self.env.ref('exportar_excel_sale_order.venta_report_excel_card').report_action(self, data=datas)
    


