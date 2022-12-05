from odoo import fields, http, _
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager, get_records_pager
from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):
   @http.route(['/my/orders', '/my/orders/page/<int:page>'], type='http', auth="user", website=True)
   def portal_my_orders(self, page=1, date_begin=None, search=None, search_in='content', date_end=None, sortby=None, **kw):
       values = self._prepare_portal_layout_values()
       partner = request.env.user.partner_id
       SaleOrder = request.env['sale.order']
       domain = [
           ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
           ('state', 'in', ['sale', 'done'])
       ]
       searchbar_inputs = {
           'order': {'input': 'name', 'label': _('Search in Order ahsan ')},
           'all': {'input': 'all', 'label': _('Search in All ahsan shah')},
       }
       if search and search_in:
           search_domain = []
           if search_in in ('name', 'all'):
               search_domain = OR([search_domain, [('name', 'ilike', search)]])
           domain += search_domain
       searchbar_sortings = {
           'date': {'label': _('Order Date'), 'order': 'date_order desc'},
           'name': {'label': _('Reference'), 'order': 'name'},
           'stage': {'label': _('Stage'), 'order': 'state'},
       }
       # default sortby order
       if not sortby:
           sortby = 'date'
       sort_order = searchbar_sortings[sortby]['order']
       if date_begin and date_end:
           domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
       # count for pager
       order_count = SaleOrder.search_count(domain)
       # pager
       pager = portal_pager(
           url="/my/orders",
           url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
           total=order_count,
           page=page,
           step=self._items_per_page
       )
       # content according to pager
       orders = SaleOrder.search(domain, order=sort_order, limit=self._items_per_page, offset=pager['offset'])
       request.session['my_orders_history'] = orders.ids[:100]
       values.update({
           'date': date_begin,
           'orders': orders.sudo(),
           'search': search,
           'searchbar_inputs': searchbar_inputs,
           'search_in': search_in,
           'page_name': 'order',
           'pager': pager,
           'default_url': '/my/orders',
           'searchbar_sortings': searchbar_sortings,
           'sortby': sortby,
       })
       return request.render("sale.portal_my_orders", values)