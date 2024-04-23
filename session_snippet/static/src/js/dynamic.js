/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToElement } from "@web/core/utils/render";
publicWidget.registry.DynamicSnippets = publicWidget.Widget.extend({
    selector:'js-dynamic_snippet',
    start:function(){
    jsonrpc('/get_total_sold').then((res)=>{
    if(res){
    res.$el.find('#prod_snip').html(renderToElement('session_snippet.dynamic_snippet_custom',{data:data}));
    }
    });
    return this._super.apply(this, arguments)
    }
});