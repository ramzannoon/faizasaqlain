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
        ('pending', 'Pending'), ('paid', 'Paid'),
        ('cancel', 'Cancelled')], string='Status',
        default='pending', copy=False, readonly=True)
    duration_in_hours = fields.Float(string='Duration in Hours', compute='compute_duration')
    actual_cost = fields.Float(string='Actual Cost', compute='compute_actual_cost')

    # def _default_vendor_bill(self):
    #      return self.env['account.journal'].search([('name', '=', 'Vendor Bills')], limit=1).id

    # journal_id = fields.Many2one('account.journal', string='Journal',  default=_default_vendor_bill)
    date = fields.Date('Comment Date', default=date.today(), readonly=1)
    production_ids = fields.Many2many('product.product', string='Products')

    def compute_actual_cost(self):
        print(self, 11111111111111)
        for rec in self:
            print(rec, 11111111111111)
            rec.actual_cost = rec.duration
            print(rec, 444444444444444)

    def action_create_bill(self):

        for rec in self:
            if rec.status == 'paid':
                pass
            product_list = []
            product_list.append((0, 0, {
                'name': 'Production Bill',
                'account_id': rec.workorder_id,
                'quantity': 1,
                'price_unit': rec.actual_cost,
                'partner_id': rec.employee_id.id,
            }))
            vals = {
                'partner_id': rec.employee_id.id,
                'journal_id': rec.env['account.journal'].search([('name', '=', 'Vendor Bills')], limit=1).id,
                'invoice_date': fields.Date.today(),
                'move_type': 'in_invoice',
                'invoice_origin': 1,
                'invoice_line_ids': product_list,
                # 'state': self.write({'state': 'posted'})
            }
            move = self.env['account.move'].create(vals)
            rec.status = 'paid'

    def compute_duration(self):
        for rec in self:
            rec.duration_in_hours = rec.duration / 60


#
# class MRPBOMMne(models.Model):
#     _inherit = 'mrp.bom'


class MRPWorkCenterRout(models.Model):
    _inherit = 'mrp.routing.workcenter'

    rate_per_hour = fields.Float(string='Rate Per Hour')

    # @api.model
    # def create(self, values):
    #     print(self,111111111111111)
    #     res = super(MRPWorkCenterRout, self)
    #     print(res,222222222222222)
    #     for line in res.operation_ids:
    #         print(line, 3333333333333)
    #         self.env['mrp.workcenter.productivity'].create({
    #             'actual_cost': line.rate_per_hour,
    #         })
    #         print(line, 3333333333333)
    #         return res
