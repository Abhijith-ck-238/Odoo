/** @odoo-module */

import { patch } from "@web/core/utils/patch";
import { Orderline } from "@point_of_sale/app/store/models";
import { PosStore } from "@point_of_sale/app/store/pos_store";





patch(Orderline.prototype, {
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            owner_id: this.get_product().owner_id,
        };
    },
});

