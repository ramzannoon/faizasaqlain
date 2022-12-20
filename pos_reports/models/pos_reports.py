import pdb
import calendar
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


# class BoardDashboard(models.Model):
#     _name = 'customer.summary'
#     _description = "Customer Summary"
#
#     name = fields.Char('Name')
#     code = fields.Char('Code')
#     unitime_id = fields.Integer()


class BoardDashboard(models.Model):
    _name = 'board.board'
    _description = "Dash board"

    full_product_name = fields.Char('Product')
    qty = fields.Char('Quantity')
    price_unit = fields.Char('Price')
    pos_order_id = fields.Char('order')
    order_date = fields.Datetime("Order Date")
    unique_id = fields.Integer()
    company = fields.Char("Company")

    def create_record(self, pos_rec):
        company_id = self.env.user.company_id
        for line in pos_rec:
            self.sudo().create({
                'full_product_name': line.full_product_name,
                'qty': line.qty,
                'price_unit': line.price_unit,
                'unique_id': line.id,
                'order_date': line.order_id.date_order,
                'company': self.env.company.name,
            })

    def board_pos_records(self):
        pos_rec = self.env['pos.order.line'].search([])
        self_record = self.env['board.board'].search([]).ids
        if not self_record:
            self.create_record(pos_rec)
        else:
            new_ids = [x for x in pos_rec.ids if x not in self_record]
            if new_ids:
                pos_line_new_ids = self.env['pos.order.line'].browse(new_ids)
                self.create_record(pos_line_new_ids)








