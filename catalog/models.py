
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    description = models.TextField(blank=True)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    specs = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fastener lookup attributes
    family = models.ForeignKey(
        'catalog.LookupFamily', 
        on_delete=models.PROTECT, 
        null=True, 
        blank=True,
        related_name="products"
    )
    thread = models.ForeignKey(
        'catalog.LookupThread',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products"
    )
    head = models.ForeignKey(
        'catalog.LookupHead',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products"
    )
    drive = models.ForeignKey(
        'catalog.LookupDrive',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products"
    )
    material = models.ForeignKey(
        'catalog.LookupMaterial',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products"
    )
    feature = models.ForeignKey(
        'catalog.LookupFeature',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products"
    )
    finish = models.ForeignKey(
        'catalog.LookupFinish',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="products"
    )
    length_mm = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Length in millimeters"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def price(self):
        return self.price_usd

    @price.setter
    def price(self, value):
        self.price_usd = value

    @property
    def specifications(self):
        return self.specs

    @specifications.setter
    def specifications(self, value):
        self.specs = value


class Compatibility(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="compatibility_from")
    compatible_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="compatibility_to")

    def __str__(self):
        return f"{self.product.sku} -> {self.compatible_product.sku}"
