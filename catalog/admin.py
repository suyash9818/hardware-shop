from django.contrib import admin
from .models import Category, Product
from .lookup_models import (
    LookupFamily, LookupThread, LookupHead, 
    LookupDrive, LookupMaterial, LookupFeature, LookupFinish
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(LookupFamily)
class LookupFamilyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "ref_no")
    list_display_links = ("code", "name")
    search_fields = ("code", "name")


@admin.register(LookupThread)
class LookupThreadAdmin(admin.ModelAdmin):
    list_display = ("code", "ref_no")
    list_display_links = ("code",)
    filter_horizontal = ("applies_to_family",)


@admin.register(LookupHead)
class LookupHeadAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "ref_no")
    list_display_links = ("code", "description")
    filter_horizontal = ("applies_to_family",)


@admin.register(LookupDrive)
class LookupDriveAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "ref_no")
    list_display_links = ("code", "description")
    filter_horizontal = ("applies_to_family",)


@admin.register(LookupMaterial)
class LookupMaterialAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "ref_no")
    list_display_links = ("code", "description")
    filter_horizontal = ("applies_to_family",)


@admin.register(LookupFeature)
class LookupFeatureAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "ref_no")
    list_display_links = ("code", "description")


@admin.register(LookupFinish)
class LookupFinishAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "ref_no")
    list_display_links = ("code", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "category", "family", "thread", "length_mm", "price_usd", "created_at")
    list_filter = ("category", "family", "thread", "material", "finish")
    search_fields = ("sku", "name")
    fieldsets = (
        (None, {
            "fields": ("sku", "name", "category", "description", "price_usd")
        }),
        ("Fastener Attributes", {
            "fields": (
                ("family", "thread", "length_mm"),
                ("head", "drive"),
                ("material", "feature", "finish"),
            )
        }),
        ("Additional", {
            "fields": ("specs", "created_at"),
            "classes": ("collapse",)
        }),
    )
