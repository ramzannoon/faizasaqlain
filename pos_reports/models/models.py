from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class POSORDER(models.Model):
    _inherit = 'pos.order'


    date_order_custom = fields.Date(string='Date Order Date Value', compute='_compute_date_order_custom', store=True)


    @api.depends('date_order')
    def _compute_date_order_custom(self):
        for rec in self:
            if rec.date_order:
                rec.date_order_custom = rec.date_order.strftime("%Y-%m-%d")


class POSpayment(models.Model):
    _inherit = 'pos.payment'


    date_order_custom = fields.Date(string='Date Order Date Value', compute='_compute_date_order_custom', store=True)


    @api.depends('payment_date')
    def _compute_date_order_custom(self):
        for rec in self:
            if rec.payment_date:
                rec.date_order_custom = rec.payment_date.strftime("%Y-%m-%d")