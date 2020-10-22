# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import datetime
from odoo import api, fields, models

class SaleWizardExcelReporteMayoreo(models.TransientModel):
    _name = 'mayoreo.excel.wizard'

    categorias = fields.Many2many(comodel_name="product.category", string="Categorias", required=False, )
    todas_las_categorias = fields.Boolean(string="Todas las Categorias", default=False)
    sale_oder_ids = fields.Many2one(
        comodel_name='sale.order',
        string='Sale_oder_ids',
        required=False)
    referencia_cliente = fields.Char(
        string='Referencia Cliente',
        required=False)
    comercial = fields.Many2one(comodel_name="res.users", string="Comercial", required=False, )
    # datetime_actual = fields.Datetime(string="Fecha y hora actual", default=fields.Date.context_today, required=False,)
    fecha_inicio = fields.Date(
        string='Fecha Inicio',
        required=False)
    fecha_fin = fields.Date(
        string='Fecha Fin',
        required=False)

    @api.multi
    def print_xls_report(self):
        datas = {}
        datas['active_ids'] = self._context.get('active_ids')
        self.sale_oder_ids = self.env['sale.order'].browse(self._context.get('active_ids')).ids
        datas['model'] = 'mayoreo.excel.wizard'
        datas['form'] = self.read()[0]
        return self.env.ref('reporte_mayoreo.report_mayoreo_excel_card').report_action(self, data=datas)
    


