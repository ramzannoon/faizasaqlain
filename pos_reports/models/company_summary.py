from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class POSCompanyAnalysis(models.Model):
    _name = 'pos.company.analysis'
    _description = "POS Company Analysis"

    name = fields.Char('Order')
    qty = fields.Char('Quantity')
    pos_order_id = fields.Char('order')
    order_date = fields.Datetime("Order Date")
    company = fields.Char("Company")

    def create_record(self, pos_rec):
        self.sudo().create({
            'name': pos_rec.order_id.name,
            'qty': pos_rec.qty,
            'order_date': pos_rec.order_id.date_order,
            'company': pos_rec.order_id.company_id.id,
            'pos_order_id': pos_rec.order_id.id,
        })

    def company_pos_records(self):
        pos_rec = self.env['pos.order.line'].search([])
        self_record = self.env['pos.company.analysis'].search([]).mapped('pos_order_id')
        if not self_record:
            for rec in pos_rec:
                self.create_record(rec)
        else:
            for order in pos_rec:
                if str(order.id) not in self_record:
                    self.create_record(order)
                else:
                    pass
