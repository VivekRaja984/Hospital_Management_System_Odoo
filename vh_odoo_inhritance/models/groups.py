from odoo import models, fields, api,_
class groups1(models.Model):
    _inherit = 'res.groups'

    def get_application_groups(self,domain):
        group_id = self.env.ref('account.group_show_line_subtotals_tax_included').id
        proforma_id = self.env.ref('sale.group_proforma_sales').id
        return super(groups1,self).get_application_groups(domain + [('id', 'not in', (group_id, proforma_id))])