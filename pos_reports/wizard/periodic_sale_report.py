from datetime import date
from odoo import api, models, fields


class PeriodicSaleReport(models.TransientModel):
    _name = "periodic.sale.report.wizard"
    _description = "Periodic Sale Report"


    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')
    user_ids = fields.Many2many('res.users', 'res_user_pos_report', string='SalePersons')

    def print_report(self):
        data = {
            'form': self.read()[0]}
        report_action = self.env.ref('pos_reports.action_periodic_sale_report_new').report_action(self, data=data)
        return report_action


    # def print_report(self):
    #     data = {
    #         'date_from': self.date_from,
    #         'date_to': self.date_to
    #     }
    #     return self.env.ref('pos_reports.action_periodic_sale_report_new').report_action(None, data=data)




