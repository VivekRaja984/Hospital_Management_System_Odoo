from odoo import models, fields, api

class patient_tag(models.Model):
    _name = 'vivek.hospital.patient.tag'
    _description = 'Patient Tag'

    name=fields.Char(string="Tag Name",required=True)
    active=fields.Boolean(string="Active",default=True,copy=False)
    color=fields.Integer(string="Color")
    color_2=fields.Char(string="Color 2")
    sequence=fields.Integer(string="Sequence")

    _sql_constraints = [
        ('unique_tag_name','unique(name)','Tag Name must be unique.'),
        ('sequence_positive','check(sequence>0)','squence must be positive.')
    ]

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + ' (Copy)'
        default['sequence'] = 1
        return super(patient_tag, self).copy(default)