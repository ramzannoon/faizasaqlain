from datetime import datetime
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
    commission = fields.Float('Commission %', compute='_compute_commission', store=True)

    debit_invoice_id = fields.Many2one('account.account', string='Debit Invoice')
    credit_invoice_id = fields.Many2one('account.account', string='Credit Invoice')
    journal_id = fields.Many2one('account.journal')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, help="Employee")
    actual_amount = fields.Float('Commision Amount', compute='_compute_actual_amount', store=True)

    j_entry_id = fields.Many2one('account.move', string="Journal Entry", store=True)

    def button_journal_entry(self):
        f = 9
        return {
            'name': 'Journal Entry',
            'view_type': 'form',
            'view_mode': 'form',
            # 'view_id': self.j_entry_id.id,
            'res_id': self.j_entry_id.id,
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
        }

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

    @api.depends('sale_target', 'amount_paid')
    def _compute_commission(self):
        for record in self:
            value = 1.2
            record.commission = (value * record.sale_target) / 100

    @api.depends('amount_paid')
    def _compute_actual_amount(self):
        for record in self:
            record.actual_amount = record.amount_paid * 100


    def action_draft(self):
        self.state = 'draft'

    def action_posted(self):
        self.state = 'posted'
        for rec in self:
            move = self.env['account.move'].create({
                'move_type': 'entry',
                'date': datetime.today(),
                'journal_id': rec.journal_id.id,
                'line_ids': [(0, 0, {
                    'account_id': rec.debit_invoice_id.id,
                    'partner_id': rec.sale_person.id,
                    # 'currency_id': rec.currency_data['currency'].id,
                    'debit': rec.commission,
                    'credit': 0,
                    'amount_currency': 200.0,
                }),
                             (0, 0, {
                                 'account_id': 2,
                                 'partner_id': rec.sale_person.id,
                                 # 'currency_id': rec.currency_data_2['currency'].id,
                                 'debit': 0,
                                 'credit': rec.commission,

                             })]})
            self.write({
                'state': "posted"
            })
            self.j_entry_id = move.id
            return move

    def action_cancel(self):
        self.state = 'cancel'

    def button_sale_targets(self):
        return {
            'name': 'Actual Sale',
            'view_mode': 'tree,form',
            'res_model': 'pos.order',
            'type': 'ir.actions.act_window',
        }


# class MRPWorkCenterRout(models.Model):
#     _inherit = 'mrp.routing.workcenter'
#
#     rate_per_hour = fields.Float(string='Rate Per Hour')
