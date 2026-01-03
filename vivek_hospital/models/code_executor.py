from odoo import models, fields
import traceback

class CodeExecutor(models.Model):
    _name = 'hospital.code.executor'
    _description = 'Code Executor'

    code = fields.Text(string='Code')
    result = fields.Text(string='Result', readonly=True)

    def action_execute_test(self):
        for rec in self:
            if not rec.code:
                rec.result = ''
                continue

            # 👇 IMPORTANT: globals for exec
            exec_globals = {
                'env': rec.env,
                'self': rec,
            }

            try:
                wrapped_code = (
                    "def __user_code__():\n"
                    f"{self._indent_code(rec.code)}"
                )

                exec(wrapped_code, exec_globals)

                result = exec_globals['__user_code__']()
                rec.result = str(result)

            except Exception:
                rec.result = traceback.format_exc()

    def _indent_code(self, code):
        return '\n'.join('    ' + line for line in code.splitlines())


#Queries:

# 1.Create():
# return env['hospital.doctor'].create({
#     'name': 'Sasti Batli',
#     'age': '99',
# })    

# return env['hospital.doctor'].create([
#     {'name': 'Dr A'},
#     {'name': 'Dr B'},
#     {'name': 'Dr C','date': fields.Date.today(),},
# ])

# 2.Browse(): it allows only id in method
# return env['hospital.doctor'].browse() #hospital.doctor()

# return env['hospital.doctor'].browse(9).name #	Khopdi

# return env['hospital.doctor'].browse([1,21]).mapped('name') #['Harsh', 'Scammer']

# return env['hospital.doctor'].browse(100).exists() #hospital.doctor(10,) otherwise hospital.doctor()

# return env['hospital.doctor'].browse(10).read(['name', 'age']) #[{'id': 10, 'name': 'Scammer', 'age': 150}]

# 3.Write():
# return env['hospital.doctor'].browse(10).write({
#     'name': 'Scammer',
#     'age' : 150
# })

# return env['hospital.doctor'].search([('age', '>', 170)]).write({
#     'marital_status': 'married',
# })

# 4.Unlink(): #delete
# return env['hospital.doctor'].browse(55).unlink() #single record delete

# return env['hospital.doctor'].browse([59,60,61]).unlink() #multiple record delete

# env['hospital.doctor'].search([('age', '>', 400)]).unlink()

# 5.Search(): 
# #Optional parameters: limit, order, offset, count
# #Search using operators -> [= , != , > , < , >= , <= , like , ilike , in , not in , child_of]

# return env['hospital.doctor'].search([]) #hospital.doctor(1, 2, 3, 5, 6, ... , 38, 39, 40)

# return env['hospital.doctor'].search([('name', '=', 'Harsh')]) #hospital.doctor(1, 6, 7)

# return env['hospital.doctor'].search([
#     ('age', '>', 50),
#     ('marital_status', '=', 'married')
# ]) #hospital.doctor(15,)

# return env['hospital.doctor'].search([
#     '|',
#     ('age', '<', 20),
#     ('age', '>', 180),
# ]) #hospital.doctor(3, 5, 15)

# return env['hospital.doctor'].search([
#     '|',
#     '|',
#     ('age', '<', 20),
#     ('age', '>', 180),
#     ('marital_status', '=', 'single')
# ]) #hospital.doctor(2, 3, 5, 11, 15)

# 6.Search_count():

# return env['hospital.doctor'].search_count([('age', '>', 60)]) #Output = 4

# return env['hospital.doctor'].search_count([
#     ('age', '>', 60),
#     ('marital_status', '=', 'single')
# ]) #Output = 3

# return env['hospital.doctor'].search_count([
#     '|',
#     ('age', '<', 20),
#     ('age', '>', 180),
# ]) #output = 3

# abc = env['hospital.doctor'].search_count([('age', '>', 180)]) 
# if abc > 0:
#     return abc ##Output = 1

# 7.filtered():

# return env['hospital.doctor'].search([
#     ('name', '=', 'Harsh'),
# ]).filtered(lambda d: d.age > 20) #hospital.doctor(1, 6, 7)

# return env['hospital.doctor'].search([
#     ('name', '=', 'Harsh'),
# ]).filtered(lambda d: d.age > 20 and d.marital_status == 'single') #hospital.doctor(1, 7)

# return env['hospital.doctor'].search([
#     ('name', '=', 'Harsh'),
# ]).filtered(lambda d: d.age > 20).mapped('name') #['Harsh', 'Harsh', 'Harsh']