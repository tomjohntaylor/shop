from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .models import ProductCategory, Product
from SaleProcess.models import Cart


def categories(request):
    product_category_list = ProductCategory.objects.filter(is_root=False)
    return render(request, 'product/categories.html', {'product_category_list': product_category_list})


def product_category(request, category_path):
    product_category = ProductCategory.objects.get(category_path=category_path)
    product_list = Product.objects.filter(product_category=product_category)
    filter_active = False
    filter_dict = product_category.create_filter_dict(request, product_list)
    filter_submited_dict = {}

    if request.GET.get('filter_active'):
        filter_active = True
        filter_submited_dict = product_category.create_filter_submited_dict(request, filter_dict)
        product_list = product_category.filter_products(filter_dict, product_list, filter_submited_dict)

    return render(request, 'product/product_category.html', {'product_category': product_category,
                                                     'product_list': product_list,
                                                     'filter_submited_dict': filter_submited_dict,
                                                     'filter_dict': filter_dict,
                                                     'filter_active': filter_active})


def product_details(request, category_path, id):
    product = get_object_or_404(Product, id=id)
    product_category = ProductCategory.objects.get(category_path=category_path)
    return render(request, 'product/product_details.html', {'product': product,
                                                            'product_category': product_category})



def add_to_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart.add_product(request.GET['product_id'], request.GET['qty'])
        cart.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        request.session['cart_json'] = {}
        request.session['cart_json'][request.GET['product_id']] = request.GET['qty']
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


