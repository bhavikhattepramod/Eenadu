odoo.define('dev_job_position_request.DashboardSupervisor', function (require) {
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
   var DashboardPage1 = AbstractAction.extend({
       contentTemplate : 'DashboardSupervisor',
       events: {
            'click .req_total': 'total_req',
            'click .req_new': 'sup_new',
            'click .req_submit': 'sup_submit',
            'click .req_hod': 'sup_hod',
            'click .req_fin': 'sup_fin',
            'click .req_hr': 'sup_hr',
            'click .req_approve': 'sup_approve',
            'click .req_reject': 'sup_reject',
            'click .req_fin_exempt': 'sup_fin_exempt',
        },

       init: function(parent, context) {
           this._super(parent, context);
           this.dashboard_templates = ['DashboardMain'];
       },
       start: function() {
           var self = this;
           this.set("title", 'DashboardPage1');
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
           var templates = ['DashboardMain'];
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
               $('#total_no_records').append('<span>' + result.total_records + '</span>');
               $('#total_news').append('<span>' + result.total_new + '</span>');
               $('#total_submits').append('<span>' + result.total_submit + '</span>');
               $('#total_hods').append('<span>' + result.total_hod + '</span>');
               $('#total_finances').append('<span>' + result.total_finance + '</span>');
               $('#total_hrs').append('<span>' + result.total_hr + '</span>');
               $('#total_no_approved').append('<span>' + result.total_approved + '</span>');
               $('#total_rejects').append('<span>' + result.total_reject + '</span>');
               $('#total_finance_exempts').append('<span>' + result.total_finance_exempt + '</span>');
           });
       },

       view_page: function (domain, name) {
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

       total_req : function () {
            var self = this;
            var name =  _t("Total Requisitions");
            var domain = [];
            self.view_page(domain,name);
        },
       sup_new : function () {
            var self = this;
            var name =  _t("Requisitions in New");
            var domain = [['state', '=', 'new']];
            self.view_page(domain,name);
        },

       sup_submit : function () {
            var self = this;
            var name =  _t("Requisitions Submit");
            var domain = [['state', '=', 'submit']];
            self.view_page(domain,name);
        },

       sup_hod : function () {
            var self = this;
            var name =  _t("Requisitions Approved by Hod");
            var domain = [['state', '=', 'hod_approve']];
            self.view_page(domain,name);
       },

       sup_fin : function () {
            var self = this;
            var name =  _t("Requisitions Approved by Finance");
            var domain = [['state', '=', 'finance_approve']];
            self.view_page(domain,name);
       },

       sup_hr : function () {
            var self = this;
            var name =  _t("Requisitions Approved by Hr");
            var domain = [['state', '=', 'hr_approved']];
            self.view_page(domain,name);
       },

       sup_approve: function () {
            var self = this;
            var name =  _t("Requisitions Approved");
            var domain = [['state', '=', 'approved']];
            self.view_page(domain,name);
        },

        sup_reject: function () {
            var self = this;
            var name =  _t("Requisitions Rejected");
            var domain = [['state', '=', 'rejected']];
            self.view_page(domain,name);
        },

        sup_fin_exempt : function () {
            var self = this;
            var name =  _t("Requisitions Finance Exempted");
            var domain = [['finance_exempted', '=', true]];
            self.view_page(domain,name);
        },

    });
   core.action_registry.add('recruitment_dashboard_supervisor', DashboardPage1);
   return DashboardPage1;
});