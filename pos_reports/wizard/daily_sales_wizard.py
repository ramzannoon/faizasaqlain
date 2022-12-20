from odoo import api, models, fields, _


class SearchAndPrintCalendarWizard(models.TransientModel):
    _name = "school.search.wizard"
    _description = "Search and Print Calendar Wizard"

    # student_id = fields.Many2one('school.students', string='Student', required=True)
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')
    pos_config_ids = fields.Many2many('pos.config', 'pos_config_daily_sale_report', string='Point of Sales')


    def school_print_calendars(self):
        data = {
            'form': self.read()[0]}
        report_action = self.env.ref('pos_reports.action_daily_sales_details').report_action(self, data=data)
        return report_action