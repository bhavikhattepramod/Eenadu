odoo.define('eenadu_classified.mgmt_dashboard', function (require){
   "use strict";
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var QWeb = core.qweb;
   var rpc = require('web.rpc');
   var ajax = require('web.ajax');
   var reta_dashboard_main = AbstractAction.extend({
      template: 'mgmt_dashboard',
   
      init: function(parent, context) {
          this._super(parent, context);
          this.dashboards_templates = ['mgmt_dashboard_data'];
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
            self.$('.o_mgmt_main_dashboard').append(QWeb.render(template, {widget: self}));
         });
         return self.fetchPieChartData();
      },

         fetchPieChartData: function () {
            var self = this;
            var user_id = this.getSession().uid
            var Charts = self._rpc({
               model: "classified.management.dashboard.data",
               method: "get_management_product_values",
               args: [[1],user_id],
            })
            .then(function (data) {
               //Product Pie Chart
               var ctx = document.getElementById('reta_mgmt_pie_chart').getContext('2d');
               const reta_pie_chart = new Chart(ctx, {
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
               var ctx = document.getElementById('reta_mgmt_bar_graph').getContext('2d');
               const reta_bar_graph = new Chart(ctx, {
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
               var ctx = document.getElementById('reta_mgmt_line_graph').getContext('2d');
               const reta_line_graph = new Chart(ctx, {
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
               model: 'classified.management.dashboard.data',
               method: 'get_display_data',
               args: [[1],user_id],
      }).then(function(result){
            self.issued_cio = result['issued_cio'],
            self.total_value_cio = result['total_value_cio'],
            self.received_ro = result['received_ro'],
            self.total_value_ro = result['total_value_ro'],
            self.pending_payment = result['pending_payment'],
            self.payment_collected = result['payment_collected'],
            self.cash = result['cash'],
            self.upi_qr = result['upi_qr'],
            self.bank_neft = result['bank_neft'],
            self.pdc = result['pdc'],
            self.unit_target_incentive_lines = result['unit_target_incentive_lines'],
            self.unit_top_cio_lines = result['unit_top_cio_lines'],
            self.unit_top_cio_lines_least = result['unit_top_cio_lines_least']
        });
        return $.when(def1);
    },
   
   
   });
   core.action_registry.add('classified_management_dashboard_tags', reta_dashboard_main);
   return reta_dashboard_main;
   });
   
   $(document).ready(function(){
      $('body').delegate('.display_cio_div','click',function() {
         window.open($(".display_cio_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_release_orders_div','click',function() {
         window.open($(".display_release_orders_div").attr("test"),'_blank');
      });
      $('body').delegate('.display_payment_collections_div','click',function() {
         window.open($(".display_payment_collections_div").attr("test"),'_blank');
      });
   });
//function showDateTime() {
//var myDiv = document.getElementById("myDiv");

//  var date = new Date();
//  var dayList = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
//  var monthNames = [
//    "January",
//    "February",
//    "March",
//    "April",
//    "May",
//    "June",
//    "July",
//    "August",
//    "September",
//    "October",
//    "November",
//    "December"
//  ];
//  var dayName = dayList[date.getDay()];
//  var monthName = monthNames[date.getMonth()];
//  var today = `${dayName}, ${monthName} ${date.getDate()}, ${date.getFullYear()}`;
//
//  var hour = date.getHours();
//  var min = date.getMinutes();
//  var sec = date.getSeconds();
//
//  var time = hour + ":" + min + ":" + sec;
//  myDiv.innerText = ` ${today}.  ${time}`;
//}
//setInterval(showDateTime, 1000);