odoo.define('custom_inventory.DashboardInventoryEenadu', function (require) {
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
   var InventoryDashboardEenadu = AbstractAction.extend({
       contentTemplate : 'InventoryDashboardEenadu',

    });
   core.action_registry.add('inventory_dashboard_eenadu', InventoryDashboardEenadu);
   return InventoryDashboardEenadu;
});