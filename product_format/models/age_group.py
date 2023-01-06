# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AgeGroup(models.Model):
    _name = 'age.group'
    _description = 'Sub Category'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
