odoo.define('dev_job_position_request.DashboardFinance', function (require) {
   "use strict";
    var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var QWeb = core.qweb;
   var web_client = require('web.web_client');
   var session = require('web.session');
   var ajax = require('web.ajax');
   var _t = core._t;
   var rpc = require('web.rpc');
   var self = this;
   var DashboardPage3 = AbstractAction.extend({
       contentTemplate : 'DashboardFinance',
       events: {
            'click .req_pending_fin': 'pending_fin',
            'click .req_approve': 'approves',
            'click .req_reject': 'rejects',
            'click .req_fin_exempt': 'fin_exempt',
        },

       init: function(parent, context) {
           this._super(parent, context);
           this.dashboard_templates = ['DashboardThird'];
       },
       start: function() {
           var self = this;
           this.set("title", 'DashboardPage3');
           return this._super().then(function() {
               self.render_dashboards();
           });
       },
       willStart: function(){
           var self = this;
           return this._super()
       },
       render_dashboards: function() {
           var self = this;
           this.fetch_data()
           var templates = []
           var templates = ['DashboardThird'];
           _.each(templates, function(template) {
               self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}))
           });
       },
       fetch_data: function() {
           var self = this
//          fetch data to the tiles
           var def1 = this._rpc({
               model: 'job.position.request',
               method: "get_data",
           })
           .then(function (result) {
               $('#total_finance_submits').append('<span>' + result.total_submit + '</span>');
               $('#total_no_finance_approved').append('<span>' + result.total_approved + '</span>');
               $('#total_finance_rejects').append('<span>' + result.total_reject + '</span>');
               $('#total_finance_exempted').append('<span>' + result.total_finance_exempt + '</span>');
           });
       },

       view_page: function (domain,name) {
        var self = this;
        self.do_action({
                name: name,
                type: 'ir.actions.act_window',
                res_model: 'job.position.request',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                domain: domain,
                target: 'current'
            });
       },

       fin_exempt : function () {
            var self = this;
            var name =  _t("Requisitions Finance Exempted");
            var domain = [['finance_exempted', '=', true]];
            self.view_page(domain,name);
        },

        pending_fin : function () {
            var self = this;
            var name =  _t("Waiting For Approval");
            var domain = [['state', '=', 'hod_approve']];
            self.view_page(domain,name);
        },

       approves: function () {
            var self = this;
            var name =  _t("Requisitions Approved");
            var domain = [['state', '=', 'approved']];
//            ev.stopPropagation();
//            ev.preventDefault();
            self.view_page(domain,name);
        },

        rejects: function () {
            var self = this;
            var name =  _t("Requisitions Rejected");
            var domain = [['state', '=', 'rejected']];
            self.view_page(domain,name);
        },
    });
   core.action_registry.add('recruitment_dashboard_finance', DashboardPage3);
   return DashboardPage3;
});