odoo.define('employee_life_cycle.DashboardElc', function (require) {
   "use strict";
   var unit_res=[];
   var dept_list=[];
   var job_list=[];
   var unit_val=null;
   var job_val=null;
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var QWeb = core.qweb;
   var web_client = require('web.web_client');
   var session = require('web.session');
   var ajax = require('web.ajax');
   var _t = core._t;
   var rpc = require('web.rpc');
   var self = this;
   var DashboardSheet1 = AbstractAction.extend({
       contentTemplate : 'DashboardElc',

       events: {
            'click .elc_tran_prob': 'tran_prob_pen',
            'click .elc_prob_to_conf': 'prob_to_conf_pen',
            'click .elc_prob_ext': 'prob_ext_pen',
            'click .elc_transfers': 'transfers_pen',
            'click .elc_promotion': 'promotion_pen',
            'click .elc_increments': 'increments_pen',
            'click .elc_re_designation': 're_designation_pen',

            'click .elc_tran_prob_app': 'tran_prob_app',
            'click .elc_prob_to_conf_app': 'prob_to_conf_app',
            'click .elc_prob_ext_app': 'prob_ext_app',
            'click .elc_transfers_app': 'transfers_app',
            'click .elc_promotion_app': 'promotion_app',
            'click .elc_increments_app': 'increments_app',
            'click .elc_re_designation_app': 're_designation_app',

            'click .disp_emp_incident': 'emp_incident',
            'click .disp_emp_man_incident_pen': 'emp_man_incident_pen',
            'click .disp_emp_man_incident_close': 'emp_man_incident_close',
        },

       init: function(parent, context) {
           this._super(parent, context);
           this.dashboard_templates = ['DashboardEmployeeElc'];
           this._send_locations();
           this._send_departments();
           this._send_job_ids();
           this._check_job_unit_position();
           this._create_general_selection();

       },
       start: function() {
           var self = this;
           this.set("title", 'DashboardSheet1');
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
           var templates = ['DashboardEmployeeElc'];
           _.each(templates, function(template) {
               self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}))
           });
       },
       fetch_data: function() {
           var self = this
//          fetch data to the tiles
           var def1 = this._rpc({
               model: 'employee.life.cycle',
               method: "get_data",
           })
           .then(function (result) {
               $('#initial_no_tran_prob').append('<span>' + result.total_tran_prob + '</span>');
               $('#initial_no_prob_to_conf').append('<span>' + result.total_prob_to_conf + '</span>');
               $('#initial_no_prob_ext').append('<span>' + result.total_prob_ext + '</span>');
               $('#initial_no_transfers').append('<span>' + result.total_transfers + '</span>');
               $('#initial_no_promotion').append('<span>' + result.total_promotion + '</span>');
               $('#initial_no_increments').append('<span>' + result.total_increments + '</span>');
               $('#initial_no_re_designation').append('<span>' + result.total_re_designation + '</span>');

               $('#final_no_tran_prob').append('<span>' + result.final_tran_prob + '</span>');
               $('#final_no_prob_to_conf').append('<span>' + result.final_prob_to_conf + '</span>');
               $('#final_no_prob_ext').append('<span>' + result.final_prob_ext + '</span>');
               $('#final_no_transfers').append('<span>' + result.final_transfers + '</span>');
               $('#final_no_promotion').append('<span>' + result.final_promotion + '</span>');
               $('#final_no_increments').append('<span>' + result.final_increments + '</span>');
               $('#final_no_re_designation').append('<span>' + result.final_re_designation + '</span>');

               $('#total_no_tran_prob').append('<span>' + (result.total_tran_prob + result.final_tran_prob)+ '</span>');
               $('#total_no_prob_to_conf').append('<span>' +( result.total_prob_to_conf + result.final_prob_to_conf )+ '</span>');
               $('#total_no_prob_ext').append('<span>' + (result.total_prob_ext + result.final_prob_ext )+ '</span>');
               $('#total_no_transfers').append('<span>' + (result.total_transfers + result.final_transfers ) + '</span>');
               $('#total_no_promotion').append('<span>' + (result.total_promotion + result.final_promotion )+ '</span>');
               $('#total_no_increments').append('<span>' + (result.total_increments + result.final_increments )+ '</span>');
               $('#total_no_re_designation').append('<span>' + (result.total_re_designation + result.final_re_designation )+'</span>');

               $('#total_no_incident').append('<span>' + result.total_incident+'</span>');
               $('#total_no_incident_progress').append('<span>' + result.total_incident_progress+'</span>');
               $('#total_no_incident_approved').append('<span>' + result.total_incident_approved+'</span>');
           });
       },

       view_page: function (domain,name) {
        var self = this;
        self.do_action({
                name: name,
                type: 'ir.actions.act_window',
                res_model: 'employee.life.cycle',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                domain: domain,
                target: 'current'
            });
       },

       view_sheet: function (domain,name) {
        var self = this;
        self.do_action({
                name: name,
                type: 'ir.actions.act_window',
                res_model: 'employee.disciplinary',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                domain: domain,
                target: 'current'
            });
       },

       view_sheet1: function (domain,name) {
        var self = this;
        self.do_action({
                name: name,
                type: 'ir.actions.act_window',
                res_model: 'manage.incident',
                view_mode: 'tree,form',
                views: [[false, 'list'], [false, 'form']],
                domain: domain,
                target: 'current'
            });
       },

        emp_incident : function () {
            var self = this;
            var name =  _t("Number Incidents");
            var domain = [];
            self.view_sheet1(domain,name);
        },

        emp_man_incident_pen : function () {
            var self = this;
            var name =  _t("Incidents In pending");
            var domain = [['state', '=', 'in_progress']];
            self.view_sheet1(domain,name);
        },

        emp_man_incident_close : function () {
            var self = this;
            var name =  _t("Incidents In Closed");
            var domain = [['state', '=', 'closed']];
            self.view_sheet1(domain,name);
        },

       tran_prob_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','tran_prob']];
            self.view_page(domain,name);
        },

        prob_to_conf_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','prob_to_conf']];
            self.view_page(domain,name);
        },

        prob_ext_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','prob_ext']];
            self.view_page(domain,name);
        },

        transfers_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','transfers']];
            self.view_page(domain,name);
        },

        promotion_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','promotion']];
            self.view_page(domain,name);
        },

        increments_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','increments']];
            self.view_page(domain,name);
        },

        re_designation_pen : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['new', 'submit', 'hr', 'hod'] ],['process','=','re_designation']];
            self.view_page(domain,name);
        },

        tran_prob_app : function () {
            var self = this;
            var name =  _t("New ELC");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','tran_prob']];
            self.view_page(domain,name);
        },

        prob_to_conf_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','prob_to_conf']];
            self.view_page(domain,name);
        },

        prob_ext_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','prob_ext']];
            self.view_page(domain,name);
        },

        transfers_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','transfers']];
            self.view_page(domain,name);
        },

        promotion_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','promotion']];
            self.view_page(domain,name);
        },

        increments_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','increments']];
            self.view_page(domain,name);
        },

        re_designation_app : function () {
            var self = this;
            var name =  _t("ELC Approved");
            var domain = [['state', 'in', ['approved', 'post'] ],['process','=','re_designation']];
            self.view_page(domain,name);
        },

        _send_locations : function (){
          rpc.query({
            model: 'emp.loyee',
            method: 'send_loactions',
            args: [[]],
            kwargs: {

            },
            }).then(result=>{
          unit_val=null;
           var ids=result[0]
           var datas=result[3]
           console.log(ids)
           console.log(datas)
unit_res=result;
             const newSelect = document.createElement('select');
               newSelect.id='select_one';
               const optionElement = document.createElement('option');
      optionElement.textContent = 'Select Unit';
      newSelect.appendChild(optionElement);
//             newSelect.style.overflowY = 'scroll';
             for (const data of datas) {
      const optionElement = document.createElement('option');
      optionElement.textContent = data;
      newSelect.appendChild(optionElement);
      const parentElement = document.getElementById('select_option');
    parentElement.appendChild(newSelect);
    $('#unit_count').text(0);
      var res= newSelect.addEventListener('change', this._checkData);
      var res= newSelect.addEventListener('change', this._check_job_unit_position);
//      alert('checking modify'+res);
//       this._checkData();
         $('#gender_count').text(0);
         $('#age_count').text(0);
         $('#emp_count').text(0);
         document.getElementById('select_gender').addEventListener('change',this._select_option_triggrer);
         document.getElementById('select_age').addEventListener('change',this._select_age_triggrer);
         document.getElementById('employment_type').addEventListener('change',this._select_employee_type);

    }




    // Step 4: Append the new select element to its parent



            });




        },
