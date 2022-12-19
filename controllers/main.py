from odoo import http

from odoo.http import request


class WebsiteForm(http.Controller):

    @http.route(['/repairorder/submit'], type='http', auth="user", website=True)
    def repair_submit(self, **post):
        # **post is a keyword argument,A keyword argument is where you provide a name to the variable as you pass it -
        # - into the function.
        company_id = request.env['res.company'].browse(request._context.get('allowed_company_ids'))
        dest_location = request.env['stock.location'].search(
            [('usage', '=', 'internal',), ('name', '=', 'Stock'), ('company_id', '=', company_id.id)])
        product = post.get('product_id')
        product_obj = request.env['product.product'].sudo().search([('id', '=', product)])
        uom_id = ""
        for rec in product_obj:
            uom_id = rec.uom_id.id
        request.env['repair.order'].sudo().create({
            'description': post.get('description'),
            'product_id': post.get('product_id'),
            'product_qty': post.get('quantity'),
            'partner_id': post.get('partner_id'),
            'product_uom': uom_id,
            'location_id': dest_location.id,
        })
        orders = request.env['repair.order'].sudo().search([], order='id DESC', limit=5)
        order_list = []
        order_list.clear()
        for i in orders:
            items = i.read(
                ['description', 'product_id', 'product_qty',
                 'partner_id', 'product_uom', 'name'])[0]
            order_list.append(items)
        values = {}
        print(order_list)
        values.update({
            'orders': order_list
        })
        return request.render("website_repair_order.repair_order_form_success", values)

    @http.route(['/repair_order/form'], type='http', auth="user", website=True)
    def repair_order(self):
        orders = request.env['sale.order'].sudo().search([('state', '=', 'sale')])
        partner = []
        partner.clear()
        for i in orders:
            if i.partner_id not in partner:
                partner.append(i.partner_id)
        partners = partner
        values = {}
        values.update({
            'partners': partners,
        })
        return request.render("website_repair_order.online_repair_request", values)

    @http.route(['/repair_order/product'], type='json', auth="public", website=True)
    def repair_product(self, **kwargs):
        partner_id = kwargs.get("customer_name")
        orders = request.env['sale.order'].sudo().search([('partner_id', '=', int(partner_id))])
        product = []
        product.clear()
        for i in orders.order_line:
            if [i.product_id.id, i.product_id.name] not in product:
                product.append([i.product_id.id, i.product_id.name])
        values = {}
        values.update({
            'product_id': product
        })
        return values

    @http.route(['/repairorder'], type='http', auth="user", website=True)
    def repair_view(self, **post):
        orders = request.env['repair.order'].sudo().search([], order='id DESC', limit=5)
        order_list = []
        order_list.clear()
        for i in orders:
            items = i.read(
                ['description', 'product_id', 'product_qty',
                 'partner_id', 'product_uom', 'name', 'state'])[0]
            order_list.append(items)
        values = {}
        print(order_list)
        values.update({
            'orders': order_list
        })
        return request.render("website_repair_order.repair_order_tree_view", values)
