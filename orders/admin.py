from django.contrib import admin

from .models import Order, OrderDetail


from django.utils.html import format_html

class OrderDetailInline(admin.TabularInline):
    """แสดงรายการสินค้าในคำสั่งซื้อแบบ inline เพื่อดูรายละเอียดได้ในหน้าเดียว"""
    model = OrderDetail
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'subtotal')
    can_delete = False
    
    def subtotal(self, obj):
        return f"{obj.subtotal} ฿"
    subtotal.short_description = 'ราคารวม'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'receiver_name', 'phone', 'total_price_display', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'receiver_name', 'phone', 'user__username')
    list_editable = ('status', )
    list_per_page = 20
    inlines = [OrderDetailInline]
    readonly_fields = ('user', 'total_price', 'created_at')
    
    def total_price_display(self, obj):
        return f"{obj.total_price} ฿"
    total_price_display.short_description = 'ยอดรวมสุทธิ'
