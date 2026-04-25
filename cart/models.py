from django.db import models
from catalog.models import Product


class Cart(models.Model):
    session_id = models.CharField(max_length=255)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def line_total(self):
        return self.product.price * self.quantity
