from django.contrib import admin
from .models import Product, Category, SpecialProduct, BookMark


admin.site.register(Category)
admin.site.register(SpecialProduct)
admin.site.register(BookMark)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)
