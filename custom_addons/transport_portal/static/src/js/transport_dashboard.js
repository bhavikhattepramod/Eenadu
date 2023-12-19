odoo.define('transport_portal.TransportDashboardEenadu', function (require) {
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
   var TransportDashboardEenadu = AbstractAction.extend({
       contentTemplate : 'TransportDashboardEenadu',

    });
   core.action_registry.add('transport_dashboard_eenadu', TransportDashboardEenadu);
   return TransportDashboardEenadu;
});