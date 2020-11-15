from .models import Cart
from Product.models import Product

def cart_processor(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        if cart:
            cart_data = {}
            for product_id, qty in cart[0].cart_json.items():
                cart_data[product_id] = {'product': Product.objects.get(id=product_id),
                                         'qty': qty}
            print(cart_data)
            return {'cart_data': cart_data}
        else:
            return {'cart_data': None}
    else:
        if 'cart_json' in request.session.keys():
            cart_data = {}
            for product_id, qty in request.session.items():
                cart_data[product_id] = {'product': Product.objects.get(id=product_id),
                                         'qty': qty}
            return {'cart_data': cart_data}
        else:
            return {'cart_data': None}
