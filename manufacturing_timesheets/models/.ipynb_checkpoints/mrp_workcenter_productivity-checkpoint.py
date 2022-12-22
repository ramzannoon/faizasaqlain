from odoo import models, fields, api


class MRPWorkcenterProductivit(models.Model):
    _inherit = 'mrp.workcenter.productivity'

    test_timesheet = fields.Char("Reason")
    time_ids = fields.One2many('mrp.workcenter.productivity', 'workcenter_id', 'Time Logs')

    workingorder_id = fields.Many2one('mrp.production', "MRP")
    production_ids = fields.Many2one('product.product', string='Products')
    employee_id = fields.Many2one('res.partner', "Partner")

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
        ('pending', 'Pending'), ('paid', 'Paid'),
        ('cancel', 'Cancelled')], string='Status',
        default='pending', copy=False, readonly=True)
    duration_in_hours = fields.Float(string='Duration in Hours', compute='compute_duration')
    actual_cost = fields.Float(string='Actual Cost', compute='compute_actual_cost')
    date = fields.Date('Comment Date', default=date.today(), readonly=1)

    def compute_actual_cost(self):
        for rec in self:
            rec.actual_cost = rec.duration

    def action_create_bill(self):
        vendor_list = []
        record_ids = []
        for line in self:
            vendor_list.append(line.employee_id.id)
            record_ids.append(line.id)
        uniq_vendor_list = set(vendor_list)
        for vendor in uniq_vendor_list:
            product_list = []
            total_cost = 0
            uniq_timesheet = self.env['mrp.workcenter.productivity'].search([('employee_id', '=', vendor),
                                                                             ('id', 'in', record_ids)])
            for time_data in uniq_timesheet:
                total_cost += time_data.actual_cost
            product_list.append((0, 0, {
                'name': 'Employee Timesheet Bill',
                'quantity': 1,
                'price_unit': total_cost,
                'partner_id': vendor,
            }))
            vals = {
                'partner_id': vendor,
                'journal_id': self.env['account.journal'].search([('type', '=', 'purchase')], limit=1).id,
                'invoice_date': fields.Date.today(),
                'move_type': 'in_invoice',
                'invoice_origin': '',
                'invoice_line_ids': product_list
            }
            move = self.env['account.move'].create(vals)
            move.action_post()


    def compute_duration(self):
        for rec in self:
            rec.duration_in_hours = rec.duration / 60



class MRPWorkCenterRout(models.Model):
    _inherit = 'mrp.routing.workcenter'

    rate_per_hour = fields.Float(string='Rate Per Hour')

