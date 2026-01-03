from odoo import models, fields, api,_
class operation(models.Model):
    _name = 'vivek.hospital.operation'
    _description = 'Operation Information'
    _log_access = False

    doctor_id=fields.Many2one('res.users',string="Doctor")
    operation_name=fields.Char(string="Operation Name",required=True)
    ref_record=fields.Reference(string="Reference Record",selection=[('vivek.hospital.appoiment','Appointment'),('vivek.hospital.patient','Patient')])

    @api.model
    def name_create(self, name):
        return self.create({'operation_name': name}).name_get()[0]
    
