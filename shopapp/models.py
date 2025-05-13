from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField()  # เก็บเปอร์เซ็นต์ของส่วนลด
    rating = models.FloatField()
    rating_count = models.IntegerField()
    sold = models.IntegerField()
    stock = models.IntegerField()
    available_colors = models.JSONField(null=True, blank=True)  # ทำให้ไม่บังคับกรอก (nullable)
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # เพิ่มฟิลด์นี้

    def calculate_discount_percent(self):  # เปลี่ยนชื่อฟังก์ชัน
        try:
            return int((1 - (self.discounted_price / self.original_price)) * 100)
        except ZeroDivisionError:
            return 0

    def __str__(self):
        return self.name
