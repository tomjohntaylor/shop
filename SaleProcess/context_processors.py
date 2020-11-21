from .models import Cart
from Product.models import Product

def cart_processor(request):
    to_delete = []
    cart_data = {}
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        if cart:
            for product_id, qty in cart[0].cart_json.items():
                try:
                    cart_data[product_id] = {'product': Product.objects.get(id=product_id),
                                             'qty': qty}
                except Product.DoesNotExist:
                    to_delete.append(product_id)
            for product_id in to_delete:
                cart[0].delete_product(product_id)
            return {'cart_data': cart_data}
        else:
            return {'cart_data': None}
    else:
        if 'cart_json' in request.session.keys():
            for product_id, qty in request.session['cart_json'].items():
                try:
                    cart_data[product_id] = {'product': Product.objects.get(id=product_id),
                                             'qty': qty}
                except Product.DoesNotExist:
                    to_delete.append(product_id)
            for product_id in to_delete:
                del request.session['cart_json'][product_id]
            return {'cart_data': cart_data}
        else:
            return {'cart_data': None}
