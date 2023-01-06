from odoo import models, fields, api
from odoo.exceptions import UserError


class OutletInternalTransfer(models.Model):
    _name = "outlet.internal.transfer"
    _inherit = "mail.thread"
    _description = "Outlet Internal Transfer"
    _order = "name"

    date = fields.Date(string="Date", required=True, help="Date of the Shop")
    name = fields.Char()
    sequence = fields.Char(string='Order Reference', required=True,
                           readonly=True, default='New')
    from_shop_id = fields.Many2one('pos.config', string="Shop From", required=True)
    to_shop_id = fields.Many2one('pos.config', string="Shop To", required=True)

    state = fields.Selection(
        [('draft', 'Draft'), ('approved', 'Approved'), ('cancelled', 'Cancelled')],
        'Status', default='draft')
    outlet_internal_lines = fields.One2many('outlet.internal.transfer.line', 'outlet_internal_transfer_id', string="Outlet Line",
                                            index=True)

    # def write(self, vals):
    #     if any(state == 'approved' for state in set(self.mapped('state'))):
    #         raise UserError("No edit in done state")
    #     else:
    #         return super().write(vals)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'pos.sale.targets') or 'New'
        res = super(OutletInternalTransfer, self).create(vals)
        return res

    def action_approve(self):
        self.write({
            'state': "approved"
        })
        picking_type_id = self.env['stock.picking.type'].search([('code', '=', "internal")], limit=1)
        print("picking type", picking_type_id.name)
        stock_picking_id = self.env['stock.picking'].create({
            'scheduled_date': self.date,
            'picking_type_id': picking_type_id.id,
            'location_id': self.from_shop_id.picking_type_id.default_location_src_id.id,
            'location_dest_id': self.to_shop_id.picking_type_id.default_location_src_id.id,
        })
        for line in self.outlet_internal_lines:
            self.env['stock.move'].create({
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'product_uom': line.product_id.uom_id.id,
                'product_uom_qty': line.quantity,
                'picking_id': stock_picking_id.id,
                'company_id': self.env.company.id,
                'date': self.date,
                'location_dest_id': self.to_shop_id.picking_type_id.default_location_src_id.id,
                'location_id': self.from_shop_id.picking_type_id.default_location_src_id.id,

            })
        state_change = stock_picking_id.write({'state': 'assigned'})
        return state_change


    def action_reset(self):
        self.write({
            'state': "draft"
        })

    def action_cancel(self):
        self.write({
            'state': "cancelled"
        })

    def button_sale_internal_transfer(self):
        return {
            'name': 'Internal Transfer Sale',
            'view_mode': 'tree,form',
            'res_model': 'pos.order',
            'type': 'ir.actions.act_window',
        }

class OutletInternalTransferLine(models.Model):
    _name = "outlet.internal.transfer.line"
    _description = "Outlet Internal Transfer Line"

    product_id = fields.Many2one('product.product', string="Product", help="Product")
    quantity = fields.Float(string="Quantity", required=True, help="Quantity")
    on_hand_quantity = fields.Float(string="Available qty")
    state = fields.Selection(
        [('draft', 'Draft'), ('approved', 'Approved'), ('cancelled', 'Cancelled')],
        'Status', default='draft', related='outlet_internal_transfer_id.state')
    outlet_internal_transfer_id = fields.Many2one('outlet.internal.transfer', string="Outlet Internal Transfer", help="Outlet", invisible=True)

    @api.onchange('product_id')
    def product_location_change(self):
        if self.product_id:
            stock_quant_ids = self.env['stock.quant'].search([('product_id', '=', self.product_id.id),
                                                              ('location_id', '=', self.outlet_internal_transfer_id.from_shop_id.picking_type_id.default_location_src_id.id)])
            available_quantity = 0
            for quants in stock_quant_ids:
                available_quantity += quants.quantity
            if available_quantity < 0:
                self.on_hand_quantity = 0
            else:
                self.on_hand_quantity = available_quantity



