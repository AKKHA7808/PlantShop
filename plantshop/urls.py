from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'สวนใบไม้ - ระบบจัดการหลังบ้าน'
admin.site.site_title = 'สวนใบไม้ Admin'
admin.site.index_title = 'จัดการร้านค้า'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('', include('products.urls')),
]

# ให้ Django serve ไฟล์รูปภาพสินค้าตอน Debug (development เท่านั้น)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
