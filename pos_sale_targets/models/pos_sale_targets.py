from odoo import models, fields, api


class POSSaleTargets(models.Model):
    _name = 'pos.sale.targets'
    _description = 'WIP Reports'

    sale_person = fields.Many2one('res.users', string='Sale Person')
    date_from = fields.Datetime(string="Date From")
    date_to = fields.Datetime(string="Date To")
    sale_target = fields.Float(string='Sale Target')
    amount_paid = fields.Float(string='Actual Sale', compute='_compute_get_commsion')

    state = fields.Selection([('draft', 'Draft'),
                              ('posted', 'Posted'),
                              ('cancel', 'Cancel')], string="State")
    commission = fields.Float('Total commission')

    @api.depends('sale_person')
    def _compute_get_commsion(self):
        for record in self:
            orders = self.env['pos.order'].search([('date_order', '>=', record.date_from),
                                                    ('date_order', '<=', record.date_to),
                                                   ('user_id', '=', record.sale_person.id)])
            sum = 0
            for ord in orders:
                sum += ord.amount_total
            record.amount_paid = sum

    def action_draft(self):
        self.state = 'draft'

    def action_posted(self):
        self.state = 'posted'

    def action_cancel(self):
        self.state = 'cancel'

    def button_sale_targets(self):
        return {
            'name': 'Actual Sale',
            'view_mode': 'tree,form',
            'res_model': 'pos.order',
            'type': 'ir.actions.act_window',
        }


class MRPWorkCenterRout(models.Model):
    _inherit = 'mrp.routing.workcenter'

    rate_per_hour = fields.Float(string='Rate Per Hour')

