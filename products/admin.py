from django.contrib import admin

from .models import Category, Product


from django.utils.html import format_html

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail', 'name', 'category', 'price', 'stock', 'is_out_of_stock', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')  # แก้ราคา/สต็อกได้เร็วจากหน้ารายการ
    list_per_page = 20
    
    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = 'รูปภาพ'
    
    def is_out_of_stock(self, obj):
        return obj.stock <= 0
    is_out_of_stock.short_description = 'สินค้าหมด?'
    is_out_of_stock.boolean = True
