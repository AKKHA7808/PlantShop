from django.contrib import admin

from orders.models import Order, OrderDetail


from django.utils.html import format_html

class OrderDetailInline(admin.TabularInline):
    """แสดงรายการสินค้าในคำสั่งซื้อแบบ inline เพื่อดูรายละเอียดได้ในหน้าเดียว"""
    model = OrderDetail
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'subtotal')
    can_delete = False
    
    @admin.display(description='ราคารวม')
    def subtotal(self, obj):
        if not obj.pk:
            return "-"
        return f"{obj.subtotal} ฿"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'receiver_name', 'phone', 'total_price_display', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'receiver_name', 'phone', 'user__username')
    list_editable = ('status', )
    list_per_page = 20
    inlines = [OrderDetailInline]
    readonly_fields = ('user', 'total_price', 'created_at')
    
    @admin.display(description='ยอดรวมสุทธิ')
    def total_price_display(self, obj):
        if not obj.pk:
            return "-"
        return f"{obj.total_price} ฿"
