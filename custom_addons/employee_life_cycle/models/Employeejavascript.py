from odoo import fields ,models ,api
from datetime import datetime
# import datetime





class EmployeeModify(models.Model):
    _name = 'emp.loyee'


    def send_loactions(self):
        data = self.env['hr.employee'].search([])
        ids = []
        vals = []
        dict = {}

        for rec in data:
            if(rec.unit_name_hr.name!=False):
                ids.append(rec.id)
                vals.append(rec.unit_name_hr.name)
                # dict[rec.unit_name_hr.name] = rec.id
        print('888888888888888888888888888888888888')
        print(ids)
        print(vals)
        print(dict)
        data=list(set(vals))
        for val in vals:
            if(val in dict):
                dict[val]+=1
            else:
                dict[val]=1
        print(dict)



        # vals2=[f]
        print(dict)
        return [ids, vals, dict,data]
    def browse_record(self,val):
        # data=self.env['hr.employee'].search_count(['unit_name_hr','=',val])
        # print(data)
        print('aaaaaaaaaa')
        # return [data]

    def send_departments(self):
        data = self.env['hr.employee'].search([])
        ids = []
        vals = []
        dict = {}

        for rec in data:
            if (rec.department_id.name != False):
                ids.append(rec.id)
                vals.append(rec.department_id.name)
                # dict[rec.unit_name_hr.name] = rec.id
        print('888888888888888888888888888888888888')
        print(ids)
        print(vals)
        print(dict)
        data = list(set(vals))
        for val in vals:
            if (val in dict):
                dict[val] += 1
            else:
                dict[val] = 1
        print(dict)

        # vals2=[f]
        print(dict)
        return [ids, vals, dict,data]

    def send_jobs(self):
        data = self.env['hr.employee'].search([])
        ids = []
        vals = []
        dict = {}

        for rec in data:
            if (rec.job_id.name != False):
                ids.append(rec.id)
                vals.append(rec.job_id.name)
                # dict[rec.unit_name_hr.name] = rec.id
        print('9999999999999999999999999999999999999')
        print(ids)
        print(vals)
        print(dict)
        data = list(set(vals))
        for val in vals:
            if (val in dict):
                dict[val] += 1
            else:
                dict[val] = 1
        print(dict)

        # vals2=[f]
        print(dict)
        return [ids, vals, dict, data]
    # def check_job_unit_position(self,unit_id,job_id):
    #     print(unit_id,'unit_id..........................')
    #     print(job_id,'jobid........................................')
    #     return [10]

    def check_job_unit_position(self,unit_val,job_val):
        print(unit_val ,'unit_val isssssssssssssssssssssssssssssssss')
        print(job_val ,'unit_val isssssssssssssssssssssssssssssssss')

        data= data = self.env['hr.employee'].search_count([('unit_name_hr.name','=',unit_val),('job_id.name','=',job_val)])
        print(data)
        return [data]
        # print(unit_id, 'unit_id..........................')
        # print(job_id, 'jobid........................................')


    def gender_count(self,gen_data):
        data=  self.env['hr.employee'].search_count([('gender','=',gen_data)])
        return [data]

    def age_count_trigger(self,age_data):
        age_list=list(map(int,age_data.split(',')))
        min,max=age_list[0],age_list[1]
        today = datetime.today()
        count=0
        data = self.env['hr.employee'].search([])
        for  rec in data:
            if(rec.birthday):
                age = today.year - rec.birthday.year - ((today.month, today.day) < (rec.birthday.month,rec.birthday.day))
                if(age>=min and age<=max):
                    count+=1


        print('count is ',count)
        return [count]
    def general_category_check(self):
        data =[rec.name for rec in self.env['general.category'].search([]) if(rec.name)]
        print('category issssssssssss',data)
        return data

    def general_category_response(self,cat_val):
        print(cat_val,'cat_val isssssssssss')

        data = self.env['hr.employee'].search_count([('emp_cat.name','=',cat_val)])
        print('genearal category response',data)
        return [data]

    def emplpoyee_type_response(self, emp_val):
        print(emp_val,'emp val is ............................')
        data = self.env['hr.employee'].search_count([('employee_type', '=', emp_val)])
        return [data]





# class HrEmployeeNew(models.Model):
#     _inherit = 'hr.employee'
#
#     age = fields.Integer("Age", compute="calculate_age",store=True)
#
