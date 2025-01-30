from django.shortcuts import render,redirect
from cart.models import Cart, CartItem
from store.models import Product


# Create your views here.
def add_to_cart(request,product_id):
    try:
        cart, _ = Cart.objects.get_or_create(user=request.user)

        product = Product.objects.get(id=product_id)
        print(product)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += 1
        else:
            if product.product_stock < 1:
                return {"error":"No enough stock available"}
            
        cart_item.save()

    except Product.DoesNotExist:
        return {"error":"Product does not exist"}
    return redirect('cart')

def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    
    for item in cart_items:
        item.total_price = item.product.product_price * item.quantity
    
    grand_total = sum(item.total_price for item in cart_items) if cart_items else 0

    context = {
        'cart_items': cart_items,
        'total_price': sum(item.total_price for item in cart_items) if cart_items else 0,
        'grand_total': grand_total,
    }

    return render(request, 'cart.html', context)


def update_cart(requsest,type,product_id):
    if type == "plus":
        cart = Cart.objects.get(user=requsest.user)
        cart_item = CartItem.objects.get(cart=cart,product_id=product_id)
        cart_item.quantity += 1
        cart_item.save()
        return redirect('cart')
        
    elif type == 'minus':
        cart = Cart.objects.get(user=requsest.user)
        cart_item = CartItem.objects.get(cart=cart,product_id=product_id)
        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
        return redirect('cart')
    

def remove_from_cart(request, product_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()

    except CartItem.DoesNotExist:
        return redirect('cart')

    return redirect('cart')