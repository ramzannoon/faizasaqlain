from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class POSProductSession(models.Model):
    _name = 'session.pos.order'
    # _inherits = {'pos.order.line': 'pos_order_id'}
    _description = "POS Product Session"

    name = fields.Char('order Ref')
    order_date = fields.Datetime("Order Date")
    company_id = fields.Many2one('res.company', string='Company')
    amount_total = fields.Float(string='Total')
    pos_order_id = fields.Char()

    def create_record(self, pos_rec):
        self.sudo().create({
            'name': pos_rec.name,
            'company_id': pos_rec.company_id.id,
            'order_date': pos_rec.date_order,
            'amount_total': pos_rec.amount_total,
            'pos_order_id': pos_rec.id
        })

    def sale_pos_records(self):
        pos_rec = self.env['pos.order'].search([])
        self_record = self.env['session.pos.order'].search([]).mapped('pos_order_id')
        print(self_record)
        if not self_record:
            for rec in pos_rec:
                self.create_record(rec)
        else:
            for order in pos_rec:
                if str(order.id) not in self_record:
                    self.create_record(order)
                else:
                    pass
            #
            # for rec in self_record:
            #     if rec.pos_order_id
            # new_ids = [x for x in pos_rec.ids if x not in self_record]
            # if new_ids:
            #     pos_line_new_ids = self.env['pos.order'].browse(new_ids)
            #     self.create_record(pos_line_new_ids)
        # for order in pos_rec:
        #     for rec in self_record:
        #         if order.name == rec.name:
        #             pass
        #     self.create_record(pos_rec)


class POSCategorySummary(models.Model):
    _name = 'category.pos.order'
    _description = "POS Category"

    full_product_name = fields.Char('Product')
    category_id = fields.Many2one('product.category', string='Category')
    qty = fields.Char('Quantity')
    pos_order_id = fields.Char('order')
    order_date = fields.Datetime("Order Date")


    def create_record(self, pos_rec):
        self.sudo().create({
            'full_product_name': pos_rec.full_product_name,
            'category_id': pos_rec.product_id.categ_id.id,
            'order_date': pos_rec.order_id.date_order,
            'qty': pos_rec.qty,
            'pos_order_id': pos_rec.order_id.id
        })

    def category_pos_records(self):
        pos_rec = self.env['pos.order.line'].search([])
        self_record = self.env['category.pos.order'].search([]).mapped('pos_order_id')
        print(self_record)
        if not self_record:
            for rec in pos_rec:
                self.create_record(rec)
        else:
            for order in pos_rec:
                if str(order.id) not in self_record:
                    self.create_record(order)
                else:
                    pass


class POSUsersSummary(models.Model):
    _name = 'users.pos.order'
    _description = "POS Users Summary"

    user_id = fields.Many2one('res.users')
    pos_order_id = fields.Char()
    name = fields.Char("Order")
    cashier = fields.Char("Cashier")

    def create_record(self, pos_rec):
        self.sudo().create({
            'name': pos_rec.name,
            'pos_order_id': pos_rec.id,
            'user_id': pos_rec.user_id.id,
        })

    def users_pos_records(self):
        pos_rec = self.env['pos.order'].search([])
        self_record = self.env['users.pos.order'].search([]).mapped('pos_order_id')
        print(self_record)
        if not self_record:
            for rec in pos_rec:
                self.create_record(rec)
        else:
            for order in pos_rec:
                if str(order.id) not in self_record:
                    self.create_record(order)
                else:
                    pass


class POSCustomersSummary(models.Model):
    _name = 'customers.pos.order'
    _description = "POS Customers Summary"

    order_ref = fields.Char('Order')
    name = fields.Char('Order')
    partner_id = fields.Many2one('res.partner')
    pos_order_id = fields.Char()

    def create_record(self, pos_rec):
        self.sudo().create({
            'name': pos_rec.name,
            'pos_order_id': pos_rec.id,
            'partner_id': pos_rec.partner_id.id,
        })


    def customers_records(self):
        pos_rec = self.env['pos.order'].search([])
        self_record = self.env['customers.pos.order'].search([]).mapped('pos_order_id')
        print(self_record)
        if not self_record:
            for rec in pos_rec:
                self.create_record(rec)
        else:
            for order in pos_rec:
                if str(order.id) not in self_record:
                    self.create_record(order)
                else:
                    pass


class POSPaymentSummary(models.Model):
    _name = 'payment.pos.order'
    _description = "POS Payment Summary"

    payment = fields.Char('Order Ref')
    amount = fields.Char('Price')
    company = fields.Char("Company")

    def create_record(self, payment_pos_rec):
        company_id = self.env.user.company_id
        for line in payment_pos_rec:
            self.sudo().create({
                'payment': line.payment_method_id.display_name,
                'company':self.env.company.name,
                'amount':line.amount,
            })

    def payment_pos_records(self):
        payment_pos_rec = self.env['pos.payment'].search([])
        payment_self_record = self.env['payment.pos.order'].search([]).ids

        if not payment_self_record:
            self.create_record(payment_pos_rec)
        else:
            new_ids = [x for x in payment_pos_rec.ids if x not in payment_self_record]
            if new_ids:
                pos_line_new_ids = self.env['payment.pos.order'].browse(new_ids)
                self.create_record(pos_line_new_ids)


class POSCompanySummary(models.Model):
    _name = 'company.pos.order'
    _description = "POS company Summary"

    order_ref = fields.Char('Order Ref')
    date_order = fields.Datetime("Order Date")
    company_id = fields.Char("Company")