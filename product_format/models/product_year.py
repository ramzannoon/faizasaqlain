# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductYear(models.Model):
    _name = 'product.year'
    _description = 'Product Year'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
