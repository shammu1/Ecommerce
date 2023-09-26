
$(document).ready(function(){
    
    $('.update-cart').click(function(e){
        e.stopImmediatePropagation();
        console.log("entering javascript 1")
        let product_id = $(this).attr("data-product")
        let action = $(this).attr("data-action")
        let price_pq = parseFloat($(this).attr("data-price")).toFixed(2)
        let cart_price = $(this).attr("data-cart-price")

        let quantity = $(".product-qty-"+product_id).val()
    
        if (action == "add"){
            quantity = Number(quantity) + 1;
        }
        if (quantity > 0){
            quantity = Number(quantity) - 1;
        }   
        
        let total_price = '$' + parseFloat(quantity * price_pq).toFixed(2);
    
        console.log("totalprice=",total_price)
        console.log("cart price=",document.querySelector('.sub-total').innerText)
        console.log(document.querySelector('.product-totalprice-'+product_id).innerText)
        document.querySelector('.product-qty-'+product_id).value = quantity;
        document.querySelector('.product-totalprice-'+product_id).innerText = total_price;
        //cart_price = parseFloat(cart_price) + parseFloat(price_pq);
        
        
    
        $.ajax({
            url: '/cart/update-cart/',
            data: {
                "id": product_id,
                "action": action,
                "quantity": quantity,
            },
            dataType: "json",
            success: function(response){
                console.log('success')
                //
                var cart_price = JSON.parse(response["total_cart_price"]);
                console.log(cart_price);
                document.querySelector('.sub-total').innerText = "$" + parseFloat(cart_price).toFixed(2);
                document.querySelector('.grand-total').innerText = "$" + parseFloat(cart_price).toFixed(2);
            }
        })
    });
//    $('.update-cart').trigger('click');

    // Shipping address show hide
    $('#shipto').change(function () {
    console.log("clicked")
    if($(this).is(':checked')) {
        $('.shipping-address').slideDown();
    } else {
        $('.shipping-address').slideUp();
    }
    });  


 /*   $('.make-default').click(function(e){
        e.stopImmediatePropagation();
        console.log("entering make default")
        let addr_id = $(this).attr("data-address")
        let address_type = $(this).attr("data-type")      
    
        $.ajax({
            url: '/user/make-default-address/',
            data: {
                "addr_id": addr_id,
                "address_type": address_type,
            },
            dataType: "json",
            success: function(response){
                console.log('success')
            }
        })
        console.log("finishing")
    });   */

    // Sorting Products
    $('#sort-list').change(function () {
        console.log("sort changed")
        $.ajax({
            url: '/products/sort/',
            data: {
                "sort-name": $(this).value,
            },
            dataType: "json",
            success: function(response){
                console.log('success')
            }
        })

    });  
    
    $('.update-prod-qty').click(function(e){
        e.stopImmediatePropagation();
        let action = $(this).attr("data-action")
        let quantity = document.querySelector('.product-qty').value
        
    
        if (action == "add"){
            quantity = Number(quantity) + 1;
        }
        else{
            if (quantity > 0){
                quantity = Number(quantity) - 1;
            }       
        }
        
        
        document.querySelector('.product-qty').value = quantity;
            
    }); 
    
    $('.add-to-cart').click(function(e){
        e.stopImmediatePropagation();
        console.log('entering add to cart')
        let quantity = document.querySelector('.product-qty').value
        let product_id = $(this).attr("data-product")
        console.log(quantity)
        console.log(product_id)
       

        $.ajax({
            url: '/cart/add/'+product_id+'/',
            data: {
                "quantity": quantity,
            },
            dataType: "json",
            success: function(response){
                window.location.href = '/cart/'
                console.log('success')
            }
        })

            
    });  
    
});

