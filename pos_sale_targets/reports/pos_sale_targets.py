from odoo import api, models


class PosSaleTarget(models.AbstractModel):
    _name = 'report.pos_sale_targets.pos_sale_targets_template'
    _description = 'Purchase Requisition Report'

    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('pos_sale_targets.pos_sale_targets_template')
        docs = self.env[report.model].browse(docids)
        company = self.env.company
        return {
            'company': company,
            'docs': docs,
        }
