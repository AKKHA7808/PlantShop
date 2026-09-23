from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product


class Order(models.Model):
    """คำสั่งซื้อของลูกค้า"""

    STATUS_PENDING = 'pending'
    STATUS_SHIPPING = 'shipping'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'รอดำเนินการ'),
        (STATUS_SHIPPING, 'กำลังจัดส่ง'),
        (STATUS_COMPLETED, 'สำเร็จ'),
        (STATUS_CANCELLED, 'ยกเลิก'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='ลูกค้า',
        on_delete=models.CASCADE, related_name='orders'
    )
    receiver_name = models.CharField('ชื่อผู้รับ', max_length=150)
    phone = models.CharField('เบอร์โทรศัพท์', max_length=15)
    shipping_address = models.TextField('ที่อยู่จัดส่ง')
    total_price = models.DecimalField('ราคารวม', max_digits=10, decimal_places=2)
    status = models.CharField('สถานะ', max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField('วันที่สั่งซื้อ', auto_now_add=True)

    class Meta:
        verbose_name = 'คำสั่งซื้อ'
        verbose_name_plural = 'คำสั่งซื้อ'
        ordering = ['-created_at']

    def __str__(self):
        return f'คำสั่งซื้อ #{self.id} - {self.user.username}'


class OrderDetail(models.Model):
    """รายการสินค้าในคำสั่งซื้อแต่ละรายการ"""
    order = models.ForeignKey(Order, verbose_name='คำสั่งซื้อ', on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, verbose_name='สินค้า', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField('จำนวน', validators=[MinValueValidator(1)])
    price = models.DecimalField('ราคาต่อชิ้น (ตอนสั่งซื้อ)', max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])

    class Meta:
        verbose_name = 'รายการสินค้าในคำสั่งซื้อ'
        verbose_name_plural = 'รายการสินค้าในคำสั่งซื้อ'

    def __str__(self):
        product_name = self.product.name if self.product else "สินค้าที่ถูกลบ"
        return f"{product_name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.price * self.quantity
