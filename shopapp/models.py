from django.db import models
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percent = models.IntegerField(default=0)  # เก็บส่วนลดเป็น %  
    rating = models.FloatField(blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    sold = models.IntegerField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    available_colors = models.JSONField(null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    is_promotion = models.BooleanField(default=False)

    @property
    def discounted_price(self):
        if self.is_promotion and self.original_price and self.discount_percent:
            discount_rate = (100 - self.discount_percent) / 100
            return (self.original_price * Decimal(discount_rate)).quantize(Decimal('0.01'))
        return self.original_price

    def __str__(self):
        return self.name
