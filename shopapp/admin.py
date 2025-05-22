from django.contrib import admin
from django import forms
from .models import Product

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ถ้าไม่ได้ติ๊ก is_promotion ซ่อน discount_percent
        if not (self.instance and self.instance.is_promotion):
            self.fields['discount_percent'].widget = forms.HiddenInput()

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'original_price', 'discount_percent', 'discounted_price_display', 'stock', 'sold', 'rating', 'is_promotion')
    search_fields = ('name',)

    readonly_fields = ('discounted_price_display',)

    def discounted_price_display(self, obj):
        return obj.discounted_price
    discounted_price_display.short_description = 'Discounted Price'

admin.site.register(Product, ProductAdmin)
