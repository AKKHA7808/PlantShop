from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User model ของระบบ ใช้ Django Authentication เป็นหลัก
    เพิ่มฟิลด์ที่จำเป็นสำหรับร้านค้า: เบอร์โทรศัพท์ และที่อยู่
    (username, first_name, email, password มาจาก AbstractUser อยู่แล้ว)
    """
    phone = models.CharField('เบอร์โทรศัพท์', max_length=15, blank=True)
    address = models.TextField('ที่อยู่', blank=True)

    def __str__(self):
        return self.username
