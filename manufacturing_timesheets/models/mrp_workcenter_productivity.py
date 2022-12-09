from odoo import models, fields, api


class MRPWorkcenterProductivit(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    test_timesheet = fields.Char("Reason")
    employee_id = fields.Many2one('hr.employee', "Employee")
    time_ids = fields.One2many('mrp.workcenter.productivity', 'workcenter_id', 'Time Logs')
    workingorder_id = fields.Many2one('mrp.production', "MRP", related='workorder_id.production_id', store=True)
    workorder_id = fields.Many2one('mrp.workorder', "Work Order", store=True)
    date = fields.Date(string="Date")
    worked_hours = fields.Date(string="Worked Hours test")
    state = fields.Selection([
        ('pending', 'Waiting for another WO'),
        ('ready', 'Ready'),
        ('progress', 'In Progress'),
        ('done', 'Finished'),
        ('cancel', 'Cancelled')], string='Status',
        default='pending', copy=False, readonly=True)

    # @api.onchange('duration')
    # def onchange_duration(self):
    #     for rec in self:
    #          rec.workorder_id.actual_duration = rec.duration