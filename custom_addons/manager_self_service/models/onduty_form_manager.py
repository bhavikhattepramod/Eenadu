from odoo import fields, models, api


class OnDutyManager(models.Model):
    _inherit = 'self.service.application.details'

    def approve_onduty_manager(self):
        self.status = 'approved'

    def reject_onduty_manager(self):
        self.status = 'reject'

    @api.model
    def displaying_data(self):
        total_submit = self.search([('status', '=', 'submitted'),('e_name.parent_id.user_id', '=', self.env.user.id)])
        return {
            'total_submit': len(total_submit),
        }


class LeaveCancelManager(models.Model):
    _inherit = 'hr.holidays.cancel'

    @api.model
    def displaying_leave_data(self):
        total_need_approval = self.search([('state', '=', 'confirm'),('employee_id.parent_id.user_id', '=', self.env.user.id)])
        return {
            'total_need_approval': len(total_need_approval),
        }


class OnTourManager(models.Model):
    _inherit = 'on.tour.form'

    def approve_ontour_manager(self):
        self.status = 'approved'

    def reject_ontour_manager(self):
        self.status = 'reject'

    @api.model
    def displaying_data_ontour(self):
        total_submit_ontour = self.search([('status', '=', 'submitted'), ('e_name_on_tour.parent_id.user_id', '=', self.env.user.id)])
        return {
            'total_submit_ontour': len(total_submit_ontour),
        }


class ShiftManager(models.Model):
    _inherit = 'shift.changes.form'

    def approve_shift_manager(self):
        self.status = 'approved'

    def reject_shift_manager(self):
        self.status = 'reject'

    @api.model
    def displaying_data_shift(self):
        total_submit_shift = self.search([('status', '=', 'submitted'), ('e_name_shift.parent_id.user_id', '=', self.env.user.id)])
        return {
            'total_submit_shift': len(total_submit_shift),
        }


class AuthorisationManager(models.Model):
    _inherit = 'authorisation.form'

    def approve_authorisation_manager(self):
        self.status = 'approved'

    def reject_authorisation_manager(self):
        self.status = 'reject'

    @api.model
    def displaying_data_authorisation(self):
        total_submit_authorise = self.search([('status', '=', 'submitted'), ('e_name_auth.parent_id.user_id', '=', self.env.user.id)])
        return {
            'total_submit_authorise': len(total_submit_authorise),
        }


class RectificationManager(models.Model):
    _inherit = 'rectification.form'

    def approve_rectification_manager(self):
        self.status = 'approved'

    def reject_rectification_manager(self):
        self.status = 'reject'

    @api.model
    def displaying_data_rectification(self):
        total_submit_rectificate = self.search([('status', '=', 'submitted'), ('e_name_rect.parent_id.user_id', '=', self.env.user.id)])
        return {
            'total_submit_rectificate': len(total_submit_rectificate),
        }


class LtaManager(models.Model):
    _inherit = 'lta.form'

    def approve_lta_manager(self):
        self.status = 'approved'

    def reject_lta_manager(self):
        self.status = 'reject'

    @api.model
    def displaying_data_lta(self):
        total_submit_lta = self.search([('status', '=', 'submitted'), ('e_name_lta.parent_id.user_id', '=', self.env.user.id)])
        return {
            'total_submit_lta': len(total_submit_lta),
        }