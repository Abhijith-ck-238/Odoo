/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { Order } from "@point_of_sale/app/store/models";



patch(Orderline.prototype, {
    setup() {
        this.pos = usePos();
    },
    async _RemoveLine(){
        var order_line_product_name = this.props.line.productName;
        var lines = this.pos.get_order().orderlines;
        for(var i in lines){
            if (lines[i].full_product_name === order_line_product_name){
                    this.pos.get_order().removeOrderline(lines[i]);
            }
        }
    }

});

