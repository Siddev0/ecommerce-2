from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_description = models.TextField()
    category_image = models.ImageField(upload_to='images/category')

    def __str__(self) -> str:
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='images/product')
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_stock = models.IntegerField(default=0)
    is_available = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name