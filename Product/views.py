from django.shortcuts import render, get_object_or_404

from .models import ProductCategory, Product


def categories(request):
    product_category_list = ProductCategory.objects.filter(is_root=False)
    return render(request, 'categories.html', {'product_category_list': product_category_list})


def product_category(request, category_path):
    product_category = ProductCategory.objects.get(category_path=category_path)
    filters_dict = {}
    filter_submited_dict = {}
    product_list = Product.objects.filter(product_category=product_category)

    for k,v in product_category.attributes_json.items():
        filter_submited_dict[k] = {}
        if request.GET.get(k+'_min'):
            filter_submited_dict[k]['_min'] = request.GET.get(k+'_min')
        if request.GET.get(k+'_max'):
            filter_submited_dict[k]['_max'] = request.GET.get(k+'_max')
        if request.GET.get(k+'_choice'):
            filter_submited_dict[k]['_choice'] = request.GET.get(k+'_choice')

        filters_dict[k] = {}
        filters_dict[k]['value'] = v
        filters_dict[k]['type'] = str(type(v))
        filters_dict[k]['choices'] = []
        if type(v) in (str, bool):
            for product in product_list:
                filters_dict[k]['choices'].append(product.attributes_json[k])

    product_list_filtered = []
    for product in product_list:
        pass_filtering = True
        print(product)
        for k,v in filter_submited_dict.items():
            if '_min' in v.keys():
                if product.attributes_json[k] < int(v['_min']):
                    pass_filtering = False
            if '_max' in v.keys():
                if product.attributes_json[k] > int(v['_max']):
                    pass_filtering = False
            if '_choice' in v.keys():
                if str(product.attributes_json[k]) != v['_choice']:
                    pass_filtering = False
        if pass_filtering:
            product_list_filtered.append(product)

    if request.GET.get('filter_active'):
        product_list = product_list_filtered

    return render(request, 'product_category.html', {'product_category': product_category,
                                                     'product_list': product_list,
                                                     'filter_submited_dict': filter_submited_dict,
                                                     'filters_dict': filters_dict})


def product_details(request, category_path, id):
    product = get_object_or_404(Product, id=id)
    product_category = ProductCategory.objects.get(category_path=category_path)
    return render(request, 'product_details.html', {'product': product,
                                                    'product_category': product_category})