//_checkData:function(){
//alert('3456789');}

        _checkData:function(){
        var self = this;

        var selres=document.getElementById('select_one').value;
        if(selres!='Select Unit'){
//        var val=unit_res[2][selres];
//        alert(selres);
          $('#unit_count').text(unit_res[2][selres]);
          unit_val=unit_res[2][selres];
          }
          else{
            $('#unit_count').text(0);
          }

//         rpc.query({
//            model: 'emp.loyee',
//            method: 'browse_record',
//            args: [this,selres],
//            kwargs: {
//
//            },
//            }).then(result=>{
//
//
//            });

},

_send_departments:function(){
rpc.query({
            model: 'emp.loyee',
            method: 'send_departments',
            args: [[]],
            kwargs: {

            },
            }).then(result=>{
           var ids=result[0]
           var datas=result[3]
//           console.log(ids)
//           console.log(datas)
dept_list=result;
//alert(dept_list);
             const newSelect = document.createElement('select');
               newSelect.id='select_two';
               const optionElement = document.createElement('option');
      optionElement.textContent = 'Select Department';
      newSelect.appendChild(optionElement);
//             newSelect.style.overflowY = 'scroll';
             for (const data of datas) {
      const optionElement = document.createElement('option');
      optionElement.textContent = data;
      newSelect.appendChild(optionElement);
      const parentElement = document.getElementById('select_option2');
    parentElement.appendChild(newSelect);
     $('#dept_count').text(0);
       newSelect.addEventListener('change', this._check_department);
//       this._checkData();
//
    }


    });




    // Step 4: Append the new select element to its parent




},

    _check_department:function(){
        var self = this;
        job_val=null;

        var selres=document.getElementById('select_two').value;
//        alert(selres);
         if(selres!='Select Department'){
        var val=dept_list[2][selres];
//        alert(val);
//        alert(selres);
          $('#dept_count').text(val);
          }
          else{
           $('#dept_count').text(0);
          }
//         rpc.query({
//            model: 'emp.loyee',
//            method: 'browse_record',
//            args: [this,selres],
//            kwargs: {
//
//            },
//            }).then(result=>{
//
//
//            });

},


