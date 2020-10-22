# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AdicionarCampos(models.Model):
    _inherit = 'sale.order'

    hora = fields.Char(string="Hora", required=False, )
    zona = fields.Char(string="Zona", required=False, )