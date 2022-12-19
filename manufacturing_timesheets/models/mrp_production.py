from odoo import models, fields, api


class ManufacturingTimesheetProduction(models.Model):
    _inherit = 'mrp.production'

    employee_id = fields.Many2one('hr.employee', "Employee")

    def button_manufacturing_timesheets(self):
        return {
            'name': 'Manufacturing Timesheets',
            'view_mode': 'tree,form',
            'res_model': 'account.analytic.line',
            'type': 'ir.actions.act_window',
        }


class ManufacturingTimesheetsWkOdr(models.Model):
    _inherit = 'mrp.workorder'

    line_ids = fields.One2many('mrp.workorder', 'employee_id', 'TimeSheet')
    employee_id = fields.Many2one('hr.employee', "Employee")
    timing_id = fields.One2many(
        'mrp.workcenter.productivity', 'workingorder_id', copy=False)
    actual_duration = fields.Float(string='Actual Duration', compute='_compute_actual_duration', store=True)

    @api.depends('time_ids', 'time_ids.duration')
    def _compute_actual_duration(self):
        for rec in self:
            duration = 0
            for line in rec.time_ids:
                duration += line.duration
            rec.actual_duration = duration
            wip = self.env['wip.reports'].search([('workorder_id', '=', rec.id)])
            wip.available_quantity = duration / 60

    @api.model
    def create(self, values):
        res = super(ManufacturingTimesheetsWkOdr, self).create(values)
        rate_po = 0
        for line in res.production_id.bom_id.operation_ids:
            if line.name == res.name:
                rate_po = round(((float(line.rate_per_hour) * float(line.time_cycle))))
        rate_po = rate_po * res.production_id.product_qty

        self.env['wip.reports'].create({
            'origin': res.production_id.origin,
            "production_id": res.production_id.id,
            "lst_price": res.product_id.lst_price,
            'workorder_id': res.id,
            "inventory_quantity": rate_po,
            'date_planned_start': res.date_planned_start,
            'date_planned_finished': res.date_planned_finished,
            'workcenter_id': res.workcenter_id.id,
            'duration_expected': res.duration_expected,
            'duration': res.duration / 60,
            'state_pro': res.state,
            'delay_days': round(((float(res.duration_expected) - float(res.duration)) / 1440), 2),
            'name': res.name,
            'state': res.production_id.state,
        })
        return res
