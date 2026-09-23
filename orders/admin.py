from django.contrib import admin

from .models import Order, OrderDetail


class OrderDetailInline(admin.TabularInline):
    """แสดงรายการสินค้าในคำสั่งซื้อแบบ inline เพื่อดูรายละเอียดได้ในหน้าเดียว"""
    model = OrderDetail
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'receiver_name', 'phone', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('receiver_name', 'phone', 'user__username')
    list_editable = ('status',)  # Admin เปลี่ยนสถานะคำสั่งซื้อได้เร็วจากหน้ารายการ
    inlines = [OrderDetailInline]
    readonly_fields = ('user', 'total_price', 'created_at')
