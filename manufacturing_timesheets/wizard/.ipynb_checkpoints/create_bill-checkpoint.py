import pdb
from datetime import date
from odoo import api, fields, models, _


class CreateBillWizard(models.TransientModel):
    _name = 'create.bill.wizard'
    _description = 'Create Bill Wizard'

    def _default_vendor_bill(self):
         return self.env['account.journal'].search([('name', '=', 'Vendor Bills')], limit=1).id

    journal_id = fields.Many2one('account.journal', string='Journal',  default=_default_vendor_bill)
    date = fields.Date('Comment Date', default=date.today(), readonly=1)
    production_ids = fields.Many2many('product.product', string='Products')


    def add_action_create_bill(self):
        production_order = ' '
        sum_production_quantity = 0.0
        for production in self.production_ids:
            production_order += production.name + ' '
            sum_production_quantity = sum_production_quantity + production.product_qty
            production.update({
                'partner_id': self.partner_id.id,
                'journal_id': self.journal_id.id,
                'account_id': self.account_id.id,
                'cost': self.cost,
            })

        product_list = []
        product_list.append((0, 0, {
            'name': 'Production Bill',
            'account_id': self.journal_id.id,
            'quantity': 1,
            'price_unit': 1,
            'partner_id': self.journal_id.id,
        }))

        vals = {
            'partner_id': self.journal_id.id,
            'journal_id': self.journal_id.id,
            'invoice_date': fields.Date.today(),
            'move_type': 'in_invoice',
            'invoice_origin': production_order,
            'invoice_line_ids': product_list
        }
        move = self.env['account.move'].create(vals)

