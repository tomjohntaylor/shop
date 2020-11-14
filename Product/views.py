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

    for k, v in product_category.attributes_json.items():
        filters_dict[k] = {}
        filters_dict[k]['value'] = v
        filters_dict[k]['type'] = str(type(v))
        filters_dict[k]['choices'] = []
        if type(v) in (str, bool):
            for product in product_list:
                filters_dict[k]['choices'].append(product.attributes_json[k])
            filters_dict[k]['choices'].append('dowolny')

    if request.GET.get('filter_active'):
        filter_submited_dict = {}
        for k, v in filters_dict.items():
            print(v['type'])
            if 'int' in v['type']:
                filter_submited_dict[k] = {}
                if request.GET.get(k + '_min'):
                    filter_submited_dict[k]['_min'] = request.GET.get(k + '_min')
                if request.GET.get(k + '_max'):
                    filter_submited_dict[k]['_max'] = request.GET.get(k + '_max')
            if 'str' in v['type'] or 'bool' in v['type']:
                filter_submited_dict[k] = []
                for choice in v['choices']:
                    if request.GET.get(k + '_' + choice):
                        filter_submited_dict[k].append(choice)

        product_list_filtered = []
        for product in product_list:
            pass_filtering = True
            for k, v in filter_submited_dict.items():
                if 'int' in filters_dict[k]['type']:
                    if '_min' in v.keys():
                        if product.attributes_json[k] < int(v['_min']):
                            pass_filtering = False
                    if '_max' in v.keys():
                        if product.attributes_json[k] > int(v['_max']):
                            pass_filtering = False
                if 'str' in filters_dict[k]['type'] or 'bool' in filters_dict[k]['type']:
                    if str(product.attributes_json[k]) not in v and 'dowolny' not in v:
                        pass_filtering = False

            if pass_filtering:
                product_list_filtered.append(product)

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

