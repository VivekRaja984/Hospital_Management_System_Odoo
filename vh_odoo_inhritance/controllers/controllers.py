# -*- coding: utf-8 -*-
# from odoo import http


# class VhOdooInhritance(http.Controller):
#     @http.route('/vh_odoo_inhritance/vh_odoo_inhritance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vh_odoo_inhritance/vh_odoo_inhritance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vh_odoo_inhritance.listing', {
#             'root': '/vh_odoo_inhritance/vh_odoo_inhritance',
#             'objects': http.request.env['vh_odoo_inhritance.vh_odoo_inhritance'].search([]),
#         })

#     @http.route('/vh_odoo_inhritance/vh_odoo_inhritance/objects/<model("vh_odoo_inhritance.vh_odoo_inhritance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vh_odoo_inhritance.object', {
#             'object': obj
#         })
