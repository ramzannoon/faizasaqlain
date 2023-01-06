# -*- coding: utf-8 -*-
# from odoo import http


# class IdtApprovalRequest(http.Controller):
#     @http.route('/idt_approval_request/idt_approval_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/idt_approval_request/idt_approval_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('idt_approval_request.listing', {
#             'root': '/idt_approval_request/idt_approval_request',
#             'objects': http.request.env['idt_approval_request.idt_approval_request'].search([]),
#         })

#     @http.route('/idt_approval_request/idt_approval_request/objects/<model("idt_approval_request.idt_approval_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('idt_approval_request.object', {
#             'object': obj
#         })
