from odoo import models, fields, api


class MrpWorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    test_timesheet = fields.Char("Reason")
    name = fields.Char("Reason")
    picking_type_id = fields.Char("Reason")
    employee_id = fields.Many2one('hr.employee', "Employee")
    date_planned_start = fields.Datetime(
        'Scheduled Date', copy=False,
        help="Date at which you plan to start the production.",
        index=True, )
    date_planned_finished = fields.Datetime(
        'Scheduled End Date',
        help="Date at which you plan to finish the production.",
        copy=False)

    def button_mark_done(self):
        for line in self:
            self.env['wip.reports'].create({
                "sale_order_id": line.sale_order_id,
                "date_planned_start": line.date_planned_start,
                "product_qty": line.product_qty,
                "bom_id": line.bom_id.id,
                "user_id": line.user_id.name,
                "company_id": line.company_id.name,
                "product_id": line.product_id.name,
                'workorder_ids': [(0, 0, {
                    'product_id': line.product_id.name,
                    'date_planned_start': line.date_planned_start,
                    'duration_expected': line.duration_expected,
                })]
            })
            wip_rep = super(MrpWorkOrder, self).button_mark_done()
            return wip_rep
