
/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Orderline } from "@point_of_sale/app/store/models";
import { Order } from "@point_of_sale/app/store/models";



patch(ProductScreen.prototype, {
    clearCart() {
    var order = this.pos.get_order()
    var lines = order.orderlines;
        while(lines.length > 0){
            this.currentOrder.removeOrderline(lines[0]);
        }
        }

    });
