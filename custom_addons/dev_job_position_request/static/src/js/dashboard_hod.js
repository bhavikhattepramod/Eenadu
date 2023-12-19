odoo.define('dev_job_position_request.DashboardHod', function (require) {
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
   var DashboardPage2 = AbstractAction.extend({
       contentTemplate : 'DashboardHod',

       events: {
            'click .req_pending_hod': 'pending_hod',
            'click .req_hod_approve': 'hod_approves',
            'click .req_hod_reject': 'hod_rejects',
        },

       init: function(parent, context) {
           this._super(parent, context);
           this.dashboard_templates = ['DashboardSecond'];
       },
       start: function() {
           var self = this;
           this.set("title", 'DashboardPage2');
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
           var templates = ['DashboardSecond'];
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
               $('#total_hod_submits').append('<span>' + result.total_submit + '</span>');
               $('#total_no_hod_approved').append('<span>' + result.total_approved + '</span>');
               $('#total_hod_rejects').append('<span>' + result.total_reject + '</span>');
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

        pending_hod : function () {
            var self = this;
            var name =  _t("Requisitions Waiting For Approval");
            var domain = [['state', '=', 'submit']];
            self.view_page(domain,name);
        },

       hod_approves: function () {
            var self = this;
            var name =  _t("Requisitions Approved");
            var domain = [['state', '=', 'approved']];
            self.view_page(domain,name);
        },

        hod_rejects: function () {
            var self = this;
            var name =  _t("Requisitions Rejected");
            var domain = [['state', '=', 'rejected']];
            self.view_page(domain,name);
        },

    });
   core.action_registry.add('recruitment_dashboard_hod', DashboardPage2);
   return DashboardPage2;
});