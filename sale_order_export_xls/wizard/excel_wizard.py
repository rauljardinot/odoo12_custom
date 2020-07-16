# -*- coding: utf-8 -*-
# Copyright (C) 2018-present  Technaureus Info Solutions Pvt. Ltd.(<http://www.technaureus.com/>).

import datetime
from odoo import api, fields, models


class SaleExcelWizard(models.TransientModel):
    _name = 'sale.excel.wizard'

    categorias = fields.Many2many(comodel_name="product.category", string="Categorias", required=False, )
    todas_las_categorias = fields.Boolean(string="Todas las Categorias" ,default=False)
    sale_oder_ids = fields.Many2one(
        comodel_name='sale.order',
        string='Sale_oder_ids',
        required=False)
 

    @api.multi
    def print_xls_report(self):
        datas={}
        datas['active_ids']= self._context.get('active_ids')
        self.sale_oder_ids = self.env['sale.order'].browse(self._context.get('active_ids')).ids
        datas['model'] = 'sale.excel.wizard'
        datas['form'] = self.read()[0]
        return self.env.ref('sale_order_export_xls.sale_report_xls').report_action(self, data=datas)
