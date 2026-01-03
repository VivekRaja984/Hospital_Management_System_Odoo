
from odoo import models, fields, api
class SaleOrderInherit(models.Model):
    _inherit = 'vivek.hospital.appoiment'

    confirmed_user_id = fields.Many2one('res.users', string='Confirmed By')
    def action_done(self):
        print("sucess.....")
        super(SaleOrderInherit, self).action_done()
        self.confirmed_user_id = self.env.user.id
        return {
            'effect':{
                'fadeout': 'slow',
                'message': 'Appointment Confirmed',
                'type': 'rainbow_man'
            }
        }

        
   