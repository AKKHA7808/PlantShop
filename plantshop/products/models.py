from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    """หมวดหมู่สินค้า เช่น ไม้ประดับ, ไม้ดอก, ไม้ฟอกอากาศ"""
    name = models.CharField('ชื่อหมวดหมู่', max_length=100, unique=True)

    class Meta:
        verbose_name = 'หมวดหมู่สินค้า'
        verbose_name_plural = 'หมวดหมู่สินค้า'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """สินค้า (ต้นไม้/ดอกไม้ประดับ)"""
    name = models.CharField('ชื่อสินค้า', max_length=200)
    category = models.ForeignKey(
        Category, verbose_name='หมวดหมู่', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='products'
    )
    description = models.TextField('รายละเอียดสินค้า', blank=True)
    price = models.DecimalField('ราคา', max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    stock = models.PositiveIntegerField('จำนวนคงเหลือ', default=0)
    image = models.ImageField('รูปสินค้า', upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField('วันที่เพิ่มสินค้า', auto_now_add=True)

    class Meta:
        verbose_name = 'สินค้า'
        verbose_name_plural = 'สินค้า'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_out_of_stock(self):
        return self.stock == 0
