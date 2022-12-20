import pdb
import calendar
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class CustomerSummary(models.Model):
    _name = 'customer.summary'
    _description = "Customer Summary"

    name = fields.Char('Name')
    code = fields.Char('Code')
    unitime_id = fields.Integer()