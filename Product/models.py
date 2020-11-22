from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.forms import ValidationError


class ProductCategory(models.Model):
    category_name = models.CharField(max_length=50)
    is_root = models.BooleanField(default=False, editable=False)
    root_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    category_path = models.CharField(max_length=300, editable=False, default=None, unique=True)

    attributes_json = models.JSONField(default={"dane": 0})
    attributes_old_json = models.JSONField(default=dict, editable=False)

    any_mapping_keyword = 'dowolny'

    def __str__(self):
        return self.category_path

    def make_root(self):
        self.is_root = True
        self.save()

    def un_root(self):
        self.is_root = False
        self.save()

    def update_category_path(self):
        if self.root_category:
            self.category_path = self.root_category.category_path + '-' + self.category_name
        else:
            self.category_path = self.category_name

    def update_category_attrbutes(self):
        new_attr = {}
        for k, v in self.root_category.attributes_json.items():
            if k in self.attributes_json.keys():
                if isinstance(product_attr[k], type(category_attr[k])):
                    new_attr[k] = self.attributes_json[k]
                else:
                    new_attr[k] = self.root_category.attributes_json[k]
            else:
                new_attr[k] = self.root_category.attributes_json[k]
        self.attributes_json = new_attr
        self.save()

    def validate_attributes_types(self):
        for k, v in self.attributes_json.items():
            if type(v) not in (int, float, list): # mozna dorzucic bool ewentualnie
                raise ValidationError('Dopuszczalne typy parametrów to (int, float, list)')

    def create_filter_dict(self, request, product_list): # tu mozna rozwazyc zeby filter_dict byl atrybutem klasy aktualizowanym zawsze po jej utworzeniu/zmianie
        filter_dict = {}
        for k, v in self.attributes_json.items():
            filter_dict[k] = {}
            filter_dict[k]['value'] = v
            filter_dict[k]['type'] = str(type(v))
            filter_dict[k]['choices'] = []
            filter_dict[k]['default'] = {}
            if type(v) in (int, float,):
                filter_dict[k]['default'] = {}
                filter_dict[k]['default']['min'] = request.GET.get(k + '_min', '')
                filter_dict[k]['default']['max'] = request.GET.get(k + '_max', '')
            if type(v) in (list,):
                filter_dict[k]['choices'] = v
                if len(filter_dict[k]['choices']) != 1:
                    filter_dict[k]['choices'].append(self.any_mapping_keyword)
                filter_dict[k]['default'] = []
                for choice in filter_dict[k]['choices']:
                    if request.GET.get(k + '_' + str(choice)) or request.GET.get(k + '_' + self.any_mapping_keyword):
                        filter_dict[k]['default'].append(choice) if choice not in filter_dict[k]['default'] else \
                        filter_dict[k]['default']
        return filter_dict

    def filter_products(self, request, filter_dict, product_list):
        product_list_filtered = []
        for product in product_list:
            pass_filtering = True
            for k, v in filter_dict.items():
                if 'int' in v['type'] or 'float' in v['type']:
                    if request.GET.get(k + '_min'):
                        if product.attributes_json[k] < float(request.GET.get(k + '_min')):
                            pass_filtering = False
                            break
                    if request.GET.get(k + '_max'):
                        if product.attributes_json[k] > float(request.GET.get(k + '_max')):
                            pass_filtering = False
                            break
                if 'list' in filter_dict[k]['type']:
                    choices = [choice for choice in v['choices'] if request.GET.get(k + '_' + str(choice))]
                    if not any(attr in choices for attr in product.attributes_json[k]) and not request.GET.get(k + '_' + self.any_mapping_keyword):
                        pass_filtering = False
                        break
            if pass_filtering:
                product_list_filtered.append(product)
        return product_list_filtered

@receiver(pre_save, sender=ProductCategory)
def update_category_pre(sender, instance, **kwargs):
    if instance.root_category and instance.root_category == instance:
        raise ValidationError('You cant make root category itself!')
    instance.validate_attributes_types()
    instance.update_category_path()
    if not instance.attributes_old_json:
        instance.attributes_old_json = instance.attributes_json
    if instance.attributes_json == {"dane": 0} and instance.root_category:
        instance.attributes_json = instance.root_category.attributes_json
    if instance.root_category:
        instance.root_category.make_root()
        for product in Product.objects.all():
            if product.product_category == instance.root_category:
                product.move_to_not_assigned()

@receiver(post_save, sender=ProductCategory)
def update_category_post(sender, instance, **kwargs):
    if instance.attributes_json != instance.attributes_old_json:
        for product in Product.objects.filter(product_category=instance):
            product.update_product_attrbutes()
        instance.attributes_old_json = instance.attributes_json
        instance.save()

        if instance.is_root:
            for category in ProductCategory.objects.filter(root_category=instance):
                category.update_category_attrbutes()

@receiver(post_delete, sender=ProductCategory)
def update_category_post_delete(sender, instance, **kwargs):
    print(instance.is_root, ProductCategory.objects.filter(root_category=instance.root_category))
    if not instance.is_root and not ProductCategory.objects.filter(root_category=instance.root_category):
        instance.root_category.un_root()

class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        limit_choices_to={'is_root': False}
    )
    attributes_json = models.JSONField(default={"dane": 0})

    def __str__(self):
        return self.product_name

    def move_to_not_assigned(self):
        if not ProductCategory.objects.filter(category_path='_Nieprzypisane'):
            ProductCategory.objects.create(category_name='_Nieprzypisane')
        self.product_category = ProductCategory.objects.get(category_path='_Nieprzypisane')
        self.attributes_json = {"dane": 0}
        self.save()

    def update_product_attrbutes(self):
        new_attr = {}
        for k, v in self.product_category.attributes_json.items():
            if k in self.attributes_json.keys():
                if isinstance(self.attributes_json[k], type(self.product_category.attributes_json[k])):
                    new_attr[k] = self.attributes_json[k]
                else:
                    new_attr[k] = self.product_category.attributes_json[k]
            else:
                new_attr[k] = self.product_category.attributes_json[k]
        self.attributes_json = new_attr
        self.save()

    def validate_attributes_json(self):
        product_attr = self.attributes_json
        category_attr = self.product_category.attributes_json
        if set(product_attr.keys()) != set(category_attr.keys()):
            raise ValidationError('Keys are not the same!') # dopisac listowanie brakujacych lub nadmiarowych kluczy
        for k,v in product_attr.items():
            if type(v) != type(category_attr[k]): # and not (type(v) == str and type(category_attr[k]) == list):
                raise ValidationError('One of key type is invalid!') # dopisac listowanie blednych kluczy
        for k,v in product_attr.items():
            if type(v) == list and not set(list(v)).issubset(list(category_attr[k])) or type(v) == str and not set([v,]).issubset(list(category_attr[k])):
                print(set(list(v)), list(category_attr[k]))
                raise ValidationError('Element listy nie znajduje sie w dopuszczalnych!') # dopisac listowanie blednych kluczy


@receiver(pre_save, sender=Product)
def update_product_pre(sender, instance, **kwargs):
    if instance.attributes_json == {"dane": 0}:
        instance.attributes_json = instance.product_category.attributes_json # TODO zamienic to na metode klasy
    else:
        instance.validate_attributes_json()
