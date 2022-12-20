from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class GoogleSpreadSheet(models.Model):
    _inherit = 'ir.attachment'
    _description = "Google Spread Sheet"
    _rec_name = 'name'

    # name = fields.Char('Name')
    # url = fields.Char('Url')
    # description = fields.text('Description')


