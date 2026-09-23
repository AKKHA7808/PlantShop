from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    """แสดงฟิลด์ phone, address เพิ่มเติมใน Django Admin"""
    fieldsets = UserAdmin.fieldsets + (
        ('ข้อมูลร้านค้า', {'fields': ('phone', 'address')}),
    )
    list_display = ('username', 'first_name', 'email', 'phone', 'is_staff')
    search_fields = ('username', 'first_name', 'email', 'phone')


admin.site.register(User, CustomUserAdmin)
