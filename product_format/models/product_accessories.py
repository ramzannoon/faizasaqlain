# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductAccessories(models.Model):
    _name = 'product.accessories'
    _description = 'Product Accessories'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
