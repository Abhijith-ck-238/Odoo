/** @odoo-module **/


import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useRef } from "@odoo/owl";
import { onMounted } from "@odoo/owl";




class RangeSliderWidgets extends Component {
//class to set values to the widget
    static template = "rangeslider.RangeSliderWidget";


    setup(){
        super.setup();
        this.inputSlider = useRef("inputSlider");
        this.sliderValue = useRef("sliderValue");

        useInputField({ getValue: () => this.props.record.data[this.props.name] || "", refName: "inputSlider" });
        this.value = this.props.record.data[this.props.name]
        onMounted(this._mounted);
    }

    _mounted(){
//    each time component is attached to DOM, the mounted is called
        this.inputSlider.el.value = this.value
        this.sliderValue.el.value = this.value

    }

    _sliderinput(){
        this.sliderValue.el.value = this.inputSlider.el.value
    }

}
export const rangeSliderWidgets = {
component: RangeSliderWidgets,
    displayName: _t("slider"),
    supportedTypes: ["integer"]
};
registry.category("fields").add('range_slider',rangeSliderWidgets);
