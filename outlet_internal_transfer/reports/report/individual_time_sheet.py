from odoo import api, models


class IndividualTimesheet(models.AbstractModel):
    _name = 'report.outlet_internal_transfer.individualtimesheet_template'
    _description = 'Individual Timesheet Report'

    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('outlet_internal_transfer.individualtimesheet_template')
        docs = self.env[report.model].browse(docids)
        company = self.env.company
        return {
            'company': company,
            'docs': docs,
        }
