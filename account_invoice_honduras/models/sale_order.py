# -*- coding: utf-8 -*-


import logging
from odoo import api, fields, models


class sale_order(models.Model):

    _inherit = 'sale.order'

    no_correlativo_orden_compra_exenta = fields.Char(string="No Correlativo de Orden Compra Exenta",
                                                 required=False, )
    no_correlativo_constancia_registro_exonerado = fields.Char(string="No Correlativo de Constancia de Registro Exonerado",
                                                               required=False, )
    no_identificativo_registro_sag = fields.Char(string="No Identificativo del Registro de la SAG",
                                                               required=False, )