from odoo import models, fields


class SaleOrderCategory(models.Model):
    _name = 'fs.sale.categ'

    name = fields.Char(string='Category')


class CustomSaleOrderLine(models.Model):
    _inherit = 'sale.order'

    sale_category = fields.Many2one('fs.sale.categ', "Sale Category")
