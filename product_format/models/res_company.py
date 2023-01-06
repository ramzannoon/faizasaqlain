# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    is_editable = fields.Boolean(string='Product Creation Fix', default=False)
    company_header = fields.Binary(string='Company Header', help="Add Report Header")
    company_footer = fields.Binary(string='Company Footer', help="Add Report Footer")
