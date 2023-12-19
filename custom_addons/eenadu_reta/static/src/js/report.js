odoo.define('eenadu_reta.AdsReport', function (require){
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var ajax = require("web.ajax");
    var QWeb = core.qweb;
    const _t = core._t;

    var ClassfiedReportJS = AbstractAction.extend({
        template: 'classified_ads_report',
        });

    core.action_registry.add('ads_report_tag', ClassfiedReportJS);
    return ClassfiedReportJS;
});