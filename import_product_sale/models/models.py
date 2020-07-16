# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import binascii
import io
import logging
import tempfile
from datetime import datetime
from odoo.exceptions import Warning, UserError
import xlrd
from odoo import models, fields, exceptions, api, _
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)

try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')

try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class ImportSaleLine(models.TransientModel):
    _name = "import.sale_line"

    file = fields.Binary('File')

    @api.multi
    def import_xls(self):
        active_ids = self._context.get('active_ids')
        active_model = self._context.get('active_model')
        # Check for selected invoices ids
        if not active_ids or active_model != 'sale.order':
            return True
        sale = self.env['sale.order'].browse(active_ids)
        fp = tempfile.NamedTemporaryFile(suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file))
        fp.seek(0)
        values = {}
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        index = 0
        for row_no in range(sheet.nrows):
            index = index + 1
            val = {}
            if row_no <= 0:
                fields = map(lambda row: row.value.encode('utf-8'), sheet.row(row_no))
            else:
                if index == 2:
                    line = list(
                        map(lambda row: isinstance(row.value, bytes) and row.value.encode('utf-8') or str(row.value),
                            sheet.row(row_no)))
                    no_orden = line[0]
                    cantidad = line[1]
                    producto = line[2].split()[0]
                    precio = line[5]
                    product_id = self.env['product.product'].search([('default_code', '=', producto)])
                    if product_id:
                        sale_order_line = self.env['sale.order.line'].create({
                            'order_id': self.id,
                            'name': product_id.name,
                            'product_id': product_id.id,
                            'product_uom_qty': int(float(cantidad)),
                            # 'price_unit': self.product_delivery_timesheet3.list_price
                        })
                        sale.order_line |= sale_order_line
                    else:
                        raise UserError(u"No se encotró el producto: " + line[2])

    @api.multi
    def import_sale(self):
        active_ids = self._context.get('active_ids')
        active_model = self._context.get('active_model')
        # Check for selected invoices ids
        if not active_ids or active_model != 'sale.order':
            return True
        sale = self.env['sale.order'].browse(active_ids)
        data = base64.b64decode(self.file)
        file_input = io.StringIO(data.decode('UTF-16'))
        reader = csv.reader(file_input,delimiter='\t')
        index=0
        for line in reader:
            index=index+1
            if index>=2:
                no_orden = line[0]
                cantidad = line[1]
                producto = line[2].split()[0]
                precio = line[5]
                product_id = self.env['product.product'].search([('default_code', '=', producto)])
                if product_id:
                    # sale_order_line = self.env['sale.order.line'].create({
                    #     'order_id': self.id,
                    #     'name': product_id.name,
                    #     'product_id': product_id.id,
                    #     #'product_uom_qty': int(float(cantidad)),
                    #     #'product_uom': product_id.product_tmpl_id.uom_id.id,
                    #     #'price_unit':float(precio)/int(float(cantidad))
                    # })

                    sale_order_line1 = self.env['sale.order.line'].create({
                        'name': product_id.name,
                        'product_id': product_id.id,
                        'product_uom_qty':  int(float(cantidad)),
                        'qty_delivered': 1,
                        'product_uom': product_id.uom_id.id,
                        'price_unit': float(precio)/int(float(cantidad)),
                        'order_id': sale.id,
                    })
                    sale_order_line1.product_id_change()
                    sale.order_line |= sale_order_line1
                else:
                    raise UserError(u"No se encotró el producto: " + line[2])
