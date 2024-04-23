/** @odoo-module */

import { PartnerDetailsEdit } from "@point_of_sale/app/screens/partner_list/partner_editor/partner_editor";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { Order } from "@point_of_sale/app/store/models";



patch(PartnerDetailsEdit.prototype, {
    setup() {
        super.setup(...arguments);
        this.intFields.push("purchase_limit");
        this.intFields.push("limit_amount");
        this.changes.limit_amount =
                this.props.partner.limit_amount;
    }
});

patch(PosStore.prototype,{
    // @Override
    async _processData(loadedData) {
        await super._processData(...arguments);
            this.limit_amount = loadedData["limit_amount"];
            },
});