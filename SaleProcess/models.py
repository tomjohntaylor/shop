from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class Cart(models.Model):
    cart_name = models.CharField(max_length=100, default='domyślny') # TODO dodac obsluge wielu koszykow
    cart_json = models.JSONField(default=dict)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def add_product(self, product_id, qty):
        if product_id in self.cart_json.keys():
            self.cart_json[product_id] += int(qty)
        else:
            self.cart_json[product_id] = int(qty)

@receiver(pre_save, sender=Cart)
def update_cart_pre(sender, instance, **kwargs):
    if str(instance.user.username) not in instance.cart_name:
       instance.cart_name = str(instance.user.username) + '_' + instance.cart_name


def create_user_cart(user):
    cart = Cart.objects.filter(user=user)
    if not cart:
        cart = Cart(user=user)
    else:
        cart = cart[0]
    # cart.save()
    return cart
