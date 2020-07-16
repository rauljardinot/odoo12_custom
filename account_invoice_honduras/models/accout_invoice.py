# -*- coding: utf-8 -*-

from collections import OrderedDict
import json
import re
import uuid
from functools import partial

from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode

from odoo import api, exceptions, fields, models, _
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


MAX_NUMERO = 999999999999
UNIDADES = (
    'cero',
    'uno',
    'dos',
    'tres',
    'cuatro',
    'cinco',
    'seis',
    'siete',
    'ocho',
    'nueve'
)
DECENAS = (
    'diez',
    'once',
    'doce',
    'trece',
    'catorce',
    'quince',
    'dieciseis',
    'diecisiete',
    'dieciocho',
    'diecinueve'
)
DIEZ_DIEZ = (
    'cero',
    'diez',
    'veinte',
    'treinta',
    'cuarenta',
    'cincuenta',
    'sesenta',
    'setenta',
    'ochenta',
    'noventa'
)
CIENTOS = (
    '_',
    'ciento',
    'doscientos',
    'trescientos',
    'cuatroscientos',
    'quinientos',
    'seiscientos',
    'setecientos',
    'ochocientos',
    'novecientos'
)
def numero_a_letras(numero):
    numero_entero = int(numero)
    if numero_entero > MAX_NUMERO:
        raise OverflowError('Número demasiado alto')
    if numero_entero < 0:
        return 'menos %s' % numero_a_letras(abs(numero))
    letras_decimal = ''
    parte_decimal = int(round((abs(numero) - abs(numero_entero)) * 100))
    if parte_decimal > 9:
        letras_decimal = 'Lempiras con %s' % numero_a_letras(parte_decimal)+' centavos'
    elif parte_decimal > 0:
        letras_decimal = 'Lempiras con  %s' % numero_a_letras(parte_decimal)+' centavos'
    if (numero_entero <= 99):
        resultado = leer_decenas(numero_entero)
    elif (numero_entero <= 999):
        resultado = leer_centenas(numero_entero)
    elif (numero_entero <= 999999):
        resultado = leer_miles(numero_entero)
    elif (numero_entero <= 999999999):
        resultado = leer_millones(numero_entero)
    else:
        resultado = leer_millardos(numero_entero)

    resultado = resultado.replace('uno mil', 'un mil')
    resultado = resultado.strip()
    resultado = resultado.replace(' _ ', ' ')
    resultado = resultado.replace('  ', ' ')
    if parte_decimal > 0:
        resultado = '%s %s' % (resultado, letras_decimal)
    r=resultado.replace('lempiras', ' Lempiras')

    return r.capitalize()

def leer_decenas(numero):
    if numero < 10:
        return UNIDADES[numero]
    decena, unidad = divmod(numero, 10)
    if numero <= 19:
        resultado = DECENAS[unidad]
    elif numero <= 29:
        resultado = 'veinti%s' % UNIDADES[unidad]
    else:
        resultado = DIEZ_DIEZ[decena]
        if unidad > 0:
            resultado = '%s y %s' % (resultado, UNIDADES[unidad])
    return resultado

def leer_centenas(numero):
    centena, decena = divmod(numero, 100)
    if numero == 0:
        resultado = 'cien'
    else:
        resultado = CIENTOS[centena]
        if decena > 0:
            resultado = '%s %s' % (resultado, leer_decenas(decena))
    return resultado

def leer_miles(numero):
    millar, centena = divmod(numero, 1000)
    resultado = ''
    if (millar == 1):
        resultado = ''
    if (millar >= 2) and (millar <= 9):
        resultado = UNIDADES[millar]
    elif (millar >= 10) and (millar <= 99):
        resultado = leer_decenas(millar)
    elif (millar >= 100) and (millar <= 999):
        resultado = leer_centenas(millar)
    resultado = '%s mil' % resultado
    if centena > 0:
        resultado = '%s %s' % (resultado, leer_centenas(centena))
    return resultado

def leer_millones(numero):
    millon, millar = divmod(numero, 1000000)
    resultado = ''
    if (millon == 1):
        resultado = ' un millon '
    if (millon >= 2) and (millon <= 9):
        resultado = UNIDADES[millon]
    elif (millon >= 10) and (millon <= 99):
        resultado = leer_decenas(millon)
    elif (millon >= 100) and (millon <= 999):
        resultado = leer_centenas(millon)
    if millon > 1:
        resultado = '%s millones' % resultado
    if (millar > 0) and (millar <= 999):
        resultado = '%s %s' % (resultado, leer_centenas(millar))
    elif (millar >= 1000) and (millar <= 999999):
        resultado = '%s %s' % (resultado, leer_miles(millar))
    return resultado
def llenar_ceros(numero,can_cifras):
    s_numero=len(str(numero))
    print(s_numero)
    prefijo=''
    for i in range(0,can_cifras-s_numero):
        prefijo+='0'
    print(prefijo+str(numero))
    return prefijo+str(numero)



