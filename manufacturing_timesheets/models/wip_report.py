from odoo import models, fields, api


class WIPTimeSheetProductin(models.Model):
    _name = 'wip.reports'
    _description = 'WIP Reports'

    sale_order = fields.Many2one('sale.order',string='Sale')
    sale_category = fields.Many2one('fs.sale.categ',string='Sale category')
    name = fields.Char(string='Work Order')
    delay_days = fields.Char(string='Delay Days(Days)')
    origin = fields.Char(string='Sale Order')
    workcenter_id = fields.Many2one('mrp.workcenter')
    # production_id = fields.Char(string='Product')
    production_id = fields.Many2one('mrp.production', string='Manufacturing Order')
    date_planned_start = fields.Datetime(string="Expected Date", )
    duration = fields.Char(string="Duration(Minutes")
    duration_expected = fields.Char(string="Duration Expected(Minutes)")
    date_planned_start = fields.Datetime(string="Expected(Minutes)")
    date_planned_finished = fields.Datetime(string="Expected Date End")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('progress', 'In Progress'), ('to_close', 'To Close'),
         ('done', 'Done'), ('cancel', 'Cancelled')], string='State',
        copy=False, index=True, readonly=True, store=True, tracking=True,
       )
    employee_id = fields.Many2one('hr.employee', "Employee")
    lst_price = fields.Char('Sale price')
    sale_order_id = fields.Char(string="Sale Order")
    inventory_quantity = fields.Char(string="Expected Cost")
    available_quantity = fields.Char(string="Actual Cost")
    state_pro = fields.Selection(
        [('pending', 'Pending'), ('ready', 'Ready'), ('progress', 'In Progress'), ('done', 'Finish'),
      ('cancel', 'Cancelled')], string='State',
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

