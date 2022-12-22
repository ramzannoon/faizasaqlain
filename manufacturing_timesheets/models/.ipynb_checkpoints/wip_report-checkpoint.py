from odoo import models, fields, api


class WIPTimeSheetProductin(models.Model):
    _name = 'wip.reports'
    _description = 'WIP Reports'

    sale_order = fields.Many2one('sale.order',string='Sale')
    sale_category = fields.Many2one('fs.sale.categ',string='Sale category')
    name = fields.Char(string='Work Order')
    delay_days = fields.Char(string='Delay Days(hours)')
    origin = fields.Char(string='Sale Order')
    workcenter_id = fields.Many2one('mrp.workcenter')
    workorder_id = fields.Many2one('mrp.workorder', string='Workorder')
    # production_id = fields.Char(string='Product')
    production_id = fields.Many2one('mrp.production', string='Manufacturing Order')
    date_planned_start = fields.Datetime(string="Expected Date", )
    duration = fields.Char(string="Actual Duration(hours)")
    duration_expected = fields.Char(string="Duration Expected(hours)")

    date_planned_start = fields.Datetime(string="Expected(hours)")
    date_planned_finished = fields.Datetime(string="Expected Date End")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('progress', 'In Progress'), ('to_close', 'To Close'),
         ('done', 'Done'), ('cancel', 'Cancelled')], string='MO Status',
        copy=False, index=True, readonly=True, store=True, tracking=True,
       )
    employee_id = fields.Many2one('hr.employee', "Employee")

    sale_order_id = fields.Char(string="Sale Order")

    lst_price = fields.Float(string='Sale price')
    inventory_quantity  = fields.Float(string="Expected Cost")
    available_quantity = fields.Float(string="Actual Cost")

    state_pro = fields.Selection(
        [('pending', 'Pending'), ('ready', 'Ready'), ('progress', 'In Progress'), ('done', 'Finish'),
      ('cancel', 'Cancelled')], string='WO Status',
        copy=False, index=True, readonly=True, store=True, tracking=True,
    )


class WIPTimeSheetProductLine(models.Model):
    _name = 'wip.reports.line'
    _description = 'WIP Reports Line'

    product_uom_qty = fields.Char("Product Qty", store=True, )
    product_id = fields.Many2one('wip.reports', "Product")
    account_id = fields.Many2one('account.account', 'Journal')
    quantity = fields.Float('Quantity')
    forecast_availability = fields.Float('Forecast Availability')
    quantity_done = fields.Char("Quantity Done")

