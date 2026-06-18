from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductImage, Review


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.action(description="Toggle Active Status")
def toggle_active(modeladmin, request, queryset):
    for product in queryset:
        product.is_active = not product.is_active
        product.save()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'seller',
        'category',
        'is_active'
    )

    actions = [toggle_active]

    inlines = [
        ProductVariantInline,
        ProductImageInline
    ]


admin.site.register(Category)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(Review)