from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductImage, Review
from django.db.models import Count


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
        'variant_count',
        'is_active'
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(variant_total=Count('productvariant'))

    def variant_count(self, obj):
        return obj.variant_total

admin.site.register(Category)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(Review)