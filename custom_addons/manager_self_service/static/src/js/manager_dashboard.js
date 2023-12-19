odoo.define('manager_self_service.DashboardManager', function (require) {
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
   var DashboardPage4 = AbstractAction.extend({
       contentTemplate : 'DashboardManager',
       events: {
            'click .self_pending_manager': 'onduty_form',
            'click .self_pending_manager_leave': 'leave_form',
            'click .self_pending_manager_shift': 'shift_form',
            'click .self_pending_manager_ontour': 'ontour_form',
            'click .self_pending_manager_auth': 'auth_form',
            'click .self_pending_manager_rectification': 'rectification_form',
            'click .self_pending_manager_lta': 'lta_form',
        },

       init: function(parent, context) {
           this._super(parent, context);
           this.dashboard_templates = ['DashboardFour'];
       },
       start: function() {
           var self = this;
           this.set("title", 'DashboardPage4');
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
//           this.fetch_data_leave()
           var templates = ['DashboardFour'];
           _.each(templates, function(template) {
               self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}))
           });
       },
       fetch_data: function() {
        var self = this;
        // Define the list of models and methods you want to call
        var modelsAndMethods = [
            { model: 'self.service.application.details', method: 'displaying_data' },
            { model: 'hr.holidays.cancel', method: 'displaying_leave_data' },
            { model: 'on.tour.form', method: 'displaying_data_ontour' },
            { model: 'shift.changes.form', method: 'displaying_data_shift' },
            { model: 'authorisation.form', method: 'displaying_data_authorisation' },
            { model: 'rectification.form', method: 'displaying_data_rectification' },
            { model: 'lta.form', method: 'displaying_data_lta' },
        ];
        // Create an array to hold the promises for each RPC call
        var rpcPromises = modelsAndMethods.map(function(item) {
            return self._rpc({
                model: item.model,
                method: item.method,
            });
        });
        // Execute all RPC calls concurrently
        Promise.all(rpcPromises)
            .then(function(results) {
                results.forEach(function(result, index) {
                    var modelAndMethod = modelsAndMethods[index];
                    if (modelAndMethod.model === 'self.service.application.details') {
                        $('#total_employee_submits').append('<span>' + result.total_submit + '</span>');
                    } else if (modelAndMethod.model === 'hr.holidays.cancel') {
                        $('#total_employee_leave_submits').append('<span>' + result.total_need_approval + '</span>');
                    } else if (modelAndMethod.model === 'on.tour.form') {
                        $('#total_employee_ontour_submits').append('<span>' + result.total_submit_ontour + '</span>');
                    } else if (modelAndMethod.model === 'shift.changes.form') {
                        $('#total_employee_shift_submits').append('<span>' + result.total_submit_shift + '</span>');
                    } else if (modelAndMethod.model === 'authorisation.form') {
                        $('#total_employee_auth_submits').append('<span>' + result.total_submit_authorise + '</span>');
                    } else if (modelAndMethod.model === 'rectification.form') {
                        $('#total_employee_rectification_submits').append('<span>' + result.total_submit_rectificate + '</span>');
                    } else if (modelAndMethod.model === 'lta.form') {
                        $('#total_employee_lta_submits').append('<span>' + result.total_submit_lta + '</span>');
                    }
                });
            });
        },

       view_page: function (res_model,domain) {
        var self = this;
        self.do_action({
                name: _t("Waiting For Approval"),
                type: 'ir.actions.act_window',
                res_model: res_model,
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                domain: domain,
                target: 'current',
                context: {create: false}
            });
       },
       onduty_form : function () {
            var self = this;
            var res_model = 'self.service.application.details';
            var domain = [['status', '=', 'submitted'],['e_name.parent_id.user_id', '=', session.uid]];
            self.view_page(res_model,domain);
       },
       leave_form : function () {
            var self = this;
            var res_model = 'hr.holidays.cancel';
            var domain = [['state', '=', 'confirm'],['employee_id.parent_id.user_id', '=', session.uid]];
            self.view_page(res_model,domain);
       },
       shift_form : function () {
            var self = this;
            var res_model = 'shift.changes.form';
            var domain = [['status', '=', 'submitted'],['e_name_shift.parent_id.user_id', '=', session.uid]];
            self.view_page(res_model,domain);
       },

       ontour_form : function () {
            var self = this;
            var res_model = 'on.tour.form';
            var domain = [['status', '=', 'submitted'],['e_name_on_tour.parent_id.user_id', '=', session.uid]];
            self.view_page(res_model,domain);
       },

       auth_form : function () {
            var self = this;
            var res_model = 'authorisation.form';
            var domain = [['status', '=', 'submitted'],['e_name_auth.parent_id.user_id', '=', session.uid]];
            self.view_page(res_model,domain);
       },

       rectification_form : function () {
            var self = this;
            var res_model = 'rectification.form';
            var domain = [['status', '=', 'submitted'],['e_name_rect.parent_id.user_id', '=', session.uid]];
            self.view_page(res_model,domain);
       },

       lta_form : function () {
            var self = this;
            var res_model = 'lta.form';
            var domain = [['status', '=', 'submitted'],['e_name_lta.parent_id.user_id', '=', session.uid]];
            self.view_page(res_model,domain);
       },

    });
   core.action_registry.add('self_dashboard_manager', DashboardPage4);
   return DashboardPage4;
});