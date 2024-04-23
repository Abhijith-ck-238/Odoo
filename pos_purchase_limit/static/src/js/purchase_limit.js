
/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { _t } from "@web/core/l10n/translation";

patch(PaymentScreen.prototype, {
    async validateOrder(isForceValidate) {
        if(!this.currentOrder.get_partner()){
            this.popup.add(ErrorPopup, {
                title: _t("Where is the customer"),
                body: _t("Please Choose a customer."),
                });
        }
        else{
            var limit_amount = this.currentOrder.get_partner().limit_amount
            var purchase_limit = this.currentOrder.get_partner().purchase_limit
            var total_amount = this.currentOrder.get_total_with_tax()

        if(total_amount > limit_amount && purchase_limit){
            this.popup.add(ErrorPopup, {
                title: _t("Limit exceeded"),
                body: _t("sorry... your purchase amount limit exceeded...please remove unwanted products"),
                });
            }
            else{
                await super.validateOrder(...arguments);
            }
            }
},
});
