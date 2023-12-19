odoo.define('eenadu_classified.classifieds_dashboard', function (require){
   "use strict";
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var QWeb = core.qweb;
   var rpc = require('web.rpc');
   var ajax = require('web.ajax');
   var classified_dashboard_main = AbstractAction.extend({
      template: 'classifieds_dashboard',
   
      init: function(parent, context) {
          this._super(parent, context);
          this.dashboards_templates = ['classifieds_dashboard_data'];
      },
   
      willStart: function() {
         var self = this;
         return $.when(this._super()).then(function() {
            return self.fetch_data();
         });
      },
   
   
      start: function() {
         var self = this;
         return this._super().then(function() {
            self.render_dashboards();
         });
      },
   
      render_dashboards: function(){
         var self = this;
         _.each(this.dashboards_templates, function(template) {
            self.$('.o_classifieds_main_dashboard').append(QWeb.render(template, {widget: self}));
         });
         return self.fetchPieChartData();
      },
         fetchPieChartData: function () {
            var self = this;
            var user_id = this.getSession().uid
            var Charts = self._rpc({
               model: "classified.dashboard.data",
               method: "get_product_target_vals",
               args: [[1],user_id],
            })
            .then(function (data) {
               //Product Pie Chart
               var ctx = document.getElementById('classifier_pie_chart').getContext('2d');
               const classifier_pie_chart = new Chart(ctx, {
                  type: 'polarArea',
                  data: {
                     labels: data.period_list,
                     datasets: [
                        {
                           label: 'Received Amount',
                           data: data.received_payment,
                           borderWidth: 1,
                           backgroundColor: data.background_color1,
                           borderColor: data.border_color1
                        },
                        // {
                        //    label: 'Received Payment',
                        //    data: data.received_payment,
                        //    borderWidth: 1,
                        //    backgroundColor: data.background_color2,
                        //    borderColor: data.border_color2
                        // }
                     ]
                  },
                  options: {
                  }
               });

               //Product Bar Graph
               var ctx = document.getElementById('classifier_bar_graph').getContext('2d');
               const classifier_bar_graph = new Chart(ctx, {
                  type: 'bar',
                  data: {
                     labels: data.period_list,
                     datasets: [
                        {
                           label: 'Target Amount',
                           data: data.target_amount,
                           borderWidth: 1,
                           backgroundColor: 'rgba(54, 162, 235, 0.6)',
                           // backgroundColor: data.background_color1,
                           // borderColor: data.border_color1
                        },
                        {
                           label: 'Received Payment',
                           data: data.received_payment,
                           borderWidth: 1,
                           backgroundColor: 'rgba(255, 99, 132, 0.6)',
                           // backgroundColor: data.background_color2,
                           // borderColor: data.border_color2
                        },
                     ]
                  },
                  options: {
                  }
               });

               //Product Line Graph
               var ctx = document.getElementById('classifier_line_graph').getContext('2d');
               const classifier_line_graph = new Chart(ctx, {
                  type: 'radar',
                  data: {
                     labels: data.period_list,
                     datasets: [
                        {
                           label: 'Target Amount',
                           data: data.target_amount,
                           borderWidth: 1,
                           backgroundColor: 'rgba(54, 162, 235)',
                           borderColor: 'rgba(54, 162, 235)',
                           pointRadius:3,
                           // backgroundColor: data.background_color1,
                           // borderColor: data.border_color1,
                           fill:false,
                        },
                        {
                           label: 'Received Payment',
                           data: data.received_payment,
                           borderWidth: 1,
                           backgroundColor: 'rgba(255, 99, 132)',
                           borderColor: 'rgba(255, 99, 132)',
                           pointRadius:3,
                           // backgroundColor: data.background_color2,
                           // borderColor: data.border_color2,
                           fill:false,
                        }
                     ]
                  },
                  options: {
                  }
               });
            });
            return Charts;
         },
   
      fetch_data: function() {
         var self = this;
         var user_id = this.getSession().uid
         var def1 =  this._rpc({
               model: 'classified.dashboard.data',
               method: 'get_display_data',
               args: [[1],user_id],
      }).then(function(result){
            self.user = result['user'],
            self.cio = result['cio'],
            self.scheduling = result['scheduling'],
            self.waiting_for_approval = result['waiting_for_approval'],
            self.release_orders = result['release_orders'],
            self.invoices = result['invoices'],
            self.invoice_amount = result['invoice_amount'],
            self.invoice_due = result['invoice_due'],
            self.deposit_amt = result['deposit_amt'],
            self.outstanding_amt = result['outstanding_amt'],
            self.total_payment_received = result['total_payment_received'],
            self.total_commission_received = result['total_commission_received'],
            self.total_incentive_payment_received = result['total_incentive_payment_received'],
            self.total_incentive_amount = result['total_incentive_amount'],
            self.target_lines = result['target_lines'],
            self.so_target_lines = result['so_target_lines'],
            self.incentive_lines = result['incentive_lines']
         });
         return $.when(def1);
      },
   
   
   });
   core.action_registry.add('classified_dashboard_tags', classified_dashboard_main);
   return classified_dashboard_main;
   });
   
   $(document).ready(function(){
      $('body').delegate('.display_cio_div','click',function() {
         window.open($(".display_cio_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_scheduling_div','click',function() {
         window.open($(".display_scheduling_div").attr("test"),'_blank');
      });
      $('body').delegate('.classified_display_waiting_for_approval_div','click',function() {
         window.open($(".classified_display_waiting_for_approval_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_release_orders_div','click',function() {
         window.open($(".display_release_orders_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_invoices_div','click',function() {
         window.open($(".display_invoices_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_deposits_div','click',function() {
         window.open($(".display_deposits_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_commission_div','click',function() {
         window.open($(".display_commission_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_incentive_div','click',function() {
         window.open($(".display_incentive_div").attr("test"),'_blank');
      });
   });