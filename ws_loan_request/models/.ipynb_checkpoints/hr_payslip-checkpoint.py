# -*- coding: utf-8 -*-
import time
import babel
from odoo import models, fields, api, tools, _
from datetime import datetime
import base64

from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.addons.hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips, ResultRules
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_round, date_utils
from odoo.tools.misc import format_date
from odoo.tools.safe_eval import safe_eval

class HrPayslip(models.Model):
    _inherit = 'hr.payslip.input'

    loan_line_id = fields.Many2one('hr.loan.line', string='Loan Lines')    

    

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
            
            
    def compute_sheet(self):
        for payslip in self: 
            loan_amount= 0
            loan_type = []
            lon_obj = self.env['hr.loan.line'].search([('date','>=',payslip.date_from),('date','<=',payslip.date_to),('loan_id.employee_id', '=', payslip.employee_id.id), ('loan_id.state', '=', 'approve')])
            for loan_line in lon_obj:
                loan_type.append(loan_line.loan_id.loan_type_id.id)
            uniq_loan_type = set(loan_type)
            for uniq_type in uniq_loan_type:
                loan_type_code=0
                loan_type_amount=0
                lon_type_obj = self.env['hr.loan.line'].search([('loan_id.loan_type_id','=',uniq_type),('date','>=',payslip.date_from),('date','<=',payslip.date_to),('loan_id.employee_id', '=', payslip.employee_id.id), ('loan_id.state', '=', 'approve')])
                for ext_loan_line in lon_type_obj:
                    loan_type_code = ext_loan_line.loan_id.loan_type_id.code
                    loan_type_amount += ext_loan_line.amount
                    loan_line.update({
                        'payslip_id': payslip.id,
                        'paid': True,
                    }) 
                is_already_exist = 0 
                if loan_type_amount>0:
                    for other_input in payslip.input_line_ids:
                        if other_input.code==loan_type_code:
                            is_already_exist = 1    
                            other_input.unlink()
                    loan_typea = self.env['hr.loan.type'].search([('id','=',uniq_type)], limit=1)
                    input_type = self.env['hr.payslip.input.type'].search([('code','=',loan_type_code)], limit=1)
                    if not input_type:
                        type_vals = {
                            'name': loan_typea.name,
                            'code': loan_typea.code,
                        }
                        input_type = self.env['hr.payslip.input.type'].create(type_vals)
                    input_vals = {
                       'payslip_id': payslip.id,
                       'sequence': 1,
                       'code': input_type.code,
                       'contract_id': payslip.contract_id.id,
                       'input_type_id': input_type.id,
                       'amount': loan_type_amount,
                    }   
                    other_input = self.env['hr.payslip.input'].create(input_vals)                        
        res = super(HrPayslip, self).compute_sheet()
        return res
   


   