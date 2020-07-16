# -*- coding: utf-8 -*-


import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)
class ResPartner(models.Model):

    _inherit = "res.partner"

    rtn = fields.Char(string='RTN' )

