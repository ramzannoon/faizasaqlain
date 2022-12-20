from odoo import api, models, fields
from datetime import date, timedelta


class PeriodicSaleReport(models.AbstractModel):
    _name = 'report.pos_reports.periodic_sale_report_template'
    _description = 'Periodic Sale Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("data", data)
        model = self.env.context.get('active_model')
        active_record = self.env[model].browse(self.env.context.get('active_id'))

        start_date = active_record.date_from
        end_date = active_record.date_to

        print("active record", active_record.date_from)
        print("active record", active_record.date_to)

        report = self.env['ir.actions.report']._get_report_from_name('pos_reports.periodic_sale_report_template')
        # docs = self.env[report.model].browse(docids)

        data = []

        delta = timedelta(days=1)
        total_qty = total_vat = total_saless = total_cost = total_profit = 0.0
        while start_date <= end_date:
            pos_orders = self.env['pos.order'].search(
                [('date_order_custom', '=', start_date.strftime("%Y-%m-%d")), ('user_id', 'in', active_record.user_ids.ids)])
            vat = cost = total_sales = qty = total_untaxed = profit = no_of_transactions = 0.0
            for order in pos_orders:
                no_of_transactions = len(pos_orders)
                for line in order.lines:
                    cost += line.price_unit
                    qty += line.qty
                vat += order.amount_tax
                total_sales += order.amount_total
                total_untaxed += order.amount_total - order.amount_tax
                profit += order.amount_total
            profit = profit - cost
            vals = {
                'date': start_date.strftime("%Y-%m-%d"),
                'no_of_transactions': no_of_transactions,
                'qty': qty,
                'total_sales': total_sales,
                'total_untaxed': total_untaxed,
                'cost': cost,
                'vat': vat,
                'profit': profit
            }
            data.append(vals)
            total_vat += vat
            total_cost += cost
            total_qty += qty
            total_profit += profit
            total_saless += total_sales
            start_date += delta
        company = self.env.company
        return {
            'doc_model': 'pos.order',
            'doc_ids': docids,
            'data': data,
            'users': active_record.user_ids,
            'print_date': fields.Date.today(),
            'date_from': start_date.strftime("%Y-%m-%d"),
            'date_to': end_date.strftime("%Y-%m-%d"),
            # 'docs': docs,
            'company': company,
            'total_vat': total_vat,
            'total_cost': total_cost,
            'total_qty': total_qty,
            'total_profit': total_profit,
            'total_saless': total_saless,
        }







# class GatePass(models.AbstractModel):
#     _name = 'report.purchase_reports.returnable_gate_pass_template'
#     _description = 'Returnable Gate Report'
#
#     def _get_report_values(self, docids, data=None):
#         report = self.env['ir.actions.report']._get_report_from_name('purchase_reports.returnable_gate_pass_template')
#
#         doc = self.env[report.model].browse(docids)
#         company = self.env.company
#         return {
#             'doc_model': 'stock.picking',
#             'doc_ids': docids,
#             'docs': doc,
#             'company': company,
#         }
#
#
#
# class OutGatePass(models.AbstractModel):
#     _name = 'report.purchase_reports.out_gate_pass_template'
#     _description = 'Returnable Gate Report'
#
#     def _get_report_values(self, docids, data=None):
#         report = self.env['ir.actions.report']._get_report_from_name('purchase_reports.out_gate_pass_template')
#
#         doc = self.env[report.model].browse(docids)
#         company = self.env.company
#         return {
#             'doc_model': 'stock.picking',
#             'doc_ids': docids,
#             'docs': doc,
#             'company': company,
#         }
