from django.db import models

from django.contrib.auth.models import User
from django.utils.text import slugify

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError



class Category(models.Model):
    name = models.CharField(max_length=100)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def get_ancestors(self):
        ancestors = []
        current = self.parent

        while current:
            ancestors.append(current)
            current = current.parent

        return ancestors[::-1]

    def __str__(self):
        return self.name
    

class Product(models.Model):

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self,*args,**kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args,**kwargs)

    def __str__(self):
        return self.name
    

class ProductVariant(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    sku = models.CharField(
        max_length=100,
        unique=True
    )

    size = models.CharField(
        max_length=50
    )

    colour = models.CharField(
        max_length=50
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.sku
    

class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='products/'
    )

    alt_text = models.CharField(
        max_length=255
    )

    is_primary = models.BooleanField(
        default=False
    )


    def clean(self):
        if self.is_primary:
            existing = ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(pk=self.pk)

            if existing.exists():
                raise ValidationError(
                    "Only one primary image allowed."
             )
            
            
    def __str__(self):
        return self.alt_text
    
    
class Review(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField(
    validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ]
)
    

    body = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'product',
            'buyer'
        )

    def __str__(self):
        return str(self.rating)