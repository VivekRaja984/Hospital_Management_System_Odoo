import random
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
class appoiment(models.Model):
    _name = 'vivek.hospital.appoiment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'appoiment Information'
    _rec_name = 'appoiment_id'
    _order='id desc'


    patient_id=fields.Many2one('vivek.hospital.patient',string='Patient',required=True,tracking=True,ondelete='restrict')
    gender=fields.Selection(related='patient_id.gender',readonly=True)
    appoiment_time=fields.Datetime(string="Appoiment Time",default=fields.Datetime.now,tracking=True)
    booking_date=fields.Date(string="Booking Date",default=fields.Date.today,tracking=True)
    ref=fields.Char(string="Reference No")
    prechription=fields.Html(string="Prechription")
    priority=fields.Selection([('0','Low'),('1','Medium'),('2','High'),('3','very_High')],string="Priority")
    state=fields.Selection([('draft','Draft'),('confirm','Confirmed'),('done','Done'),('cancel','Cancelled')],string="Status",default='draft',tracking=True)
    doctor_id=fields.Many2one('res.users',string="Doctor")
    pharmacy_line_ids=fields.One2many('vivek.hospital.appoiment.pharmacy.lines','appoiment_id',string="Pharmacy Lines")
    hidden_sales_price=fields.Boolean(string="Hide Sales Price")
    appoiment_id=fields.Char(string="Appoiment ID")
    operation_id=fields.Many2one('vivek.hospital.operation',string="Operation")
    progress=fields.Integer(string="Progress",compute='_compute_progress')
    duration=fields.Float(string="Duration")
    company_id=fields.Many2one('res.company',string="Company",default=lambda self: self.env.company)
    currency_id=fields.Many2one('res.currency',string="Currency",related='company_id.currency_id')

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                rec.progress = random.randint(0, 25)
            elif rec.state == 'confirm':
                rec.progress = random.randint(26, 75)
            elif rec.state == 'done':
                rec.progress = 100
            else:
                rec.progress = 0

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref=self.patient_id.ref

    def action_test(self):
        print("Confirmed")
        return{
            'type':'ir.actions.act_url',
            'url':'http://localhost:8098/web#cids=1&menu_id=5&action=37&model=ir.module.module&view_type=kanban'
        }
        
    def action_confirm(self):
        for rec in self:
            rec.state='confirm'
    def action_done(self):
        for rec in self:
            rec.state='done'
    def action_send_confirmation_email(self):
        templat=self.env.ref('vivek_hospital.email_template_appoiment_confirmation1')
        for rec in self:
            if rec.patient_id.email:  
                templat.send_mail(rec.id, force_send=True,email_values={'auto_delete': False})
            
    def action_cancel(self):
        for rec in self:
            rec.state='cancel'
    def action_Reset_to_draft(self):
        for rec in self:
            rec.state='draft'
    @api.model
    def create(self, vals):
        vals['appoiment_id']=self.env['ir.sequence'].next_by_code('vivek.hospital.appoiment')
        return super(appoiment, self).create(vals)
    def unlink(self):
        if self.state!='draft':
            raise ValidationError(_("Only draft appointments can be deleted."))
        return super(appoiment, self).unlink()

class AppomentpharmacyLines(models.Model):
    _name = 'vivek.hospital.appoiment.pharmacy.lines'
    _description = 'Appoiment Pharmacy Lines'

    
    product_id=fields.Many2one('product.product',string="Product",required=True)
    quantity=fields.Integer(string="Quantity",default=1)
    price=fields.Float(string="Price")
    appoiment_id=fields.Many2one('vivek.hospital.appoiment',string="Appoiment")
    price_subtotal=fields.Monetary(string="Subtotal",compute='_compute_price_subtotal',currency_field="company_currency_id")
    company_currency_id=fields.Many2one(related='appoiment_id.currency_id',string="Currency",readonly=True)
    @api.depends('quantity','price')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal=rec.quantity*rec.price