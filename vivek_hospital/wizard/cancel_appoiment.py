import datetime
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
from dateutil import relativedelta

class cancelappoimentwizard(models.TransientModel):
    _name = 'vivek.hospital.cancel.appoiment.wizard'
    _description = 'Cancel Appoiment Wizard'
    @api.model
    def default_get(self, fields_list):
        res=super(cancelappoimentwizard,self).default_get(fields_list)
        res['date_cancel']=fields.Datetime.now()
        return res

    appointment_id=fields.Many2one('vivek.hospital.appoiment',string="Appoiment",domain="[('state','=','confirm')]",required=True)
    reason=fields.Text(string="Reason for Cancellation",required=True)
    date_cancel=fields.Datetime(string="Cancellation Date")

    def action_cancel(self):
      cancel_day1=self.env['ir.config_parameter'].get_param('vivek_hospital.cancel_days')
      allowed_date=self.appointment_id.booking_date-relativedelta.relativedelta(days=int(cancel_day1))
      if self.appointment_id.booking_date == fields.Date.today():
            raise  ValidationError(_("You cannot cancel today's appointment."))
      elif allowed_date < fields.Date.today():
            raise  ValidationError(_("You cannot cancel appointment before %s days of booking date."%cancel_day1))
      else:
            self.appointment_id.action_cancel()
            return{ 
            'type':'ir.actions.client',
            'tag':'reload',
            }
    