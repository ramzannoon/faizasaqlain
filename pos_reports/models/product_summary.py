
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class POSProductSummary(models.Model):
    _name = 'pos.product.summary'
    # _inherits = {'pos.order.line': 'pos_order_id'}
    _description = "POS Product Summary"

    # pos_order_id = fields.Many2one('pos.order.line')
    full_product_name = fields.Char('Product')
    qty = fields.Char('Quantity')
    price_unit = fields.Char('Price')
    pos_order_id = fields.Char('order')
    order_date= fields.Datetime("Order Date")
    unique_id = fields.Integer()

    company = fields.Char("Company")

    def create_record(self, pos_rec):
        company_id = self.env.user.company_id
        for line in pos_rec:
            self.sudo().create({
                'full_product_name': line.full_product_name,
                'qty': line.qty,
                'price_unit': line.price_unit,
                'unique_id': line.id,
                'order_date': line.order_id.date_order,
                'company':self.env.company.name,
            })

    def pos_records(self):
        pos_rec = self.env['pos.order.line'].search([])
        self_record = self.env['pos.product.summary'].search([]).ids
        if not self_record:
            self.create_record(pos_rec)
        else:
            new_ids = [x for x in pos_rec.ids if x not in self_record]
            if new_ids:
                pos_line_new_ids = self.env['pos.order.line'].browse(new_ids)
                self.create_record(pos_line_new_ids)












    # assess_list = []
    # for rec in progress_rec_rec:
    #     line_ids = rec.registration_component_ids.student_id.ids
    #     if wiz_student_id in line_ids:
    #         assessment_ids = rec.assessment_ids
    #         if assessment_ids:
    #             for line in assessment_ids:
    #                 assessment_lines = line.assessment_lines
    #                 for std in assessment_lines:
    #                     if std.student_id.id == wiz_student_id:
    #                         std_dic = {
    #                             'student_id': std.student_id.name,
    #                             'max_marks': std.max_marks,
    #                             'obtained_marks': std.obtained_marks,
    #                             'percentage': std.percentage,
    #                             'course': rec.name,
    #                         }
    #                         assess_list.append(std_dic)

    # docargs = {
    #     'doc_ids': [],
    #     'data': data['form'],
    #     'date': str(fields.Datetime.now()),
    #     'assess_list': assess_list,
    #     # 'student': student or False,
    #     # 'term': term or False,
    #     # 'template_list': template_list,
    #
    # }
    # print(assess_list, 4444444444444444444444444444444)
    # return docargs



