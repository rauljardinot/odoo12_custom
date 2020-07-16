
from odoo import _, api, fields, exceptions, models
from odoo.exceptions import UserError, ValidationError

class ir_sequence(models.Model):

    _inherit = 'ir.sequence'

class ir_sequence_date_range(models.Model):

    _inherit = 'ir.sequence.date_range'

    numero_inicial = fields.Integer(string="Número Inicial", required=False ,default=1000)
    numero_final = fields.Integer(string="Número Final", required=False,default=2000 )
    cai = fields.Char(string="CAI", required=False, )

    @api.onchange('numero_inicial')
    def _onchange_numero_inicial(self):
        cantidad_cifras = 10 ** (self.sequence_id.padding - 1)
        if len(str(self.numero_final)) > len(str(cantidad_cifras)):
            raise ValidationError(
                _('El valor de Número Inicial no puede ser mayor a ' + str(len(str(cantidad_cifras))) + ' cifras'))
    @api.constrains('numero_inicial')
    def constrains_numero_inicial(self):
        cantidad_cifras = 10 ** (self.sequence_id.padding - 1)
        if len(str(self.numero_final)) > len(str(cantidad_cifras)):
            raise ValidationError(
                _('El valor de Número Inicial no puede ser mayor a ' + str(len(str(cantidad_cifras))) + ' cifras'))

    @api.onchange('numero_final')
    def _onchange_numero_final(self):
        cantidad_cifras = 10 ** (self.sequence_id.padding - 1)
        if len(str(self.numero_final))> len(str(cantidad_cifras)):
            raise ValidationError(_('El valor de Número Final no puede ser mayor a '+str(len(str(cantidad_cifras)))+' cifras'))
    @api.constrains('numero_final')
    def constrains_numero_final(self):
        cantidad_cifras = 10 ** (self.sequence_id.padding - 1)
        if len(str(self.numero_final)) > len(str(cantidad_cifras)):
            raise ValidationError(
                _('El valor de Número Final no puede ser mayor a ' + str(len(str(cantidad_cifras))) + ' cifras'))