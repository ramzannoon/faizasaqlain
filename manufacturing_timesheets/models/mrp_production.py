from odoo import models, fields, api


class ManufacturingTimesheets(models.Model):
    _inherit = 'mrp.production'

    line_ids = fields.One2many('mrp.workorder', 'employee_id', 'TimeSheet')
    employee_id = fields.Many2one('hr.employee', "Employee")

    timing_id = fields.One2many(
        'mrp.workcenter.productivity', 'workingorder_id', copy=False)

    @api.model
    def create(self, values):
        res = super(ManufacturingTimesheets, self).create(values)
        for line in res.workorder_ids:
            check = self.env['wip.reports'].create({
                'origin': res.origin,
                'state': res.state,
                "production_id": line.production_id.id,
                "lst_price": line.product_id.lst_price,
                # "inventory_quantity": line.product_id.qty_available.inventory_quantity,
                # "available_quantity": line.product_id.qty_available.available_quantity,
                'date_planned_start': line.date_planned_start,
                'date_planned_finished': line.date_planned_finished,
                'workcenter_id': line.workcenter_id.id,
                'duration_expected': line.duration_expected,
                'duration': line.duration,
                'state_pro': line.state,
                'delay_days': round(((float(line.duration_expected) - float(line.duration)) / 1440), 2),
                'name': line.name,
            })
            return res

    def button_manufacturing_timesheets(self):
        return {
                'name': 'Manufacturing Timesheets',
                'view_mode': 'tree,form',
                'res_model': 'account.analytic.line',
                'type': 'ir.actions.act_window',
            }
