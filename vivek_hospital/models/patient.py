from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil import relativedelta

class patient(models.Model):
    _name = 'vivek.hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Information'
    _rec_name='name'

    name = fields.Char(string='Patient Name', required=True,tracking=True)
    dob=fields.Date(string="dob")
    ref=fields.Char(string="Reference No",readonly=True)
    age = fields.Integer(string='Age',compute='_compute_age',tracking=True,store=True,inverse='_compute_dob')  
    
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender',tracking=True)
    active = fields.Boolean(string='Active', default=True)
    image=fields.Image(string="Patient Image")
    tag_ids=fields.Many2many('vivek.hospital.patient.tag',string="Tags")
    appoiment_count=fields.Integer(string="Appoiment Count",compute='_compute_appoiment_count')
    appoiment_ids=fields.One2many('vivek.hospital.appoiment','patient_id',string="Appoiments")
    parent=fields.Char(string="Parent Name")
    marital_status=fields.Selection([('single','Single'),('married','Married'),('divorced','Divorced')],string="Marital Status")
    partner_name=fields.Char(string="Partner Name")
    is_birthday=fields.Boolean(string="Is Birthday",compute='_compute_is_birthday')
    phone=fields.Char(string="Phone Number")
    email=fields.Char(string="Email")
    website=fields.Char(string="Website")


    @api.depends('appoiment_ids')
    def _compute_appoiment_count(self):
        for rec in self:
            rec.appoiment_count=self.env['vivek.hospital.appoiment'].search_count([('patient_id','=',rec.id)])
    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                today=fields.Date.today()
                rec.age=today.year-rec.dob.year
            else:
                rec.age=0
    @api.model
    def create(self, vals):
        vals['ref']=self.env['ir.sequence'].next_by_code('vivek.hospital.patient')
        return super(patient, self).create(vals)
    def write(self,vals):
        if  not self.ref:
            vals['ref']=self.env['ir.sequence'].next_by_code('vivek.hospital.patient')
        return super(patient, self).write(vals)
    def name_get(self):
        return [(record.id,"[%s]%s"%(record.ref, record.name))for record in self]
    @api.constrains('dob')
    def _check_dob(self):
        for rec in self:
            if rec.dob and rec.dob>fields.Date.today():
                raise  ValidationError("DOB cannot be set in the future.")
    @api.ondelete(at_uninstall=False)
    def _check_appoiment_before_delete(self):
        for rec in self:
            if rec.appoiment_ids:
                raise  ValidationError("You cannot delete a patient with existing appointments.")
    @api.depends('age')
    def _compute_dob(self):
        today=fields.Date.today()
        for rec in self:
            rec.dob=today-relativedelta.relativedelta(years=rec.age)
    @api.depends('dob')
    def _compute_is_birthday(self):
        today=fields.Date.today()
        for rec in self:
            if rec.dob and rec.dob.month==today.month and rec.dob.day==today.day:
                rec.is_birthday=True
            else:
                rec.is_birthday=False
    def action_view_appointments (self):
        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form,calendar',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'res_model': 'vivek.hospital.appoiment',
            'target': 'current',
        }

