from django.db import models
from django.db.models.signals import pre_save, post_save
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

    attributes_json = models.JSONField(default={"dane": "brak"})
    attributes_old_json = models.JSONField(default=dict, editable=False)

    def __str__(self):
        return self.category_path

    def make_root(self):
        self.is_root = True
        self.save()

    def update_category_path(self):
        if self.root_category:
            self.category_path = self.root_category.category_path + '-' + self.category_name
        else:
            self.category_path = self.category_name


@receiver(pre_save, sender=ProductCategory)
def update_category_pre(sender, instance, **kwargs):
    if instance.root_category and instance.root_category == instance:
        raise ValidationError('You cant make root category itself!')

    instance.update_category_path()

    if not instance.attributes_old_json:
        instance.attributes_old_json = instance.attributes_json

    if instance.root_category:
        instance.root_category.make_root()

        for product in Product.objects.all():
            if product.product_category == instance.root_category:
                product.move_to_not_assigned()

@receiver(post_save, sender=ProductCategory)
def update_category_post(sender, instance, **kwargs):
    if instance.attributes_json != instance.attributes_old_json:
        for product in Product.objects.filter(product_category=instance):
            product.update_attrbutes()
        instance.attributes_old_json = instance.attributes_json
        instance.save()
    if instance.attributes_json == {"dane": "brak"} and instance.root_category:
        print("instance.attributes_json = instance.root_category.attributes_json")
        instance.attributes_json = instance.root_category.attributes_json
        instance.save()




class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        limit_choices_to={'is_root': False}
    )
    attributes_json = models.JSONField(default={"dane": "brak"})

    def __str__(self):
        return self.product_name

    def move_to_not_assigned(self):
        if not ProductCategory.objects.filter(category_path='_Nieprzypisane'):
            ProductCategory.objects.create(category_name='_Nieprzypisane')
        self.product_category = ProductCategory.objects.get(category_path='_Nieprzypisane')
        self.attributes_json = {"dane": "brak"}
        self.save()

    def update_attrbutes(self):
        product_attr = self.attributes_json
        category_attr = self.product_category.attributes_json
        new_attr = {}
        for k, v in category_attr.items():
            if k in product_attr.keys():
                new_attr[k] = product_attr[k]
            else:
                new_attr[k] = category_attr[k]
        self.attributes_json = new_attr
        self.save()

    def validate_attributes_json(self):
        product_attr = self.attributes_json
        category_attr = self.product_category.attributes_json
        if set(product_attr.keys()) != set(category_attr.keys()):
            raise ValidationError('Keys are not the same!') # dopisac listowanie brakujacych lub nadmiarowych kluczy
        category_attr_key_types = {}
        for k,v in category_attr.items():
            category_attr_key_types[k] = type(v)
        for k,v in product_attr.items():
            if type(v) != category_attr_key_types[k]:
                raise ValidationError('One of key type is invalid!') # dopisac listowanie blednych kluczy

@receiver(pre_save, sender=Product)
def update_product_pre(sender, instance, **kwargs):
    if instance.attributes_json == {"dane": "brak"}:
        instance.attributes_json = instance.product_category.attributes_json
    else:
        instance.validate_attributes_json()
