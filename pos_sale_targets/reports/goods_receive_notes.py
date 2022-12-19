from odoo import api, models


class GoodsReceiveNotes(models.AbstractModel):
    _name = 'report.pos_sale_targets.goods_receive_notes_template'
    _description = 'Goods Receive Report'

    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('pos_sale_targets.goods_receive_notes_template')
        docs = self.env[report.model].browse(docids)
        company = self.env.company
        return {
            'company': company,
            'docs': docs,
        }
