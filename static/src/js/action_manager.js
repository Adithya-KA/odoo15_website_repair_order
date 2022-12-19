odoo.define('website_repair_order.online_repair_request',function(require){
    "use strict";

    var ajax = require('web.ajax');
    $(function(){
        $('#partner_id').on('change',function(e){
            e.preventDefault();
            var customer_name = $("select[name ='partner_id']").val();
            ajax.rpc('/repair_order/product',{customer_name}).then(function(response){
                $('#product_id').empty();
                response['product_id'].forEach(element =>{
                    $('#product_id').html($('#product_id').html()+ `<option value=${element[0]}>${element[1]}</option>`)
                    console.log(element[0], element[1])
                });
            });
        });
    });
});
