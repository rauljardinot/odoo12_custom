# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def print_quotation(self):
        direccion =self.partner_id.street and  self.partner_id.street2
        if not direccion :
            raise UserError(_("La Dirección del Cliente esta incompleta."))
        elif not self.partner_id.phone:
            raise UserError(_("El campo teléfono del Cliete esta vacio."))

        else:
            self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

            return self.env.ref('sale.action_report_saleorder')\
                .with_context(discard_logo_check=True).report_action(self)