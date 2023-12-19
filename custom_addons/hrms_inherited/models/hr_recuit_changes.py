from odoo import fields,models,api


class HrRecruitChanges(models.Model):
    _inherit = 'hr.applicant'

    date_rejected = fields.Datetime("Rejected Date", compute='_compute_date_rejected', store=True, readonly=False,
                                    tracking=True)
    date_selected = fields.Datetime("Selected Date", compute='_compute_date_selected', store=True, readonly=False,
                                    tracking=True)
    reject_reason = fields.Text(string='Rejected Reason', tracking=True)

    # For Selected Ribbon
    @api.depends('stage_id.hired_stage')
    def _compute_date_selected(self):
        for applicant in self:
            if applicant.stage_id and applicant.stage_id.selected_stage and not applicant.date_selected:
                applicant.date_selected = fields.datetime.now()
            if not applicant.stage_id.selected_stage:
                applicant.date_selected = False

    #For Rejected Ribbion
    @api.depends('stage_id.hired_stage')
    def _compute_date_rejected(self):
        for applicant in self:
            if applicant.stage_id and applicant.stage_id.rejected_stage and not applicant.date_rejected:
                applicant.date_rejected = fields.datetime.now()
            if not applicant.stage_id.rejected_stage:
                applicant.date_rejected = False

    def archive_applicant(self):
        for rec in self:
            if rec.date_selected:
                rec.date_selected = False
            if rec.date_closed:
                rec.date_closed = False
            return super(HrRecruitChanges, self).archive_applicant()


class RecruitmentStageChanges(models.Model):
    _inherit = 'hr.recruitment.stage'

    rejected_stage = fields.Boolean('Rejected Stage', tracking=True)
    selected_stage = fields.Boolean('Selected Stage', tracking=True)






