# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AdicionarCampos(models.Model):
    _inherit = 'sale.order'

    zona = fields.Many2one(
        comodel_name='zona.zona',
        string='Zona',
        required=False)
    hora = fields.Many2one(
        comodel_name='horario.horario',
        string='Horario',
        required=False)




class ZonaZona(models.Model):
    _name = 'zona.zona'
    _description = 'Zona'

    name = fields.Char(string="Nombre" , required=True,)

class HorarioHorario(models.Model):
    _name = 'horario.horario'
    _description = 'Horario'

    name = fields.Char(string="Nombre" , required=True,)