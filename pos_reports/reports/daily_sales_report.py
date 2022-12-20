from odoo import api, fields, models, _
from datetime import date, timedelta


class DailySalesDetails(models.AbstractModel):
    _name = 'report.pos_reports.daily_sales_details_template'
    _description = 'Daily Sales Details Report'

    def _get_report_values(self, docids, data=None):

        model = self.env.context.get('active_model')
        active_record = self.env[model].browse(self.env.context.get('active_id'))

        start_date = active_record.date_from
        end_date = active_record.date_to

        company = self.env.company

        print("active record", active_record.date_from)
        print("active record", active_record.date_to)

        report = self.env['ir.actions.report']._get_report_from_name('pos_reports.periodic_sale_report_template')
        # docs = self.env[report.model].browse(docids)

        delta = timedelta(days=1)
        data = []
        # card = cash = check = total_cost = total_profit = 0.0
        qty = cost = sales = total = vat = invoiced = discount = profit = 0
        while start_date <= end_date:
            pos_orders = self.env['pos.order.line'].search(
                [('order_id.date_order_custom', '=', start_date.strftime("%Y-%m-%d")),
                 ('order_id.config_id', 'in', active_record.pos_config_ids.ids)])
            for order in pos_orders:
                vals = {
                    'date': start_date.strftime("%Y-%m-%d"),
                    'session': order.order_id.session_id.name,
                    'ref': order.order_id.name,
                    'invoice': order.order_id.account_move.name,
                    'customer': order.order_id.partner_id.name,
                    'method': order.order_id.payment_ids.payment_method_id.name,
                    'total_wo_vat': order.price_subtotal,
                    'cost': order.product_id.standard_price * order.qty,
                    'profit': order.price_subtotal - (order.product_id.standard_price * order.qty),
                    'vat': order.price_subtotal_incl - order.price_subtotal,
                    'total': order.price_subtotal_incl,
                    'company': company,
                }
                data.append(vals)
                qty += order.qty
                cost += order.product_id.standard_price * order.qty
                discount += (order.price_subtotal_incl * order.discount) / 100

            start_date += delta

        company = self.env.company

        payment_methods = self.env['pos.payment.method'].search([])
        payment_data = []

        for payment in payment_methods:
            payments = self.env['pos.payment'].search([('date_order_custom', '>=', active_record.date_from.strftime("%Y-%m-%d")),
                                                       ('date_order_custom', '<=', active_record.date_to.strftime("%Y-%m-%d")),
                                                       ('payment_method_id', '=', payment.id)])
            amount = 0
            if payments:
                for p in payments:
                    amount += p.amount
            payment_vals = {
                'name': payment.name,
                'amount': amount
            }
            payment_data.append(payment_vals)

        pos_orders = self.env['pos.order'].search(
            [('date_order_custom', '>=', active_record.date_from.strftime("%Y-%m-%d")),('date_order_custom', '<=', active_record.date_to.strftime("%Y-%m-%d")),
             ('config_id', 'in', active_record.pos_config_ids.ids)])
        for order in pos_orders:
            sales += order.amount_total - order.amount_tax
            vat += order.amount_tax
            invoiced += 0
            total += order.amount_total
        profit += total - cost

        return {
            'doc_model': 'pos.order',
            'doc_ids': docids,
            'data': data,
            'date_from': start_date.strftime("%Y-%m-%d"),
            'date_to': end_date.strftime("%Y-%m-%d"),
            'print_date': fields.Date.today(),
            'company': company,
            'payment_methods': payment_methods,
            'payment_data': payment_data,
            'total_qty': qty,
            'total_cost': cost,
            'sales_revenue': sales,
            'total_sales': total,
            'invoiced': invoiced,
            'vat': vat,
            'discount': discount,
            'profit': profit
        }

        # docs = self.env['pos.order'].browse(docids)
        # company = self.env.company
        # return {
        #     'doc_ids': docids,
        #     'docs': docs,
        #     'doc_model': 'pos.order',
        #     'company': company,
        # }
