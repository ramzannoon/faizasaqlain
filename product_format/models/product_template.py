# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    age_group_ids = fields.Many2many('age.group', string='Sub Categories')
    year_id = fields.Many2one('product.year', string='Year')
    design_name = fields.Char(string='Design Name')
    design_code = fields.Char(string='Design Code')
    collection_name = fields.Char(string='Collection Name')
    sampling_code = fields.Char(string='Sampling Code')
    calender_season_ids = fields.Many2many('calender.season', string='Seasons')
    accessories_ids = fields.Many2many('product.accessories', string='Accessories')
    components_ids = fields.Many2many('product.component', string='Component')
    product_gender = fields.Selection([('male', 'Male'),
                                       ('female', 'Female'),
                                       ('unisex', 'Unisex'),
                                       ], string='Product Gender')
