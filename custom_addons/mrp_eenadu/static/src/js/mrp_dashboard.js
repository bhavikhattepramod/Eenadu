odoo.define('mrp_eenadu.DashboardMrpEenadu', function (require) {
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
   var MrpDashboardEenadu = AbstractAction.extend({
       contentTemplate : 'MrpDashboardEenadu',

    });
   core.action_registry.add('mrp_dashboard_eenadu', MrpDashboardEenadu);
   return MrpDashboardEenadu;
});