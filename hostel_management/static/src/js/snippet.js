/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";

publicWidget.registry.Rooms = publicWidget.Widget.extend({
    selector: '.dynamic_room_snippet',
    start: function(){
        var self = this;

        jsonrpc('/dynamic_rooms').then(function(data){
            data[0].is_active = true
            self.$el.find('#crsl').html(renderToElement('hostel_management.website_room_dynamic',{data:data}));
        });
    },
});

publicWidget.registry.websiteCartDelete = publicWidget.Widget.extend({
    selector: '.clear_cart_div',
    events: {
        'click .js_clear_cart': '_onClickClearCart'
    },

    _onClickClearCart:function(ev) {
        jsonrpc('/shop/cart/clear_cart').then(function(){
        location.reload(true);
        });

    },
});