def leer_millardos(numero):
    millardo, millon = divmod(numero, 1000000)
    return '%s millones %s' % (leer_miles(millardo), leer_millones(millon))


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'


    rango_emision = fields.Char(string='Rango de Emisión',compute='_compute_rango_emision')
    importe_letras = fields.Char(string='Importe en Letras',  required=False,compute='_compute_importe_letras' )

    correlativo_constancia_registro_exonerado = fields.Char(string="No Correlativo de Constancia de Registro Exonerado",
                                                               required=False,compute='_compute_no_correlativo_constancia_registro_exonerado' )
    identificativo_registro_sag = fields.Char(string="No Identificativo del Registro de la SAG",
                                                               required=False,compute='_compute_no_correlativo_constancia_registro_exonerado')
    fecha_limite = fields.Date(string="Fecha Límite de Emisión", compute='_compute_rango_emision')
    cai = fields.Char(string="CAI", required=False,compute='_compute_rango_emision')
    no_correlativo_orden_compra_exenta = fields.Char(string="No Correlativo de Orden Compra Exenta",
                                                     required=False,compute='_compute_no_correlativo_constancia_registro_exonerado')
    referencia_orden_compra = fields.Char(string="Orden de Compra", required=False, compute='_compute_no_correlativo_constancia_registro_exonerado')

    importe_exonerado = fields.Boolean(string="Importe Exonerado" ,compute='_compute_no_correlativo_constancia_registro_exonerado',store=False)

    importe_exento =fields.Boolean(string="Importe Exonerado" ,compute='_compute_no_correlativo_constancia_registro_exonerado',store=False)
    importe_gravado15 = fields.Boolean(string="Importe Gravado 15" ,compute='_compute_no_correlativo_constancia_registro_exonerado',store=False)
    importe_gravado18 = fields.Boolean(string="Importe Gravado 18" ,compute='_compute_no_correlativo_constancia_registro_exonerado',store=False)
    lsv15 =fields.Boolean(string="Importe lsv15" ,compute='_compute_no_correlativo_constancia_registro_exonerado',store=False)
    lsv18 = fields.Boolean(string="Importe lsv19" ,compute='_compute_no_correlativo_constancia_registro_exonerado',store=False)



    @api.multi
    @api.depends('amount_total')
    def _compute_importe_letras(self):
        numero_l=''
        for record in self:
            numero_l = numero_a_letras(record.amount_total)
            if numero_l.find("centavos") == -1:
                numero_l = numero_l + " Lempiras exactos"
            record.importe_letras=numero_l.replace('lempiras','Lempiras')

    @api.multi
    def _compute_rango_emision(self):
        for record in self:
            print(self.journal_id.sequence_id)
            diario=self.journal_id.sequence_id.date_range_ids
            secuencia=self.env['ir.sequence.date_range'].search([('id','=',diario.id),('date_from','<=',fields.Date.to_string(self.date_invoice)),('date_to','>',fields.Date.to_string(self.date_invoice))])
            self.fecha_limite=secuencia.date_to
            self.cai=secuencia.cai
            c=self.journal_id.sequence_id.padding
            inicio=llenar_ceros(secuencia.numero_inicial,c)
            fin = llenar_ceros(secuencia.numero_final,c)
            record.rango_emision =str(self.journal_id.sequence_id.prefix) +'-'+ inicio +' al '+str(self.journal_id.sequence_id.prefix) +'-'+ fin

    @api.multi
    def _compute_no_correlativo_constancia_registro_exonerado(self):
        for record in self:
            sale_order=self.env['sale.order'].search([('name', '=', record.origin)])
            record.correlativo_constancia_registro_exonerado=sale_order.no_correlativo_constancia_registro_exonerado
            record.identificativo_registro_sag = sale_order.no_identificativo_registro_sag
            record.no_correlativo_orden_compra_exenta=sale_order.no_correlativo_orden_compra_exenta
            record.referencia_orden_compra = sale_order.client_order_ref

    def _amount_by_group(self):
        for invoice in self:
            currency = invoice.currency_id or invoice.company_id.currency_id
            fmt = partial(formatLang, invoice.with_context(lang=invoice.partner_id.lang).env, currency_obj=currency)
            res = {}
            group_ids=list()
            for line in invoice.tax_line_ids:
                tax = line.tax_id
                group_ids+=tax.ids
                group_key = (tax.tax_group_id, tax.amount_type, tax.amount)

                res.setdefault(group_key, {'base': 0.0, 'amount': 0.0})
                res[group_key]['amount'] += line.amount_total
                res[group_key]['base'] += line.base
            print(res)
            ig15 = self.env['account.tax'].search([('name', '=', 'Gravado 15%')])
            ig18 = self.env['account.tax'].search([('name', '=', 'Gravado 18%')])
            print(ig15.tax_group_id)
            print(ig18.tax_group_id)
            tax_print=self.env['account.tax'].search([('id', 'not in', group_ids),('type_tax_use','=','sale') ,( 'active','=','true')])
            for t in tax_print:
                res.setdefault((t.tax_group_id,'percent',0.0), {'base': 0.0, 'amount': 0.0})

            for line in invoice.tax_line_ids:
                if line.tax_id.tax_group_id.name=="Importe Exonerado":
                    res[(line.tax_id.tax_group_id,'percent',0.0)]['amount']+=res[(line.tax_id.tax_group_id,'percent',0.0)]['base']
                    continue
                if line.tax_id.tax_group_id.name=="Importe Exento":
                    res[(line.tax_id.tax_group_id,'percent',0.0)]['amount']+=res[(line.tax_id.tax_group_id,'percent',0.0)]['base']
                    continue
                if line.tax_id.name=="ISV 15%":
                    res[(ig15.tax_group_id,'percent',0.0)]['amount']+= line.base
                    continue
                if line.tax_id.name=="ISV 18%":
                    res[(ig18.tax_group_id,'percent',0.0)]['amount']+= line.base
                    continue
            res = sorted(res.items(), key=lambda l: l[0][0].sequence)
            invoice.amount_by_group = [(
                r[0][0].name, r[1]['amount'], r[1]['base'],
                fmt(r[1]['amount']), fmt(r[1]['base']),
                len(res),
            ) for r in res]