//third



_send_job_ids:function(){
rpc.query({
            model: 'emp.loyee',
            method: 'send_jobs',
            args: [[]],
            kwargs: {

            },
            }).then(result=>{
           var ids=result[0]
           var datas=result[3]
//           console.log(ids)
//           console.log(datas)
job_list=result;
             const newSelect = document.createElement('select');
               newSelect.id='select_three';
//             newSelect.style.overflowY = 'scroll';
$('#unit_job_count').text(0);
 const optionElement = document.createElement('option');
      optionElement.textContent = 'Select Job';
      newSelect.appendChild(optionElement);
      for (const data of datas) {
      const optionElement = document.createElement('option');
      optionElement.textContent = data;
      newSelect.appendChild(optionElement);
      const parentElement = document.getElementById('select_option3');
    parentElement.appendChild(newSelect);
    $('#job_count').text(0);
       newSelect.addEventListener('change', this._check_job);
       newSelect.addEventListener('change', this._check_job_unit_position);
//       this._checkData();
//
    }


    });




    // Step 4: Append the new select element to its parent




},

    _check_job:function(){
        var self = this;

        var selres=document.getElementById('select_three').value;
//        alert(selres)
        if(selres!='Select Job'){
        var val=job_list[2][selres];
//        alert(selres);
          $('#job_count').text(val);
          job_val=job_list[2][selres];
          }
          else{
          $('#job_count').text(0);
          }
//         rpc.query({
//            model: 'emp.loyee',
//            method: 'browse_record',
//            args: [this,selres],
//            kwargs: {
//
//            },
//            }).then(result=>{
////
////
////            });
//
},


