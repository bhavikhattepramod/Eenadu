from odoo import fields, models


class PurchaseOrderLine(models.TransientModel):
    _name = 'physical.fitness'

    name = fields.Many2one('hr.employee', string="Name")

    def invoice_print(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('physical_report.report_hrms_wizards').report_action(self, data=data)



class PurchaseOrderLine(models.TransientModel):
    _name = 'joining.report'

    name = fields.Many2one('hr.employee', string="Name")

    def invoice_print(self):
        data = {
            # 'model': 'purchase.invoice.wizard',
            # 'form': self.read()[0]
        }
        return self.env.ref('physical_report.report_joining_wizards').report_action(self, data=data)


