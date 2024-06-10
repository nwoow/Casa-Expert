from product.models import Product

def product_in_cart(request):
    cart = request.session.get('cart') 
    product = []
    totalamount = 0
    if cart:    
        for k in cart:
            try:
                queryset =Product.objects.get(uid=k)
                queryset.quantity = cart[k]
                if queryset.quantity:
                    totalprice = queryset.dis_price*int(queryset.quantity)
                    totalamount = totalamount + (queryset.dis_price*int(queryset.quantity))
                    queryset.totalprice = totalprice
                    product.append(queryset)
                else:
                    pass
            except Product.DoesNotExist:
                pass           
    return {'product_in_cart':product,'totalamount':totalamount,'cart_count':len(product)}



def contact_context(request):
    contact_message = {}
    return {'contact_message':contact_message}
