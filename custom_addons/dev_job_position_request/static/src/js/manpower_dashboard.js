odoo.define('dev_job_position_request.ManpowerDashboard',function (require){
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core')
var Qweb = core.qweb;

var ManpowerDashboard = AbstractAction.extend({
    template : 'Dashboard',


    init: function(parent,context){
        this._super(parent,context);
        this.dashboards_template = ['DashboardOrders'];
    },

    start: function() {
        var self = this;
        this.set("title",'Dashboard');
        return this._super().then(function() {
            self.render_dashboards();
        });

    },

    render_dashboards: function() {
        var self = this;
        _.each(this.dashboards_template), function(template) {
            self.$('.o_pos_dashboard').append(Qweb.render(template,{widget: self}));
        });
    },


})
core.action_registry.add('custom_dashboard_tag',ManpowerDashboard);

return ManpowerDashboard;

});
















































//import { useService } from "@web/core/utils/hooks";
//
//const { Component, onWillStart } = owl;
//
//export class ManpowerDashboard extends Component {
//    setup() {
//        this.orm = useService("orm");
//        this.action = useService("action");
//
//        onWillStart(async () => {
//            this.manpowerData = await this.orm.call(
//                "job.position.request",
//                "retrieve_dashboard",
//            );
//        });
//    }
//
//    /**
//     * This method clears the current search query and activates
//     * the filters found in `filter_name` attibute from button pressed
//     */
//    setSearchContext(ev) {
//        let filter_name = ev.currentTarget.getAttribute("filter_name");
//        let filters = filter_name.split(',');
//        let searchItems = this.env.searchModel.getSearchItems((item) => filters.includes(item.name));
//        this.env.searchModel.query = [];
//        for (const item of searchItems){
//            this.env.searchModel.toggleSearchItem(item.id);
//        }
//    }
//}
//
//ManpowerDashboard.template = 'dev_job_position_request.ManpowerDashboard'