_check_job_unit_position:function(){
 var self=this;
// alert('aaaaaaaaaaaaaaa');
if(job_val!=null && unit_val!=null){

rpc.query({
            model: 'emp.loyee',
            method: 'check_job_unit_position',
//                args: [[]],
            args: [this,document.getElementById('select_one').value,document.getElementById('select_three').value],
            kwargs: {

            },
            }).then(result=>{
                 $('#unit_job_count').text(result[0]);

            });
            }

},


_select_option_triggrer:function(){


if(document.getElementById('select_gender').value==='select'){
 $('#gender_count').text(0);
}
else{
rpc.query({
            model: 'emp.loyee',
            method: 'gender_count',
//                args: [[]],
            args: [this,document.getElementById('select_gender').value],
            kwargs: {

            },
            }).then(result=>{
                $('#gender_count').text(result[0]);
            });
            }

},

_select_age_triggrer:function(){


if(document.getElementById('select_age').value==='select'){
 $('#age_count').text(0);
}
else{
rpc.query({
            model: 'emp.loyee',
            method: 'age_count_trigger',
//                args: [[]],
            args: [this,document.getElementById('select_age').value],
            kwargs: {

            },
            }).then(result=>{
                $('#age_count').text(result[0]);
            });




            }

},

_create_general_selection:function(){

rpc.query({
            model: 'emp.loyee',
            method: 'general_category_check',
//                args: [[]],
            args: [[]],
            kwargs: {

            },
            }).then(result=>{

             const newSelect = document.createElement('select');
               newSelect.id='select_general';
               const optionElement = document.createElement('option');
      optionElement.textContent = 'Select Category';
      newSelect.appendChild(optionElement);
//             newSelect.style.overflowY = 'scroll';
             for (const data of result) {
      const optionElement = document.createElement('option');
      optionElement.textContent = data;
      newSelect.appendChild(optionElement);
      const parentElement = document.getElementById('select_general_cat');
    parentElement.appendChild(newSelect);

    }
     $('#cat_count').text(0);
    newSelect.addEventListener('change', this._check_general_cat);

            });

},

_check_general_cat:function(){
if(document.getElementById('select_general').value==='Select Category'){

             $('#cat_count').text(0);
            }
            else{
            rpc.query({
            model: 'emp.loyee',
            method: 'general_category_response',
//                args: [[]],
            args: [this,document.getElementById('select_general').value],
            kwargs: {

            },
            }).then(result=>{
                $('#cat_count').text(result[0]);
            });

            }


},


_select_employee_type:function(){

if(document.getElementById('employment_type').value==="select"){
  $('#emp_count').text(0);
            }
            else{

             rpc.query({
            model: 'emp.loyee',
            method: 'emplpoyee_type_response',
//                args: [[]],
            args: [this,document.getElementById('employment_type').value],
            kwargs: {

            },
            }).then(result=>{
                $('#emp_count').text(result[0]);
            });

            }


},


//ending function
    });
   core.action_registry.add('employee_dashboard_elc', DashboardSheet1);
   return DashboardSheet1;
});