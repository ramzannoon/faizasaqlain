from odoo import models, fields, api


class MRPWorkcenterProductivit(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    test_timesheet = fields.Char("Reason")
    employee_id = fields.Many2one('hr.employee', "Partner")
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
        ('cancel', 'Cancelled')], string='MO Status',
        default='pending', copy=False, readonly=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('cancel', 'Cancelled')], string='Status',
        default='pending', copy=False, readonly=True)
    duration_in_hours = fields.Float(string='Duration in Hours', compute='compute_duration')
    actual_cost = fields.Float(string='Actual Cost')

    def action_create_bill(self):
        for rec in self:
            selected_ids = rec.env.context.get('active_ids', [])
            selected_records = rec.env['mrp.production'].browse(selected_ids)
        return {
            'name': ('Production Bill'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'create.bill.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def compute_duration(self):
        for rec in self:
            rec.duration_in_hours = rec.duration / 60


class MRPBOMMne(models.Model):
    _inherit = 'mrp.bom'

    @api.model
    def create(self, values):
        res = super(MRPWorkCenterRout, self)
        for line in res.operation_ids:
            self.env['mrp.workcenter.productivity'].create({
                'actual_cost': line.rate_per_hour,
            })
            return res


class MRPWorkCenterRout(models.Model):
    _inherit = 'mrp.routing.workcenter'

    rate_per_hour = fields.Float(string='Rate Per Hour' )



        # for line in self:
        #     self.env['mrp.workcenter.productivity'].create({
        #         'operation_ids': [(0, 0, {
        #             'rate_per_hour': line.rate_per_hour,
        #         })]
        #     })
        #     wip_rep = super(MRPWorkCenterRout, self).cost_calculate()
        #     return wip_rep
