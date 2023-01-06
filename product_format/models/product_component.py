# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductComponent(models.Model):
    _name = 'product.component'
    _description = 'Product Component'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
