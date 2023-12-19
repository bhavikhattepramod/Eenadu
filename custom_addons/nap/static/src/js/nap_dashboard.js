odoo.define('nap.DashboardNapEenadu', function (require) {
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
   var NapDashboardEenadu = AbstractAction.extend({
       contentTemplate : 'NapDashboardEenadu',

    });
   core.action_registry.add('nap_dashboard_eenadu', NapDashboardEenadu);
   return NapDashboardEenadu;
});